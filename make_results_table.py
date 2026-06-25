"""
make_results_table.py — Aggregate held-out evaluation table.

Reads JSON files produced by eval_by_difficulty.py and reports:
  - overall solve rate across difficulties
  - tactic failure rate across executed tactic steps
  - d=8 solve rate in plain summary only

Usage:
  python make_results_table.py --results-dir results
"""

import argparse
import json
from pathlib import Path

import numpy as np


CONDITIONS = [
    ("mdp_cost", "Peano Player"),
    ("mdp_sparse", "Multi-Step (reward only)"),
    ("bandit_cost", "Bandit + cost"),
    ("bandit_sparse", "Bandit"),
]


def stderr(values):
    values = np.asarray(values, dtype=float)
    if len(values) <= 1:
        return 0.0
    return values.std(ddof=1) / np.sqrt(len(values))


def load_json(path):
    with open(path) as f:
        return json.load(f)


def aggregate_one_seed(data):
    by_difficulty = data["results_by_difficulty"]

    total_solved = 0
    total_trials = 0
    total_failure_steps = 0.0
    total_executed_steps = 0.0

    for row in by_difficulty.values():
        total_solved += row["solved"]
        total_trials += row["trials"]

        if "total_tactic_failures" in row and "total_steps" in row:
            total_failure_steps += row["total_tactic_failures"]
            total_executed_steps += row["total_steps"]
        else:
            executed_steps = row["mean_steps"] * row["trials"]
            total_failure_steps += row["tactic_failure_rate"] * executed_steps
            total_executed_steps += executed_steps

    overall_solve = total_solved / total_trials
    overall_failure = (
        total_failure_steps / total_executed_steps
        if total_executed_steps > 0
        else 0.0
    )
    d8_solve = by_difficulty["8"]["solve_rate"]

    return {
        "overall_solve": overall_solve,
        "overall_failure": overall_failure,
        "d8_solve": d8_solve,
    }


def summarize_condition(results_dir, prefix):
    files = sorted(results_dir.glob(f"{prefix}_seed*.json"))
    if not files:
        raise FileNotFoundError(f"No files found for prefix {prefix!r}")

    per_seed = [aggregate_one_seed(load_json(path)) for path in files]

    summary = {}
    for metric in ["overall_solve", "overall_failure", "d8_solve"]:
        values = np.array([row[metric] for row in per_seed], dtype=float)
        summary[metric] = {
            "mean": values.mean(),
            "sem": stderr(values),
            "n": len(values),
        }

    return summary


def fmt_percent(mean, sem, decimals=1):
    return f"{100.0 * mean:.{decimals}f} $\\pm$ {100.0 * sem:.{decimals}f}"


def latex_emphasize(text, rank):
    if rank == 0:
        return f"\\textbf{{{text}}}"
    if rank == 1:
        return f"\\underline{{{text}}}"
    return text


def ranks_for_metric(summaries, metric, higher_is_better):
    values = np.array([metrics[metric]["mean"] for _, metrics in summaries], dtype=float)
    order = np.argsort(values)

    if higher_is_better:
        order = order[::-1]

    ranks = {}
    for rank, idx in enumerate(order):
        ranks[idx] = rank

    return ranks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=str, default="results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)

    summaries = []
    for prefix, label in CONDITIONS:
        metrics = summarize_condition(results_dir, prefix)
        summaries.append((label, metrics))

    solve_ranks = ranks_for_metric(
        summaries=summaries,
        metric="overall_solve",
        higher_is_better=True,
    )
    failure_ranks = ranks_for_metric(
        summaries=summaries,
        metric="overall_failure",
        higher_is_better=False,
    )

    print("\nLaTeX table:\n")
    print(r"\begin{table}[t]")
    print(r"\centering")
    print(r"\begin{tabular}{@{}lcc@{}}")
    print(r"\toprule")
    print(r"Condition & Solve (\%) & Failure (\%) \\")
    print(r"\midrule")

    for idx, (label, metrics) in enumerate(summaries):
        solve = fmt_percent(
            metrics["overall_solve"]["mean"],
            metrics["overall_solve"]["sem"],
            decimals=1,
        )
        failure = fmt_percent(
            metrics["overall_failure"]["mean"],
            metrics["overall_failure"]["sem"],
            decimals=2,
        )

        solve = latex_emphasize(solve, solve_ranks[idx])
        failure = latex_emphasize(failure, failure_ranks[idx])

        print(f"{label} & {solve} & {failure} \\\\")

    print(r"\bottomrule")
    print(r"\end{tabular}")
    print(
        r"\caption{Held-out evaluation at convergence, averaged over 5 seeds. "
        r"Solve rate is aggregated across difficulties. Failure rate is the "
        r"fraction of executed tactic steps that fail.}"
    )
    print(r"\label{tab:main-results}")
    print(r"\end{table}")

    print("\nPlain summary:\n")
    for label, metrics in summaries:
        solve = fmt_percent(
            metrics["overall_solve"]["mean"],
            metrics["overall_solve"]["sem"],
            decimals=1,
        )
        failure = fmt_percent(
            metrics["overall_failure"]["mean"],
            metrics["overall_failure"]["sem"],
            decimals=2,
        )
        d8 = fmt_percent(
            metrics["d8_solve"]["mean"],
            metrics["d8_solve"]["sem"],
            decimals=1,
        )

        print(label)
        print(f"  solve:   {solve}")
        print(f"  failure: {failure}")
        print(f"  d=8:     {d8}")


if __name__ == "__main__":
    main()