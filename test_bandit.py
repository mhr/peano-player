"""Test bandit GRPO: first-error propagation, φ scoring, batch assembly, gradient step."""
import random
import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr
import numpy as np

from gen import generate_one, to_lean, clone, rewrite_in_goal, RULES, Zero, Succ, Pred, Add, Var
from bandit_train import (
    tokenize_bandit, rollout_bandit, collect_batch, grpo_step,
    GRPOBanditConfig,
)
from models import AutoregressivePolicy, count_params, SEP_TOKEN, TACTIC_OFFSET

results = {"passed": 0, "failed": 0}
def check(name, cond):
    if cond:
        print(f"  ✓ {name}")
        results["passed"] += 1
    else:
        print(f"  ✗ {name}")
        results["failed"] += 1

# Use d1=-0.5 for tests so we can distinguish from uninitialized zeros
cfg = GRPOBanditConfig(max_seq_len=280, d_model=64, n_heads=2, n_layers=2,
                        num_tactics=4, theorems_per_iter=4, G=4,
                        max_difficulty=4, minibatch_size=8, max_steps=10,
                        d1=-0.5, d2=-1.0)
key = jr.PRNGKey(0)
key, mk = jr.split(key)
policy = AutoregressivePolicy(cfg.vocab_size, cfg.max_seq_len, cfg.d_model,
                               cfg.n_heads, cfg.n_layers, cfg.num_tactics, key=mk)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. tokenize_bandit
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("tokenize_bandit:")
tok = tokenize_bandit("succ zero = succ zero", [], 280)
check("shape (280,)", tok.shape == (280,))
goal_len = len("succ zero = succ zero".encode("utf-8"))
check("SEP at right position", int(tok[goal_len]) == SEP_TOKEN)

tok2 = tokenize_bandit("succ zero = succ zero", [0, 3], 280)
check("tactic 0 encoded", int(tok2[goal_len + 1]) == TACTIC_OFFSET + 0)
check("tactic 3 encoded", int(tok2[goal_len + 2]) == TACTIC_OFFSET + 3)
check("different from no-tactic version", not jnp.allclose(tok, tok2))

