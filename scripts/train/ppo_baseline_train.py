"""
ppo_baseline_train.py — PPO + reward shaping baseline for Peano tactic synthesis.

MonolithPolicy with fixed penalty λ for tactic failures.
Reward at each step: r - λ * (tactic_failed).
No adaptive Lagrangian.

Default model config (d_model=256, n_layers=5) is param-matched
to GoalConstraintPolicy (d_model=128, n_layers=4, 5 encoders) at ~4M params.

Usage:
  python scripts/train/ppo_baseline_train.py [--num-iterations 2000] [--fresh]
"""

import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import argparse
import random
import time
from dataclasses import dataclass
from pathlib import Path

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr
import numpy as np
import optax
from tqdm import tqdm

try:
    import wandb
    HAS_WANDB = True
except ImportError:
    HAS_WANDB = False

from peano_player.gen import (
    generate_one, to_lean, clone, rewrite_in_goal,
    RULES, TACTIC_TO_IDX,
)
from peano_player.models import MonolithPolicy, count_params

print(f"JAX devices: {jax.devices()}")

NUM_TACTICS = 4


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class PPOBaselineConfig:
    # ── Model (param-matched to GCPO) ──
    vocab_size: int = 256
    max_seq_len: int = 256
    d_model: int = 256
    n_heads: int = 4
    n_layers: int = 5
    num_tactics: int = NUM_TACTICS

    # ── PPO ──
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_coef: float = 0.2
    ent_coef: float = 0.01
    vf_coef: float = 0.5
    update_epochs: int = 4
    minibatch_size: int = 64
    max_grad_norm: float = 1.0
    target_kl: float = 0.02
    anneal_lr: bool = True
    learning_rate: float = 3e-4

    # ── Reward shaping ──
    cost_penalty: float = 1.0     # fixed λ: reward = r - λ * cost

    # ── Rollout / env ──
    episodes_per_iter: int = 64
    max_steps: int = 20
    min_difficulty: int = 1
    max_difficulty: int = 8

    # ── Training ──
    seed: int = 0
    num_iterations: int = 2000
    wandb_project: str = "peano-player"
    log_every: int = 1
    save_every: int = 200
    checkpoint_dir: str = "checkpoints/ppo_baseline"
    fresh: bool = False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Tokenization
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def tokenize_goal(goal_str: str, max_len: int) -> jnp.ndarray:
    raw = [min(b, 255) for b in goal_str.encode("utf-8")[:max_len]]
    padded = raw + [0] * (max_len - len(raw))
    return jnp.array(padded, dtype=jnp.int32)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Environment step
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def step_env(lhs, rhs, action: int):
    rule = RULES[action]
    result = rewrite_in_goal(lhs, rhs, rule)
    cost = 0.0

    if result is None:
        return lhs, rhs, 0.0, 1.0, True  # reward, cost, done

    new_lhs, new_rhs = result
    if new_lhs == new_rhs:
        return new_lhs, new_rhs, 1.0, 0.0, True

    return new_lhs, new_rhs, 0.0, 0.0, False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JIT helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@eqx.filter_jit
def _jit_forward(policy, tokens):
    return policy.forward_with_value(tokens)


