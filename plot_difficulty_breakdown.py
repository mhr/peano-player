"""
plot_difficulty_breakdown.py — Four-line plot of solve rate vs. difficulty.

Reads JSON files produced by eval_by_difficulty.py, groups by condition,
computes mean ± stderr across seeds, and plots four lines with shaded bands.

Expected directory structure:
  results/
    gcpo_seed0.json
    gcpo_seed1.json
    ...
    ppo_cost_seed0.json      (PPO λ=1, your CMDP)
    ppo_sparse_seed0.json    (PPO λ=0, ablation)
    grpo_sparse_seed0.json   (GRPO baseline)
    grpo_cost_seed0.json     (GRPO + Kim & Yun)

Usage:
  python plot_difficulty_breakdown.py --results-dir results/ --output figures/difficulty_breakdown.pdf
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Condition definitions: (glob prefix, display label, color)

# CONDITIONS = [
#     ("ppo_cost",    "Peano Player",          "#2e75b6", "o"),
#     ("ppo_sparse",  "MDP (reward only)",     "#5b9bd5", "s"),
#     ("grpo_cost",   "Bandit + feedback",     "#e07b39", "^"),
#     ("grpo_sparse", "Bandit",                "#888888", "D"),
# ]

CONDITIONS = [
    ("mdp_cost", "Peano Player", "#1f77b4", "o"),
    ("mdp_sparse", "Multi-Step (reward only)", "#ff7f0e", "s"),
    ("bandit_cost", "Bandit + cost", "#2ca02c", "^"),
    ("bandit_sparse", "Bandit", "#d62728", "D"),
]


def load_condition(results_dir, prefix):
    """Load all seed files matching prefix, return array of shape (n_seeds, n_difficulties)."""
    files = sorted(results_dir.glob(f"{prefix}_seed*.json"))
    if not files:
        return None, None

    all_rates = []
    difficulties = None

    for f in files:
        with open(f) as fp:
            data = json.load(fp)
        by_d = data["results_by_difficulty"]
        ds = sorted(by_d.keys(), key=int)
        rates = [by_d[d]["solve_rate"] for d in ds]
        all_rates.append(rates)
        if difficulties is None:
            difficulties = [int(d) for d in ds]

    return np.array(all_rates), np.array(difficulties)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=str, default="results",
                        help="Directory containing eval JSON files")
    parser.add_argument("--output", type=str, default="figures/difficulty_breakdown.pdf",
                        help="Output figure path")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # fig, ax = plt.subplots(figsize=(5, 3.5))
    plt.rcParams.update({
        "font.family": "serif",
        # "font.serif": ["Times", "Times New Roman", "STIX"],
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "lines.linewidth": 1.2,
        "lines.markersize": 3.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    fig, ax = plt.subplots(figsize=(7, 3.5))

    for prefix, label, color, marker in CONDITIONS:
        rates, difficulties = load_condition(results_dir, prefix)
        if rates is None:
            print(f"  No files found for prefix '{prefix}', skipping.")
            continue

        n_seeds = rates.shape[0]
        mean = rates.mean(axis=0) * 100
        stderr = rates.std(axis=0, ddof=1) / np.sqrt(n_seeds) * 100

        ax.plot(difficulties, mean, marker=marker, markersize=4, label=label,
                color=color, linewidth=1.5)
        ax.fill_between(difficulties, mean - stderr, mean + stderr,
                        alpha=0.2, color=color)

    ax.set_xlabel("Difficulty $d$")
    ax.set_ylabel("Solve rate (%)")
    ax.set_xticks(range(1, 9))
    ax.set_ylim(0.0, 105.0)
    ax.set_yticks(range(0, 101, 10))
    # ax.legend(fontsize=8, loc="lower left")
    ax.legend(fontsize=7, bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    print(f"Saved figure to {output_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
