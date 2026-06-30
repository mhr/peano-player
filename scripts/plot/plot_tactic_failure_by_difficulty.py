"""
plot_tactic_failure_by_difficulty.py — Tactic failure rate vs. difficulty.

Reads JSON files produced by eval_by_difficulty.py, groups by condition,
computes mean ± sample standard error across seeds, and plots four lines
with shaded bands.

Usage:
  python scripts/plot/plot_tactic_failure_by_difficulty.py \
      --results-dir results/ \
      --output figures/tactic_failure_by_difficulty.pdf
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CONDITIONS = [
    ("mdp_cost", "Peano Player", "#1f77b4", "o"),
    ("mdp_sparse", "Multi-Step (reward only)", "#ff7f0e", "s"),
    ("bandit_cost", "Bandit + cost", "#2ca02c", "^"),
    ("bandit_sparse", "Bandit", "#d62728", "D"),
]


def load_condition_metric(results_dir, prefix, metric):
    """Load metric for all seed files matching prefix.

    Returns:
        values: array of shape (n_seeds, n_difficulties)
        difficulties: array of difficulty values
    """
    files = sorted(results_dir.glob(f"{prefix}_seed*.json"))
    if not files:
        return None, None

    all_values = []
    difficulties = None

    for path in files:
        with open(path) as fp:
            data = json.load(fp)

        by_difficulty = data["results_by_difficulty"]
        difficulty_keys = sorted(by_difficulty.keys(), key=int)

        values = [by_difficulty[d][metric] for d in difficulty_keys]
        all_values.append(values)

        if difficulties is None:
            difficulties = [int(d) for d in difficulty_keys]

    return np.array(all_values, dtype=float), np.array(difficulties, dtype=int)


def apply_style():
    plt.rcParams.update({
        "font.family": "serif",
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="Directory containing eval JSON files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="figures/tactic_failure_by_difficulty.pdf",
        help="Output figure path",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    apply_style()
    fig, ax = plt.subplots(figsize=(7, 3.5))

    max_upper = 0.0

    for prefix, label, color, marker in CONDITIONS:
        values, difficulties = load_condition_metric(
            results_dir=results_dir,
            prefix=prefix,
            metric="tactic_failure_rate",
        )

        if values is None:
            print(f"No files found for prefix '{prefix}', skipping.")
            continue

        n_seeds = values.shape[0]
        mean = values.mean(axis=0) * 100.0

        if n_seeds > 1:
            stderr = values.std(axis=0, ddof=1) / np.sqrt(n_seeds) * 100.0
        else:
            stderr = np.zeros_like(mean)

        max_upper = max(max_upper, float(np.max(mean + stderr)))

        ax.plot(
            difficulties,
            mean,
            marker=marker,
            markersize=4,
            label=label,
            color=color,
            linewidth=1.5,
        )
        ax.fill_between(
            difficulties,
            mean - stderr,
            mean + stderr,
            alpha=0.2,
            color=color,
        )

    ax.set_xlabel("Difficulty $d$")
    ax.set_ylabel("Tactic failure rate (%)")
    ax.set_xticks(range(1, 9))
    ax.set_ylim(0.0, max(5.0, 1.15 * max_upper))
    ax.legend(
        fontsize=7,
        bbox_to_anchor=(1.02, 0.5),
        loc="center left",
        borderaxespad=0,
    )
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    print(f"Saved figure to {output_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()