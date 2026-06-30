"""
eval_by_difficulty.py — Evaluate a trained Peano Player agent per difficulty level.

Loads a checkpoint, generates theorems at each difficulty d=1..D,
rolls out episodes, and writes results to a JSON file.

Usage:
  # MDP, cost (CMDP agent, λ=1):
  python scripts/eval/eval_by_difficulty.py --model ppo --checkpoint checkpoints/ppo_baseline/policy_2000.eqx \
      --trials 100 --output results/ppo_cost_seed0.json

  # MDP, sparse (reward-only ablation, λ=0):
  python scripts/eval/eval_by_difficulty.py --model ppo --checkpoint checkpoints/ppo_sparse/policy_2000.eqx \
      --trials 100 --output results/ppo_sparse_seed0.json

  # Bandit, sparse (GRPO baseline):
  python scripts/eval/eval_by_difficulty.py --model bandit --checkpoint checkpoints/grpo_sparse/policy_2000.eqx \
      --trials 100 --output results/grpo_sparse_seed0.json

  # Bandit, cost (GRPO + Kim & Yun):
  python scripts/eval/eval_by_difficulty.py --model bandit --checkpoint checkpoints/grpo_cost/policy_2000.eqx \
      --trials 100 --output results/grpo_cost_seed0.json

Full shell script:
#!/bin/bash
TRIALS=200
EVAL_SEED=9999

for seed in 0 1 2 3 4; do
  # MDP, cost (CMDP)
  python scripts/eval/eval_by_difficulty.py --model ppo \
    --checkpoint checkpoints/ppo_baseline_lambda1.0_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/mdp_cost_seed${seed}.json

  # MDP, sparse
  python scripts/eval/eval_by_difficulty.py --model ppo \
    --checkpoint checkpoints/ppo_baseline_lambda0.0_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/mdp_sparse_seed${seed}.json

  # Bandit, cost
  python scripts/eval/eval_by_difficulty.py --model bandit \
    --checkpoint checkpoints/bandit_grpo_phi_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/bandit_cost_seed${seed}.json

  # Bandit, sparse
  python scripts/eval/eval_by_difficulty.py --model bandit \
    --checkpoint checkpoints/bandit_grpo_nophi_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/bandit_sparse_seed${seed}.json
done
"""

import argparse
import json
import random
from pathlib import Path

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr
import numpy as np

from peano_player.gen import generate_one, to_lean, clone, RULES, rewrite_in_goal
from peano_player.models import MonolithPolicy, AutoregressivePolicy, SEP_TOKEN, TACTIC_OFFSET


NUM_TACTICS = 4

# ── Tokenization ──

def tokenize_goal(goal_str: str, max_len: int) -> jnp.ndarray:
    """Tokenize a goal string for the MDP agent (MonolithPolicy)."""
    raw = [min(b, 255) for b in goal_str.encode("utf-8")[:max_len]]
    padded = raw + [0] * (max_len - len(raw))
    return jnp.array(padded, dtype=jnp.int32)


def tokenize_bandit(goal_str, prev_tactic_ids, max_len, goal_max_len=256):
    """Tokenize [goal_bytes, SEP, tactic_tokens] for the bandit (AutoregressivePolicy)."""
    goal_bytes = [min(b, 249) for b in goal_str.encode("utf-8")[:goal_max_len]]
    seq = goal_bytes + [SEP_TOKEN]
    for tid in prev_tactic_ids:
        seq.append(TACTIC_OFFSET + tid)
    seq = seq[:max_len]
    padded = seq + [0] * (max_len - len(seq))
    return jnp.array(padded, dtype=jnp.int32)


# ── Environment step ──

def step_env(lhs, rhs, action):
    """Apply tactic to goal. Returns (new_lhs, new_rhs, reward, cost, done)."""
    rule = RULES[action]
    result = rewrite_in_goal(lhs, rhs, rule)
    if result is None:
        return lhs, rhs, 0.0, 1.0, True      # tactic failure
    new_lhs, new_rhs = result
    if new_lhs == new_rhs:
        return new_lhs, new_rhs, 1.0, 0.0, True  # proof closed
    return new_lhs, new_rhs, 0.0, 0.0, False     # valid, not closed


# ── MDP evaluation (per-step) ──

@eqx.filter_jit
def _forward_ppo(policy, tokens):
    logits, _ = policy.forward_with_value(tokens)
    return logits


def evaluate_mdp(policy, lhs, rhs, key, max_steps=20, max_seq_len=256):
    """Roll out one episode with per-step observation."""
    cur_lhs, cur_rhs = clone(lhs), clone(rhs)
    steps = 0
    tactic_failures = 0

    for _ in range(max_steps):
        if cur_lhs == cur_rhs:
            break

        goal_str = f"{to_lean(cur_lhs)} = {to_lean(cur_rhs)}"
        tokens = tokenize_goal(goal_str, max_seq_len)
        logits = _forward_ppo(policy, tokens)

        key, subkey = jr.split(key)
        action = int(jr.categorical(subkey, logits))

        cur_lhs, cur_rhs, reward, cost, done = step_env(cur_lhs, cur_rhs, action)
        steps += 1
        if cost > 0:
            tactic_failures += 1
        if done:
            break

    return {
        "solved": bool(cur_lhs == cur_rhs),
        "steps": steps,
        "tactic_failures": tactic_failures,
    }


# ── Bandit evaluation (generate-then-execute) ──