@eqx.filter_jit
def _jit_sample(key, logits):
    action = jr.categorical(key, logits)
    log_prob = jax.nn.log_softmax(logits)[action]
    return action, log_prob


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Rollout
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def rollout_episode(policy, cfg, key):
    difficulty = random.randint(cfg.min_difficulty, cfg.max_difficulty)
    both_sides = random.random() < 0.35

    thm = None
    for _ in range(20):
        thm = generate_one(name="t", difficulty=difficulty, both_sides=both_sides)
        if thm is not None:
            break
    if thm is None:
        return None

    lhs, rhs = clone(thm.lhs), clone(thm.rhs)

    tokens_l, actions_l, shaped_rewards_l = [], [], []
    values_l, log_probs_l, dones_l = [], [], []
    raw_rewards_l, costs_l = [], []

    for _ in range(cfg.max_steps):
        if lhs == rhs:
            break

        goal_str = f"{to_lean(lhs)} = {to_lean(rhs)}"
        tokens = tokenize_goal(goal_str, cfg.max_seq_len)

        logits, value = _jit_forward(policy, tokens)

        key, subkey = jr.split(key)
        action, log_prob = _jit_sample(subkey, logits)
        action = int(action)
        log_prob = float(log_prob)

        lhs, rhs, reward, cost, done = step_env(lhs, rhs, action)

        # Shaped reward: r - λ * cost
        shaped_reward = reward - cfg.cost_penalty * cost

        tokens_l.append(np.array(tokens))
        actions_l.append(action)
        shaped_rewards_l.append(shaped_reward)
        raw_rewards_l.append(reward)
        costs_l.append(cost)
        values_l.append(float(value))
        log_probs_l.append(log_prob)
        dones_l.append(float(done))

        if done:
            break

    if not tokens_l:
        return None

    return {
        "tokens":          np.stack(tokens_l),
        "actions":         np.array(actions_l),
        "shaped_rewards":  np.array(shaped_rewards_l, dtype=np.float32),
        "raw_rewards":     np.array(raw_rewards_l, dtype=np.float32),
        "costs":           np.array(costs_l, dtype=np.float32),
        "values":          np.array(values_l, dtype=np.float32),
        "log_probs":       np.array(log_probs_l, dtype=np.float32),
        "dones":           np.array(dones_l, dtype=np.float32),
        "solved":          any(r > 0 for r in raw_rewards_l),
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GAE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def compute_gae(rewards, values, dones, gamma, lam):
    T = len(rewards)
    advantages = np.zeros(T, dtype=np.float32)
    lastgae = 0.0
    for t in reversed(range(T)):
        next_val = values[t + 1] if t < T - 1 else 0.0
        nonterminal = 1.0 - dones[t] if t < T - 1 else 0.0
        delta = rewards[t] + gamma * next_val * nonterminal - values[t]
        advantages[t] = lastgae = delta + gamma * lam * nonterminal * lastgae
    returns = advantages + values
    return advantages, returns


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Batch assembly
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def collect_batch(policy, cfg, key):
    episodes = []
    for _ in range(cfg.episodes_per_iter):
        key, subkey = jr.split(key)
        ep = rollout_episode(policy, cfg, subkey)
        if ep is not None:
            episodes.append(ep)

    if not episodes:
        return None

    def cat(arrays):
        return np.concatenate(arrays)

    advs, rets = [], []
    for ep in episodes:
        a, r = compute_gae(ep["shaped_rewards"], ep["values"],
                           ep["dones"], cfg.gamma, cfg.gae_lambda)
        advs.append(a)
        rets.append(r)

    batch = {k: jnp.array(cat([e[k] for e in episodes]))
             for k in ("tokens", "actions", "shaped_rewards", "raw_rewards",
                        "costs", "values", "log_probs", "dones")}

    batch["advantages"] = jnp.array(cat(advs))
    batch["returns"] = jnp.array(cat(rets))

    batch["solve_rate"] = float(np.mean([e["solved"] for e in episodes]))
    batch["avg_ep_len"] = float(np.mean([len(e["raw_rewards"]) for e in episodes]))
    batch["total_costs"] = float(cat([e["costs"] for e in episodes]).sum())
    batch["mean_cost_per_ep"] = batch["total_costs"] / len(episodes)
    batch["num_episodes"] = len(episodes)

    return batch


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PPO step
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@eqx.filter_jit
def ppo_step(policy, tokens, actions, old_lp, old_values,
             advantages, returns, clip_coef, vf_coef, ent_coef):
    """Standard PPO step. Returns (loss, grads, approx_kl)."""
    def loss_fn(model):
        def single(tok, act, olp, old_v, adv, ret):
            logits, value = model.forward_with_value(tok)

            lp = jax.nn.log_softmax(logits)[act]
            logratio = lp - olp
            ratio = jnp.exp(logratio)

            pg1 = -adv * ratio
            pg2 = -adv * jnp.clip(ratio, 1.0 - clip_coef, 1.0 + clip_coef)
            pg_loss = jnp.maximum(pg1, pg2)

            v_loss_unclipped = (value - ret) ** 2
            v_clipped = old_v + jnp.clip(value - old_v, -clip_coef, clip_coef)
            v_loss_clipped = (v_clipped - ret) ** 2
            v_loss = 0.5 * jnp.maximum(v_loss_unclipped, v_loss_clipped)

            probs = jax.nn.softmax(logits)
            entropy = -jnp.sum(probs * jnp.log(probs + 1e-8))

            approx_kl = (ratio - 1.0) - logratio

            return pg_loss, v_loss, entropy, approx_kl

        pg, vl, ent, kl = jax.vmap(single)(
            tokens, actions, old_lp, old_values, advantages, returns)
        loss = jnp.mean(pg) + vf_coef * jnp.mean(vl) - ent_coef * jnp.mean(ent)
        return loss, jnp.mean(kl)

    (loss, approx_kl), grads = eqx.filter_value_and_grad(loss_fn, has_aux=True)(policy)
    return loss, grads, approx_kl


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Checkpointing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def save_checkpoint(policy, opt_state, step, ckpt_dir):
    eqx.tree_serialise_leaves(str(ckpt_dir / f"policy_{step}.eqx"), policy)
    eqx.tree_serialise_leaves(str(ckpt_dir / f"opt_{step}.eqx"), opt_state)

    if HAS_WANDB and wandb.run is not None:
        artifact = wandb.Artifact(f"ppo-baseline-checkpoint-{step}", type="checkpoint")
        artifact.add_file(str(ckpt_dir / f"policy_{step}.eqx"))
        artifact.add_file(str(ckpt_dir / f"opt_{step}.eqx"))
        wandb.log_artifact(artifact)


def find_latest_checkpoint(ckpt_dir):
    existing = list(ckpt_dir.glob("policy_*.eqx"))
    if not existing:
        return None
    return max(int(p.stem.split("_")[1]) for p in existing)


def load_checkpoint(policy, opt, step, ckpt_dir):
    policy = eqx.tree_deserialise_leaves(str(ckpt_dir / f"policy_{step}.eqx"), policy)
    opt_state = opt.init(eqx.filter(policy, eqx.is_array))
    opt_state = eqx.tree_deserialise_leaves(str(ckpt_dir / f"opt_{step}.eqx"), opt_state)
    return policy, opt_state


def save_run_id(run_id, ckpt_dir):
    (ckpt_dir / "wandb_run_id.txt").write_text(run_id)


def load_run_id(ckpt_dir):
    path = ckpt_dir / "wandb_run_id.txt"
    if path.exists():
        return path.read_text().strip()
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main training loop
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def train(cfg: PPOBaselineConfig):
    key = jr.PRNGKey(cfg.seed)
    random.seed(cfg.seed)

    ckpt_dir = Path(cfg.checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    if cfg.fresh:
        for f in ckpt_dir.glob("policy_*"):
            f.unlink()
        for f in ckpt_dir.glob("opt_*"):
            f.unlink()
        print(f"Fresh start. Cleared checkpoints in {ckpt_dir}")

    key, model_key = jr.split(key)
    policy = MonolithPolicy(
        vocab_size=cfg.vocab_size, max_seq_len=cfg.max_seq_len,
        d_model=cfg.d_model, n_heads=cfg.n_heads, n_layers=cfg.n_layers,
        num_tactics=cfg.num_tactics, key=model_key,
    )
    print(f"MonolithPolicy: {count_params(policy):,} params (λ={cfg.cost_penalty})")

    opt = optax.chain(
        optax.clip_by_global_norm(cfg.max_grad_norm),
        optax.adam(cfg.learning_rate),
    )
    opt_state = opt.init(eqx.filter(policy, eqx.is_array))

    start_iter = 0
    if not cfg.fresh:
        latest = find_latest_checkpoint(ckpt_dir)
        if latest is not None:
            start_iter = latest
            policy, opt_state = load_checkpoint(policy, opt, start_iter, ckpt_dir)
            print(f"Resumed from iteration {start_iter}")

    if HAS_WANDB:
        if cfg.fresh:
            run_id = f"ppo-baseline-lambda{cfg.cost_penalty}-{int(time.time())}"
            # run_id = f"ppo-baseline-{int(time.time())}"
            save_run_id(run_id, ckpt_dir)
        else:
            run_id = load_run_id(ckpt_dir)
            if run_id is None:
                run_id = f"ppo-baseline-{int(time.time())}"
                save_run_id(run_id, ckpt_dir)
        wandb.init(
            project=cfg.wandb_project,
            name=run_id,
            id=run_id,
            resume="allow",
            config=vars(cfg),
        )

    solve_ema = 0.0
    cost_ema = 0.0
    ema_alpha = 0.05

    pbar = tqdm(range(start_iter, cfg.num_iterations), desc="PPO-baseline",
                initial=start_iter, total=cfg.num_iterations)
    for iteration in pbar:
        key, rollout_key = jr.split(key)

        batch = collect_batch(policy, cfg, rollout_key)
        if batch is None:
            continue
        N = batch["tokens"].shape[0]
        if N < 2:
            continue

        solve_ema += ema_alpha * (batch["solve_rate"] - solve_ema)
        cost_ema += ema_alpha * (batch["mean_cost_per_ep"] - cost_ema)
        ep_reward = float(batch["raw_rewards"].sum()) / batch["num_episodes"]

        if cfg.anneal_lr:
            anneal_frac = 1.0 - iteration / cfg.num_iterations
        else:
            anneal_frac = 1.0

        kl_exceeded = False
        for _epoch in range(cfg.update_epochs):
            if kl_exceeded:
                break
            key, perm_key = jr.split(key)
            perm = jr.permutation(perm_key, N)

            for start in range(0, N, cfg.minibatch_size):
                if kl_exceeded:
                    break
                end = min(start + cfg.minibatch_size, N)
                idx = perm[start:end]

                mb_adv = batch["advantages"][idx]
                mb_adv = (mb_adv - jnp.mean(mb_adv)) / (jnp.std(mb_adv) + 1e-8)

                loss, grads, kl = ppo_step(
                    policy,
                    batch["tokens"][idx],
                    batch["actions"][idx],
                    batch["log_probs"][idx],
                    batch["values"][idx],
                    mb_adv,
                    batch["returns"][idx],
                    cfg.clip_coef, cfg.vf_coef, cfg.ent_coef,
                )

                grads = jax.tree.map(lambda g: g * anneal_frac, grads)

                updates, opt_state = opt.update(
                    eqx.filter(grads, eqx.is_array),
                    opt_state,
                    eqx.filter(policy, eqx.is_array),
                )
                policy = eqx.apply_updates(policy, updates)

                if cfg.target_kl is not None and float(kl) > cfg.target_kl:
                    kl_exceeded = True
                    break

        pbar.set_postfix_str(
            f"solve={solve_ema:.1%} cost={cost_ema:.2f}"
        )

        if (iteration + 1) % cfg.log_every == 0:
            log = {
                "iteration": iteration + 1,
                "solve_rate": batch["solve_rate"],
                "avg_ep_len": batch["avg_ep_len"],
                "reward/ep": ep_reward,
                "mean_cost_per_ep": batch["mean_cost_per_ep"],
                "batch_steps": int(N),
                "num_episodes": batch["num_episodes"],
            }
            if HAS_WANDB and wandb.run is not None:
                wandb.log(log)

            tqdm.write(
                f"  [{iteration+1:>5}] solve={batch['solve_rate']:.1%} "
                f"rew/ep={ep_reward:.3f} len={batch['avg_ep_len']:.1f} "
                f"cost/ep={batch['mean_cost_per_ep']:.2f}"
            )

        if (iteration + 1) % cfg.save_every == 0:
            step = iteration + 1
            save_checkpoint(policy, opt_state, step, ckpt_dir)
            tqdm.write(f"  -> checkpoint at iteration {step}")

    save_checkpoint(policy, opt_state, cfg.num_iterations, ckpt_dir)
    if HAS_WANDB and wandb.run is not None:
        wandb.finish()
    print("PPO baseline training complete.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description="PPO baseline for Peano tactic synthesis")
    parser.add_argument("--num-iterations", type=int, default=2000)
    parser.add_argument("--episodes-per-iter", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--cost-penalty", type=float, default=1.0,
                        help="Fixed λ for reward shaping (r - λ*cost)")
    parser.add_argument("--n-layers", type=int, default=5)
    parser.add_argument("--d-model", type=int, default=256)
    parser.add_argument("--max-difficulty", type=int, default=8)
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--checkpoint-dir", type=str, default=None)
    args = parser.parse_args()


    ckpt_dir = args.checkpoint_dir or f"checkpoints/ppo_baseline_lambda{args.cost_penalty}_seed{args.seed}"

    cfg = PPOBaselineConfig(
        num_iterations=args.num_iterations,
        episodes_per_iter=args.episodes_per_iter,
        learning_rate=args.learning_rate,
        cost_penalty=args.cost_penalty,
        n_layers=args.n_layers,
        d_model=args.d_model,
        max_difficulty=args.max_difficulty,
        fresh=args.fresh,
        seed=args.seed,
        checkpoint_dir=ckpt_dir,
    )
    train(cfg)


if __name__ == "__main__":
    main()