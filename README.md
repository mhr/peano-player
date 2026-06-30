# Peano Player

RL for Lean 4 tactic synthesis over Peano arithmetic.
Paper: <https://openreview.net/forum?id=LW3lsb9jA6>

## Repository layout

```
.
├── src/peano_player/      # importable core library
│   ├── gen.py             #   synthetic theorem + proof generation
│   └── models.py          #   policy architectures
├── scripts/               # command-line entry points (run from repo root)
│   ├── train/             #   bandit_train.py, ppo_baseline_train.py
│   ├── eval/              #   eval_by_difficulty.py, make_results_table.py, proof_length_by_difficulty.py
│   └── plot/              #   plot_convergence.py, plot_difficulty_breakdown.py, plot_tactic_failure_by_difficulty.py
├── experiments/           # shell drivers that reproduce the paper's runs
├── data/                  # generated dataset (peano_dataset.{jsonl,lean})
├── results/               # evaluation metrics (JSON, one file per condition/seed)
├── figures/               # generated paper figures (not version-controlled)
├── tests/                 # unit tests
├── checkpoints/           # trained model checkpoints (not version-controlled)
├── pyproject.toml
└── requirements.txt
```

## Installation

1. Install [Lean 4 + elan](https://leanprover.github.io/) (for type-checking generated proofs).
2. Install the Python package and its dependencies:

   ```bash
   pip install -e .
   ```

   Equivalently, `pip install -r requirements.txt` installs just the deps.

3. **GPU (Linux + CUDA 12; the paper's runs used this):**

   ```bash
   pip install "jax[cuda12]==0.5.0"
   ```

`pip install -e .` puts the `peano_player` package on your path so the
scripts can `import peano_player`. **Run all scripts from the repository
root** — they read and write `data/`, `results/`, `figures/`, and
`checkpoints/` using paths relative to it.

## Usage

Generate a dataset:

```bash
python -m peano_player.gen --num 500 --seed 0 \
    --out-lean data/peano_dataset.lean --out-jsonl data/peano_dataset.jsonl
```

Train:

```bash
python scripts/train/bandit_train.py --fresh --advantage grpo
python scripts/train/ppo_baseline_train.py --fresh
```

Evaluate and build the results table / figures:

```bash
python scripts/eval/eval_by_difficulty.py --model bandit \
    --checkpoint checkpoints/bandit_grpo_phi_seed0/policy_2000.eqx \
    --trials 200 --output results/bandit_cost_seed0.json
python scripts/eval/make_results_table.py --results-dir results
python scripts/plot/plot_difficulty_breakdown.py --results-dir results/ \
    --output figures/difficulty_breakdown.pdf
```

Reproduce the paper's full sweep with the drivers in `experiments/`:

```bash
bash experiments/experimental_runs.sh    # train all conditions/seeds
bash experiments/eval_by_difficulty.sh   # evaluate all checkpoints
```

## Tests

```bash
pytest
```
