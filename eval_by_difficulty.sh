#!/bin/bash
TRIALS=200
EVAL_SEED=9999

for seed in 0 1 2 3 4; do
  # MDP, cost (CMDP)
  python eval_by_difficulty.py --model ppo \
    --checkpoint checkpoints/ppo_baseline_lambda1.0_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/mdp_cost_seed${seed}.json

  # MDP, sparse
  python eval_by_difficulty.py --model ppo \
    --checkpoint checkpoints/ppo_baseline_lambda0.0_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/mdp_sparse_seed${seed}.json

  # Bandit, cost
  python eval_by_difficulty.py --model bandit \
    --checkpoint checkpoints/bandit_grpo_phi_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/bandit_cost_seed${seed}.json

  # Bandit, sparse
  python eval_by_difficulty.py --model bandit \
    --checkpoint checkpoints/bandit_grpo_nophi_seed${seed}/policy_2000.eqx \
    --trials $TRIALS --seed $EVAL_SEED --output results/bandit_sparse_seed${seed}.json
done