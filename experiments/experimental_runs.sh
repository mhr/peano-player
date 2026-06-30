# ── GPU 0: MDP, sparse reward (λ=0) ──
tmux new-session -d -s ppo_l0
tmux send-keys -t ppo_l0 '
conda activate phd
for seed in 0 1 2 3 4; do
  CUDA_VISIBLE_DEVICES=0 python scripts/train/ppo_baseline_train.py \
    --cost-penalty 0.0 --seed $seed --fresh
done
'

# ── GPU 1: MDP, CMDP (λ=1) ──
tmux new-session -d -s ppo_l1
tmux send-keys -t ppo_l1 '
conda activate phd
for seed in 0 1 2 3 4; do
  CUDA_VISIBLE_DEVICES=1 python scripts/train/ppo_baseline_train.py \
    --cost-penalty 1.0 --seed $seed --fresh
done
'

# ── GPU 2: Bandit, sparse reward only ──
tmux new-session -d -s grpo_nophi
tmux send-keys -t grpo_nophi '
conda activate phd
for seed in 0 1 2 3 4; do
  CUDA_VISIBLE_DEVICES=2 python scripts/train/bandit_train.py \
    --no-phi --seed $seed --fresh
done
'

# ── GPU 3: Bandit, dense tactic feedback ──
tmux new-session -d -s grpo_phi
tmux send-keys -t grpo_phi '
conda activate phd
for seed in 0 1 2 3 4; do
  CUDA_VISIBLE_DEVICES=3 python scripts/train/bandit_train.py \
    --seed $seed --fresh
done
'