@eqx.filter_jit
def _forward_bandit(policy, tokens):
    return policy(tokens)


def evaluate_bandit(policy, lhs, rhs, key, max_steps=20,
                    max_seq_len=280, goal_max_len=256):
    """Generate full tactic sequence, then execute post hoc."""
    goal_str = f"{to_lean(lhs)} = {to_lean(rhs)}"

    # Phase 1: generate all tactics autoregressively
    prev_tactics = []
    all_actions = []
    for _ in range(max_steps):
        tokens = tokenize_bandit(goal_str, prev_tactics, max_seq_len, goal_max_len)
        logits = _forward_bandit(policy, tokens)

        key, subkey = jr.split(key)
        action = int(jr.categorical(subkey, logits))

        # Clamp to valid tactic range (0..3); ignore EOS for eval
        action = min(action, NUM_TACTICS - 1)

        all_actions.append(action)
        prev_tactics.append(action)

    # Phase 2: execute against environment
    exec_lhs, exec_rhs = clone(lhs), clone(rhs)
    steps_executed = 0
    tactic_failures = 0

    for a in all_actions:
        if exec_lhs == exec_rhs:
            break
        result = rewrite_in_goal(exec_lhs, exec_rhs, RULES[a])
        steps_executed += 1
        if result is None:
            tactic_failures += 1
            break
        exec_lhs, exec_rhs = result

    return {
        "solved": bool(exec_lhs == exec_rhs),
        "steps": steps_executed,
        "tactic_failures": tactic_failures,
    }


# ── Model loading ──

def load_ppo(checkpoint_path):
    key = jr.PRNGKey(0)
    policy = MonolithPolicy(
        vocab_size=256, max_seq_len=256,
        d_model=256, n_heads=4, n_layers=5, num_tactics=NUM_TACTICS,
        key=key,
    )
    policy = eqx.tree_deserialise_leaves(checkpoint_path, policy)
    return policy


def load_bandit(checkpoint_path):
    key = jr.PRNGKey(0)
    policy = AutoregressivePolicy(
        vocab_size=256, max_seq_len=280,
        d_model=256, n_heads=4, n_layers=5, num_tactics=NUM_TACTICS,
        key=key,
    )
    policy = eqx.tree_deserialise_leaves(checkpoint_path, policy)
    return policy


# ── Main ──

def main():
    parser = argparse.ArgumentParser(description="Evaluate agent per difficulty level.")
    parser.add_argument("--model", choices=["ppo", "bandit"], required=True,
                        help="Model type: ppo (MonolithPolicy) or bandit (AutoregressivePolicy)")
    parser.add_argument("--checkpoint", type=str, required=True,
                        help="Path to policy .eqx checkpoint")
    parser.add_argument("--trials", type=int, default=100,
                        help="Theorems per difficulty level (default: 100)")
    parser.add_argument("--min-difficulty", type=int, default=1)
    parser.add_argument("--max-difficulty", type=int, default=8)
    parser.add_argument("--max-steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0,
                        help="Random seed for theorem generation and action sampling")
    parser.add_argument("--output", type=str, required=True,
                        help="Output JSON path")
    args = parser.parse_args()

    if args.model == "ppo":
        policy = load_ppo(args.checkpoint)
        evaluate_fn = lambda pol, l, r, k: evaluate_mdp(
            pol, l, r, k, max_steps=args.max_steps, max_seq_len=256)
    else:
        policy = load_bandit(args.checkpoint)
        evaluate_fn = lambda pol, l, r, k: evaluate_bandit(
            pol, l, r, k, max_steps=args.max_steps, max_seq_len=280)

    print(f"Loaded {args.model} from {args.checkpoint}")

    key = jr.PRNGKey(args.seed)
    results = {}

    for d in range(args.min_difficulty, args.max_difficulty + 1):
        random.seed(args.seed * 1000 + d)

        solved_count = 0
        total_steps = 0
        total_tactic_failures = 0
        successful_proof_lengths = []
        generated = 0

        for trial in range(args.trials):
            thm = None
            for _ in range(20):
                both_sides = random.random() < 0.35
                thm = generate_one(name="eval", difficulty=d, both_sides=both_sides)
                if thm is not None:
                    break
            if thm is None:
                continue

            generated += 1
            key, subkey = jr.split(key)
            ep = evaluate_fn(policy, thm.lhs, thm.rhs, subkey)

            if ep["solved"]:
                solved_count += 1
                successful_proof_lengths.append(ep["steps"])
            total_steps += ep["steps"]
            total_tactic_failures += ep["tactic_failures"]

        solve_rate = solved_count / max(generated, 1)
        results[str(d)] = {
            "difficulty": d,
            "trials": generated,
            "solved": solved_count,
            "solve_rate": solve_rate,
            "mean_steps": total_steps / max(generated, 1),
            "mean_proof_length": (float(np.mean(successful_proof_lengths))
                                  if successful_proof_lengths else None),
            "tactic_failure_rate": total_tactic_failures / max(total_steps, 1),
        }
        print(f"  d={d}: {solved_count}/{generated} solved ({solve_rate:.1%})")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({
            "model": args.model,
            "checkpoint": args.checkpoint,
            "seed": args.seed,
            "trials_per_difficulty": args.trials,
            "results_by_difficulty": results,
        }, f, indent=2)
    print(f"Wrote results to {args.output}")


if __name__ == "__main__":
    main()
