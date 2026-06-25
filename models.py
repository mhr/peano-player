"""
models.py — Policy architectures for Peano tactic synthesis.

MonolithPolicy:
  Baseline transformer. tokens → logits.
"""

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Bandit constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEP_TOKEN = 250
TACTIC_OFFSET = 252
NUM_BANDIT_ACTIONS = 4

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Shared building blocks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TransformerBlock(eqx.Module):
    norm1: eqx.nn.LayerNorm
    norm2: eqx.nn.LayerNorm
    attn: eqx.nn.MultiheadAttention
    mlp: eqx.nn.MLP

    def __init__(self, d_model, n_heads, *, key):
        k1, k2 = jr.split(key)
        self.norm1 = eqx.nn.LayerNorm(d_model)
        self.norm2 = eqx.nn.LayerNorm(d_model)
        self.attn = eqx.nn.MultiheadAttention(
            num_heads=n_heads, query_size=d_model,
            key_size=d_model, value_size=d_model,
            output_size=d_model, key=k1,
        )
        self.mlp = eqx.nn.MLP(
            in_size=d_model, out_size=d_model,
            width_size=4 * d_model, depth=1,
            activation=jax.nn.gelu, key=k2,
        )

    def __call__(self, x):
        seq_len = x.shape[0]
        mask = jnp.tril(jnp.ones((seq_len, seq_len), dtype=jnp.bool_))
        h = jax.vmap(self.norm1)(x)
        h = self.attn(h, h, h, mask=mask) + x
        out = jax.vmap(self.mlp)(jax.vmap(self.norm2)(h)) + h
        return out


class TransformerEncoder(eqx.Module):
    """Byte-level transformer encoder → last-token representation."""
    embedding: eqx.nn.Embedding
    pos_embedding: eqx.nn.Embedding
    blocks: list
    norm_f: eqx.nn.LayerNorm

    def __init__(self, vocab_size, max_seq_len, d_model, n_heads, n_layers, *, key):
        keys = jr.split(key, n_layers + 2)
        self.embedding = eqx.nn.Embedding(vocab_size, d_model, key=keys[0])
        self.pos_embedding = eqx.nn.Embedding(max_seq_len, d_model, key=keys[1])
        self.blocks = [
            TransformerBlock(d_model, n_heads, key=keys[i + 2])
            for i in range(n_layers)
        ]
        self.norm_f = eqx.nn.LayerNorm(d_model)

    def __call__(self, token_ids):
        seq_len = token_ids.shape[0]
        tok_emb = jax.vmap(self.embedding)(token_ids)
        pos_emb = jax.vmap(self.pos_embedding)(jnp.arange(seq_len))
        x = tok_emb + pos_emb
        for block in self.blocks:
            x = block(x)
        x = jax.vmap(self.norm_f)(x)
        return x[-1]  # (d_model,)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Monolithic baseline
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MonolithPolicy(eqx.Module):
    """Baseline transformer policy with optional value head for PPO/RCPO.

    __call__ returns logits only (BC-compatible).
    forward_with_value() returns (logits, value) for actor-critic training.
    """
    encoder: TransformerEncoder
    head: eqx.nn.Linear
    value_head: eqx.nn.Linear

    def __init__(self, vocab_size, max_seq_len, d_model, n_heads, n_layers,
                 num_tactics, *, key):
        k_enc, k_head, k_val = jr.split(key, 3)
        self.encoder = TransformerEncoder(
            vocab_size, max_seq_len, d_model, n_heads, n_layers, key=k_enc)
        self.head = eqx.nn.Linear(d_model, num_tactics, key=k_head)
        self.value_head = eqx.nn.Linear(d_model, 1, key=k_val)

    def __call__(self, token_ids):
        """Returns logits. BC-compatible."""
        return self.head(self.encoder(token_ids))

    def forward_with_value(self, token_ids):
        """Returns (logits, value). For PPO/RCPO training."""
        h = self.encoder(token_ids)
        logits = self.head(h)
        value = self.value_head(h).squeeze()
        return logits, value

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Bandit model for baselines
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AutoregressivePolicy(eqx.Module):
    """Bandit/open-loop policy. [goal_bytes, SEP, prev_tactics] → 5 logits.
    No value head — designed for critic-free methods (GRPO, MaxRL)."""
    encoder: TransformerEncoder
    head: eqx.nn.Linear

    def __init__(self, vocab_size, max_seq_len, d_model, n_heads, n_layers, num_tactics, *, key):
        k_enc, k_head = jr.split(key)
        self.encoder = TransformerEncoder(
            vocab_size, max_seq_len, d_model, n_heads, n_layers, key=k_enc)
        self.head = eqx.nn.Linear(d_model, num_tactics, key=k_head)

    def __call__(self, token_ids):
        return self.head(self.encoder(token_ids))
