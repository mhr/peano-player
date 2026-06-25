"""
grpo_bandit_train.py — Bandit GRPO/MaxRL with autoregressive tactic generation.

Kim & Yun (ICLR 2026) MDP: model generates full tactic sequence from initial
goal only, never seeing intermediate proof states. After generation, execute
against env and score with GRPO or MaxRL + optional tactic φ.

No EOS token — model always generates max_steps tactics. Execution stops at
first error or proof closure; all steps are scored via first-error propagation.

Model: AutoregressivePolicy(num_tactics=4) — same 4 tactic outputs as
MonolithPolicy, but input is [goal_bytes, SEP, prev_tactics] with causal
attention over the full sequence.

Usage:
  python grpo_bandit_train.py --fresh --advantage grpo          # GRPO + φ
  python grpo_bandit_train.py --fresh --advantage grpo --no-phi # GRPO binary
  python grpo_bandit_train.py --fresh --advantage maxrl --no-phi # MaxRL binary
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

from gen import generate_one, to_lean, clone, rewrite_in_goal, RULES, TACTIC_TO_IDX
from models import AutoregressivePolicy, count_params, SEP_TOKEN, TACTIC_OFFSET

print(f"JAX devices: {jax.devices()}")
NUM_TACTICS = 4


@dataclass
class GRPOBanditConfig:
    vocab_size: int = 256
    max_seq_len: int = 280
    d_model: int = 256
    n_heads: int = 4
    n_layers: int = 5
    num_tactics: int = NUM_TACTICS
    clip_coef: float = 0.2
    ent_coef: float = 0.01
    update_epochs: int = 4
    minibatch_size: int = 64
    max_grad_norm: float = 1.0
    target_kl: float = 0.02
    anneal_lr: bool = True
    learning_rate: float = 3e-4
    G: int = 4
    d1: float = 0.0              # valid tactic, proof failed (matched to PPO)
    d2: float = -1.0             # erroneous tactic (matched to PPO)
    advantage: str = "grpo"      # "grpo" or "maxrl"
    use_phi: bool = True          # use tactic φ process signal
    theorems_per_iter: int = 16
    max_steps: int = 20
    min_difficulty: int = 1
    max_difficulty: int = 8
    goal_max_len: int = 256
    num_iterations: int = 2000
    seed: int = 0
    wandb_project: str = "peano-player"
    log_every: int = 1
    save_every: int = 200
    checkpoint_dir: str = "checkpoints/grpo_bandit"
    fresh: bool = False


def tokenize_bandit(goal_str, prev_tactic_ids, max_len, goal_max_len=256):
    """Tokenize [goal_bytes..., SEP, tactic_tokens...] padded to max_len."""
    goal_bytes = [min(b, 249) for b in goal_str.encode("utf-8")[:goal_max_len]]
    seq = goal_bytes + [SEP_TOKEN]
    for tid in prev_tactic_ids:
        seq.append(TACTIC_OFFSET + tid)
    seq = seq[:max_len]
    padded = seq + [0] * (max_len - len(seq))
    return jnp.array(padded, dtype=jnp.int32)


@eqx.filter_jit
def _jit_forward(policy, tokens):
    return policy(tokens)


@eqx.filter_jit
def _jit_sample(key, logits):
    action = jr.categorical(key, logits)
    log_prob = jax.nn.log_softmax(logits)[action]
    return action, log_prob


def rollout_bandit(policy, lhs, rhs, cfg, key):
    """Generate max_steps tactics autoregressively, then execute post-hoc.

    Generation: model sees [goal, SEP, prev_tactics] at each step.
    Always generates exactly max_steps tactics (no EOS, no early exit).

    Execution: run tactics against env to find first error or proof closure.
    ALL max_steps steps are kept for training — no truncation.

    φ scoring (Kim & Yun first-error propagation):
      - Solved: all steps get φ=1.0
      - Failed: steps before first error get d1, steps at/after get d2
    """
    goal_str = f"{to_lean(lhs)} = {to_lean(rhs)}"

    # ── Phase 1: Generate all tactics ──
    prev_tactics = []
    all_actions = []
    all_log_probs = []
    all_tokens = []

    for _ in range(cfg.max_steps):
        tokens = tokenize_bandit(goal_str, prev_tactics,
                                 cfg.max_seq_len, cfg.goal_max_len)
        all_tokens.append(np.array(tokens))

        logits = _jit_forward(policy, tokens)
        key, subkey = jr.split(key)
        action, log_prob = _jit_sample(subkey, logits)
        action = int(action)
        log_prob = float(log_prob)

        all_actions.append(action)
        all_log_probs.append(log_prob)
        prev_tactics.append(action)

    n = len(all_actions)

    # ── Phase 2: Execute to find first error / proof closure ──
    exec_lhs, exec_rhs = clone(lhs), clone(rhs)
    first_error = None

    for i, a in enumerate(all_actions):
        if exec_lhs == exec_rhs:
            break  # proof already closed
        result = rewrite_in_goal(exec_lhs, exec_rhs, RULES[a])
        if result is None:
            first_error = i
            break
        exec_lhs, exec_rhs = result

    solved = (exec_lhs == exec_rhs)

    # ── Phase 3: φ scores over ALL steps (no truncation) ──
    phi = np.zeros(n, dtype=np.float32)
    if solved:
        phi[:] = 1.0
    else:
        for i in range(n):
            if first_error is not None and i >= first_error:
                phi[i] = cfg.d2
            else:
                phi[i] = cfg.d1

    return {
        "step_tokens": np.stack(all_tokens),
        "actions":     np.array(all_actions),
        "log_probs":   np.array(all_log_probs, dtype=np.float32),
        "phi":         phi,
        "solved":      bool(solved),
        "num_steps":   n,
    }


def collect_batch(policy, cfg, key):
    all_tokens, all_actions, all_log_probs, all_advantages = [], [], [], []
    total_solved, total_episodes, total_costs = 0, 0, 0.0

    for _ in range(cfg.theorems_per_iter):
        difficulty = random.randint(cfg.min_difficulty, cfg.max_difficulty)
        both_sides = random.random() < 0.35
        thm = None
        for _ in range(20):
            thm = generate_one(name="t", difficulty=difficulty, both_sides=both_sides)
            if thm is not None:
                break
        if thm is None:
            continue

        episodes = []
        for _ in range(cfg.G):
            key, subkey = jr.split(key)
            ep = rollout_bandit(policy, thm.lhs, thm.rhs, cfg, subkey)
            if ep is not None:
                episodes.append(ep)
        if len(episodes) < 2:
            continue

        outcomes = np.array([1.0 if ep["solved"] else 0.0 for ep in episodes])
        mean_outcome = outcomes.mean()
        std_outcome = outcomes.std() + 1e-8
        K = int(outcomes.sum())

        # ── Count ALL episodes for true metrics (before any skip) ──
        total_episodes += len(episodes)
        total_solved += K
        for ep in episodes:
            total_costs += sum(1 for i in range(ep["num_steps"])
                               if ep["phi"][i] == cfg.d2)

        # Skip degenerate groups for MaxRL
        if cfg.advantage == "maxrl" and (K == 0 or K == len(episodes)):
            # All same outcome — no contrastive signal
            # Still include process signal if use_phi
            if not cfg.use_phi:
                continue

        for ei, ep in enumerate(episodes):
            n = ep["num_steps"]

            # ── Outcome advantage ──
            if cfg.advantage == "grpo":
                a_outcome = (outcomes[ei] - mean_outcome) / std_outcome
            elif cfg.advantage == "maxrl":
                if K == 0 or K == len(episodes):
                    a_outcome = 0.0
                elif outcomes[ei] == 1.0:
                    a_outcome = 1.0 / K
                else:
                    a_outcome = 0.0  # failures get zero outcome signal
            else:
                raise ValueError(f"Unknown advantage method: {cfg.advantage}")

            # ── Process advantage (tactic φ) ──
            if cfg.use_phi:
                a_process = ep["phi"] - mean_outcome
            else:
                a_process = np.zeros(n, dtype=np.float32)

            advantages = np.full(n, a_outcome, dtype=np.float32) + a_process

            all_tokens.append(ep["step_tokens"])
            all_actions.append(ep["actions"])
            all_log_probs.append(ep["log_probs"])
            all_advantages.append(advantages)

    if not all_tokens:
        # No training data (e.g. MaxRL skipped all groups), but still report metrics
        if total_episodes > 0:
            return {
                "tokens": None,
                "solve_rate": total_solved / total_episodes,
                "num_episodes": total_episodes,
                "mean_cost_per_ep": total_costs / total_episodes,
                "avg_ep_len": float(cfg.max_steps),
            }
        return None

    batch = {
        "tokens":     jnp.array(np.concatenate(all_tokens)),
        "actions":    jnp.array(np.concatenate(all_actions)),
        "log_probs":  jnp.array(np.concatenate(all_log_probs)),
        "advantages": jnp.array(np.concatenate(all_advantages)),
    }
    batch["solve_rate"] = total_solved / max(total_episodes, 1)
    batch["num_episodes"] = total_episodes
    batch["mean_cost_per_ep"] = total_costs / max(total_episodes, 1)
    batch["avg_ep_len"] = float(sum(len(a) for a in all_actions)) / max(total_episodes, 1)
    return batch


@eqx.filter_jit
def grpo_step(policy, tokens, actions, old_lp, advantages, clip_coef, ent_coef):
    def loss_fn(model):
        def single(tok, act, olp, adv):
            logits = model(tok)
            lp = jax.nn.log_softmax(logits)[act]
            logratio = lp - olp
            ratio = jnp.exp(logratio)
            pg1 = -adv * ratio
            pg2 = -adv * jnp.clip(ratio, 1.0 - clip_coef, 1.0 + clip_coef)
            pg_loss = jnp.maximum(pg1, pg2)
            probs = jax.nn.softmax(logits)
            entropy = -jnp.sum(probs * jnp.log(probs + 1e-8))
            approx_kl = (ratio - 1.0) - logratio
            return pg_loss, entropy, approx_kl
        pg, ent, kl = jax.vmap(single)(tokens, actions, old_lp, advantages)
        loss = jnp.mean(pg) - ent_coef * jnp.mean(ent)
        return loss, jnp.mean(kl)
    (loss, approx_kl), grads = eqx.filter_value_and_grad(loss_fn, has_aux=True)(policy)
    return loss, grads, approx_kl


def save_checkpoint(policy, opt_state, step, ckpt_dir):
    eqx.tree_serialise_leaves(str(ckpt_dir / f"policy_{step}.eqx"), policy)
    eqx.tree_serialise_leaves(str(ckpt_dir / f"opt_{step}.eqx"), opt_state)
    if HAS_WANDB and wandb.run is not None:
        artifact = wandb.Artifact(f"grpo-bandit-checkpoint-{step}", type="checkpoint")
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
    return path.read_text().strip() if path.exists() else None


def train(cfg: GRPOBanditConfig):
    if cfg.advantage == "maxrl" and cfg.use_phi:
        raise ValueError("MaxRL with tactic φ is not valid — MaxRL discards failures, "
                         "φ scores failures. Use --no-phi with --advantage maxrl.")

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
    policy = AutoregressivePolicy(
        vocab_size=cfg.vocab_size, max_seq_len=cfg.max_seq_len,
        d_model=cfg.d_model, n_heads=cfg.n_heads, n_layers=cfg.n_layers,
        num_tactics=cfg.num_tactics, key=model_key,
    )
    print(f"AutoregressivePolicy (BANDIT): {count_params(policy):,} params "
          f"(advantage={cfg.advantage}, use_phi={cfg.use_phi}, "
          f"G={cfg.G}, d1={cfg.d1}, d2={cfg.d2})")

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
        phi_tag = "phi" if cfg.use_phi else "nophi"
        tag = f"{cfg.advantage}-bandit-{phi_tag}"
        if cfg.fresh:
            run_id = f"{tag}-{int(time.time())}"
            save_run_id(run_id, ckpt_dir)
        else:
            run_id = load_run_id(ckpt_dir)
            if run_id is None:
                run_id = f"{tag}-{int(time.time())}"
                save_run_id(run_id, ckpt_dir)
        wandb.init(
            project=cfg.wandb_project, name=run_id, id=run_id,
            resume="allow", config=vars(cfg),
        )

    solve_ema, cost_ema, ema_alpha = 0.0, 0.0, 0.05

    phi_tag = "phi" if cfg.use_phi else "nophi"
    desc = f"{cfg.advantage}-bandit-{phi_tag}"
    pbar = tqdm(range(start_iter, cfg.num_iterations), desc=desc,
                initial=start_iter, total=cfg.num_iterations)
    for iteration in pbar:
        key, rollout_key = jr.split(key)
        batch = collect_batch(policy, cfg, rollout_key)
        if batch is None:
            continue

        solve_ema += ema_alpha * (batch["solve_rate"] - solve_ema)
        cost_ema += ema_alpha * (batch["mean_cost_per_ep"] - cost_ema)

        # Skip gradient update if no training data (MaxRL all-degenerate)
        has_training_data = batch["tokens"] is not None
        if has_training_data:
            N = batch["tokens"].shape[0]
            if N < 2:
                has_training_data = False

        if has_training_data:
            anneal_frac = (1.0 - iteration / cfg.num_iterations) if cfg.anneal_lr else 1.0

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

                    loss, grads, kl = grpo_step(
                        policy, batch["tokens"][idx], batch["actions"][idx],
                        batch["log_probs"][idx], mb_adv,
                        cfg.clip_coef, cfg.ent_coef,
                    )
                    grads = jax.tree.map(lambda g: g * anneal_frac, grads)
                    updates, opt_state = opt.update(
                        eqx.filter(grads, eqx.is_array), opt_state,
                        eqx.filter(policy, eqx.is_array),
                    )
                    policy = eqx.apply_updates(policy, updates)

                    if cfg.target_kl is not None and float(kl) > cfg.target_kl:
                        kl_exceeded = True
                        break

        pbar.set_postfix_str(f"solve={solve_ema:.1%} cost={cost_ema:.2f}")

        if (iteration + 1) % cfg.log_every == 0:
            log = {
                "iteration": iteration + 1,
                "solve_rate": batch["solve_rate"],
                "reward/ep": batch["solve_rate"],
                "avg_ep_len": batch["avg_ep_len"],
                "mean_cost_per_ep": batch["mean_cost_per_ep"],
                "num_episodes": batch["num_episodes"],
            }
            if HAS_WANDB and wandb.run is not None:
                wandb.log(log)
            tqdm.write(
                f"  [{iteration+1:>5}] solve={batch['solve_rate']:.1%} "
                f"len={batch['avg_ep_len']:.1f} "
                f"cost/ep={batch['mean_cost_per_ep']:.2f} "
                f"eps={batch['num_episodes']}"
            )

        if (iteration + 1) % cfg.save_every == 0:
            step = iteration + 1
            save_checkpoint(policy, opt_state, step, ckpt_dir)
            tqdm.write(f"  -> checkpoint at iteration {step}")

    save_checkpoint(policy, opt_state, cfg.num_iterations, ckpt_dir)
    if HAS_WANDB and wandb.run is not None:
        wandb.finish()
    print(f"Bandit {cfg.advantage} training complete.")


def main():
    parser = argparse.ArgumentParser(description="Bandit GRPO/MaxRL for Peano tactic synthesis")
    parser.add_argument("--num-iterations", type=int, default=2000)
    parser.add_argument("--theorems-per-iter", type=int, default=16)
    parser.add_argument("--G", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--d1", type=float, default=0.0)
    parser.add_argument("--d2", type=float, default=-1.0)
    parser.add_argument("--advantage", choices=["grpo", "maxrl"], default="grpo",
                        help="Advantage method: grpo (normalize by σ) or maxrl (normalize by K)")
    parser.add_argument("--no-phi", action="store_true",
                        help="Disable tactic φ process signal (binary outcome only)")
    parser.add_argument("--n-layers", type=int, default=5)
    parser.add_argument("--d-model", type=int, default=256)
    parser.add_argument("--max-difficulty", type=int, default=8)
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    phi_tag = "phi" if not args.no_phi else "nophi"
    ckpt_dir = f"checkpoints/bandit_{args.advantage}_{phi_tag}_seed{args.seed}"

    cfg = GRPOBanditConfig(
        num_iterations=args.num_iterations,
        theorems_per_iter=args.theorems_per_iter,
        G=args.G, learning_rate=args.learning_rate,
        d1=args.d1, d2=args.d2,
        advantage=args.advantage,
        use_phi=not args.no_phi,
        n_layers=args.n_layers, d_model=args.d_model,
        max_difficulty=args.max_difficulty,
        checkpoint_dir=ckpt_dir,
        seed=args.seed,
        fresh=args.fresh,
    )
    train(cfg)


if __name__ == "__main__":
    main()