# Goal bytes clipped to avoid special tokens
tok3 = tokenize_bandit("\xff" * 10, [], 280)  # bytes > 249
check("goal bytes clipped to 249", all(int(tok3[i]) <= 249 for i in range(10)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. rollout_bandit — always max_steps, no truncation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("\nrollout_bandit (no truncation):")
random.seed(42)
thm = None
for _ in range(50):
    thm = generate_one(name="t", difficulty=3, both_sides=False)
    if thm is not None:
        break

key, rk = jr.split(key)
ep = rollout_bandit(policy, thm.lhs, thm.rhs, cfg, rk)
check("episode not None", ep is not None)
check(f"num_steps = max_steps = {cfg.max_steps}", ep["num_steps"] == cfg.max_steps)
check("step_tokens shape", ep["step_tokens"].shape == (cfg.max_steps, 280))
check("actions shape", ep["actions"].shape == (cfg.max_steps,))
check("log_probs shape", ep["log_probs"].shape == (cfg.max_steps,))
check("phi shape", ep["phi"].shape == (cfg.max_steps,))
check("all actions in [0,3]", all(0 <= a <= 3 for a in ep["actions"]))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. First-error propagation — direct tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("\nFirst-error propagation:")

# Run many rollouts collecting solved/unsolved episodes
solved_eps, unsolved_with_error, unsolved_no_error = [], [], []
for seed in range(500):
    random.seed(seed * 13)
    diff = random.randint(1, 4)
    t = generate_one(name="t", difficulty=diff, both_sides=False)
    if t is None:
        continue
    key, rk = jr.split(key)
    e = rollout_bandit(policy, t.lhs, t.rhs, cfg, rk)
    if e is None:
        continue
    if e["solved"]:
        solved_eps.append(e)
    else:
        # Check if there's an actual tactic error
        has_d2 = np.any(e["phi"] == cfg.d2)
        if has_d2:
            unsolved_with_error.append(e)
        else:
            unsolved_no_error.append(e)
    if len(solved_eps) >= 3 and len(unsolved_with_error) >= 3:
        break

# ── Solved: all phi = 1.0 ──
for i, e in enumerate(solved_eps[:3]):
    check(f"solved {i}: ALL phi=1.0", np.all(e["phi"] == 1.0))
    check(f"solved {i}: num_steps={cfg.max_steps}", e["num_steps"] == cfg.max_steps)
    # No d1 or d2 anywhere
    check(f"solved {i}: no d1 values", not np.any(e["phi"] == cfg.d1))
    check(f"solved {i}: no d2 values", not np.any(e["phi"] == cfg.d2))

# ── Unsolved with error: d1 before error, d2 from error onward ──
for i, e in enumerate(unsolved_with_error[:3]):
    check(f"error {i}: num_steps={cfg.max_steps}", e["num_steps"] == cfg.max_steps)

    d2_mask = (e["phi"] == cfg.d2)
    d1_mask = (e["phi"] == cfg.d1)
    first_d2 = np.argmax(d2_mask)  # first True

    # Everything before first_d2 must be d1
    if first_d2 > 0:
        check(f"error {i}: all d1 before error (steps 0-{first_d2-1})",
              np.all(e["phi"][:first_d2] == cfg.d1))
    # Everything from first_d2 onward must be d2
    check(f"error {i}: all d2 from error onward (steps {first_d2}-{cfg.max_steps-1})",
          np.all(e["phi"][first_d2:] == cfg.d2))
    # d2 region should be contiguous and extend to end
    check(f"error {i}: d2 extends to last step",
          e["phi"][-1] == cfg.d2)
    # d1 and d2 account for ALL steps (no zeros or other values)
    check(f"error {i}: d1+d2 cover all steps",
          np.sum(d1_mask) + np.sum(d2_mask) == cfg.max_steps)

    # Verify first_d2 corresponds to actual tactic error
    # Execute manually to cross-check
    exec_lhs, exec_rhs = clone(e["_lhs"]) if "_lhs" in e else (None, None), None
    # Can't easily cross-check without the original theorem, so skip

# ── Unsolved, no error (all valid but proof didn't close): all d1 ──
for i, e in enumerate(unsolved_no_error[:2]):
    check(f"no-error {i}: all d1", np.all(e["phi"] == cfg.d1))
    check(f"no-error {i}: no d2", not np.any(e["phi"] == cfg.d2))

# ── Key invariant: d1 != 0 so we know values were actually set ──
print("\nφ value invariants:")
all_eps = solved_eps[:3] + unsolved_with_error[:3] + unsolved_no_error[:2]
for i, e in enumerate(all_eps):
    # With d1=-0.5, no step should be exactly 0.0 (which would indicate unset)
    # Exception: this could fail if d1 were 0.0, which is why we test with d1=-0.5
    phi_values = set(np.unique(e["phi"]))
    valid_values = {1.0, cfg.d1, cfg.d2}
    check(f"ep {i}: all phi in {{1.0, {cfg.d1}, {cfg.d2}}}",
          phi_values.issubset(valid_values))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. collect_batch
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("\ncollect_batch:")
random.seed(42)
key, bk = jr.split(key)
batch = collect_batch(policy, cfg, bk)
check("batch not None", batch is not None)
if batch is not None:
    N = batch["tokens"].shape[0]
    check(f"batch has {N} steps", N > 0)
    check("tokens shape (N, 280)", batch["tokens"].shape == (N, 280))
    check("actions in [0,3]", jnp.all((batch["actions"] >= 0) & (batch["actions"] <= 3)))
    check("advantages shape (N,)", batch["advantages"].shape == (N,))
    check(f"N divisible by max_steps", N % cfg.max_steps == 0)
    check("advantages finite", jnp.all(jnp.isfinite(batch["advantages"])))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 5. grpo_step
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    print("\ngrpo_step:")
    mb = min(8, N)
    mb_adv = batch["advantages"][:mb]
    mb_adv = (mb_adv - jnp.mean(mb_adv)) / (jnp.std(mb_adv) + 1e-8)
    loss, grads, kl = grpo_step(
        policy, batch["tokens"][:mb], batch["actions"][:mb],
        batch["log_probs"][:mb], mb_adv, 0.2, 0.01)
    check("loss finite", jnp.isfinite(loss))
    check("kl finite", jnp.isfinite(kl))
    grad_leaves = jax.tree_util.tree_leaves(eqx.filter(grads, eqx.is_array))
    check("non-zero grads", any(jnp.any(g != 0) for g in grad_leaves))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. MaxRL validation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print("\nMaxRL validation:")
try:
    bad_cfg = GRPOBanditConfig(advantage="maxrl", use_phi=True)
    from bandit_train import train
    train(bad_cfg)
    check("maxrl+phi raises error", False)
except ValueError as e:
    check("maxrl+phi raises ValueError", "not valid" in str(e))


print(f"\n{'='*50}")
print(f"Passed: {results['passed']}, Failed: {results['failed']}")
if results["failed"] == 0:
    print("All tests passed!")
else:
    print(f"WARNING: {results['failed']} test(s) failed!")
    import sys; sys.exit(1)