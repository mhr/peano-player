import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import wandb


ENTITY = "mhr2145"
PROJECT = "peano-player"

OUT_DIR = pathlib.Path("figures")
OUT_DIR.mkdir(exist_ok=True)

EXPORT_DIR = pathlib.Path("wandb_export")
EXPORT_DIR.mkdir(exist_ok=True)

KEYS = [
    "iteration",
    "solve_rate",
    "mean_cost_per_ep",
    "avg_ep_len",
    "num_episodes",
]

INCLUDE_RUN_IDS = {
    # Multi-step sparse, lambda = 0
    "ppo-baseline-lambda0.0-1779528928",
    "ppo-baseline-lambda0.0-1779532122",
    "ppo-baseline-lambda0.0-1779535397",
    "ppo-baseline-lambda0.0-1779538685",
    "ppo-baseline-lambda0.0-1779542256",

    # Multi-step cost, lambda = 1
    "ppo-baseline-lambda1.0-1779528945",
    "ppo-baseline-lambda1.0-1779532284",
    "ppo-baseline-lambda1.0-1779535662",
    "ppo-baseline-lambda1.0-1779539007",
    "ppo-baseline-lambda1.0-1779542640",

    # Bandit sparse, no phi
    "grpo-bandit-nophi-1779528950",
    "grpo-bandit-nophi-1779546827",
    "grpo-bandit-nophi-1779561644",
    "grpo-bandit-nophi-1779575782",
    "grpo-bandit-nophi-1779594023",

    # Bandit cost, phi
    "grpo-bandit-phi-1779528956",
    "grpo-bandit-phi-1779542340",
    "grpo-bandit-phi-1779554282",
    "grpo-bandit-phi-1779572775",
    "grpo-bandit-phi-1779584307",
}

CONDITION_ORDER = [
    "multistep_cost",
    "multistep_sparse",
    "bandit_cost",
    "bandit_sparse"
]

CONDITION_LABELS = {
    "multistep_cost": "Peano Player",
    "multistep_sparse": "Multi-Step (reward only)",
    "bandit_cost": "Bandit + cost",
    "bandit_sparse": "Bandit"
}

CONDITION_COLORS = {
    "multistep_cost":   "#E23145",  # Peano Player — crimson
    "multistep_sparse": "#FF7F0E",  # Multi-Step (reward only) — orange
    "bandit_cost":      "#2CA02C",  # Bandit + cost — green
    "bandit_sparse":    "#1F77B4",  # Bandit — blue
}

SMOOTH_BETA = 0.95


def apply_style():
    plt.rcParams.update({
        # "font.family": "serif",
        # "font.serif": ["DejaVu Serif"],
        # "mathtext.fontset": "stix",
        
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "mathtext.fontset": "dejavusans",

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


def infer_condition(run):
    config = run.config

    if "cost_penalty" in config:
        lam = float(config.get("cost_penalty", 0.0))
        return "multistep_cost" if lam > 0.0 else "multistep_sparse"

    use_phi = bool(config.get("use_phi", False))
    return "bandit_cost" if use_phi else "bandit_sparse"


def export_wandb_runs():
    api = wandb.Api(timeout=60)
    runs = api.runs(f"{ENTITY}/{PROJECT}")

    all_rows = []

    for run in runs:
        if run.id not in INCLUDE_RUN_IDS:
            continue

        print(f"Exporting {run.name} ({run.id})")

        rows = list(run.scan_history(keys=KEYS))
        if not rows:
            print("  skipped: no matching history rows")
            continue

        df = pd.DataFrame(rows)

        if "iteration" not in df.columns or "solve_rate" not in df.columns:
            print("  skipped: missing iteration or solve_rate")
            continue

        df = df.dropna(subset=["iteration", "solve_rate"]).copy()
        if df.empty:
            print("  skipped: no non-null iteration/solve_rate rows")
            continue

        df["iteration"] = df["iteration"].astype(int)
        df["solve_rate"] = df["solve_rate"].astype(float)

        df["run_id"] = run.id
        df["run_name"] = run.name
        df["seed"] = run.config.get("seed")
        df["condition"] = infer_condition(run)

        all_rows.append(df)

    if not all_rows:
        raise RuntimeError("No runs were exported. Check INCLUDE_RUN_IDS.")

    full = pd.concat(all_rows, ignore_index=True)

    full.to_csv(EXPORT_DIR / "training_runs.csv", index=False)
    full.to_parquet(EXPORT_DIR / "training_runs.parquet", index=False)

    print("\nExported runs:")
    print(
        full[["run_name", "run_id", "condition", "seed"]]
        .drop_duplicates()
        .sort_values(["condition", "seed", "run_name"])
        .to_string(index=False)
    )

    print("\nRun count per condition:")
    print(
        full[["run_id", "condition"]]
        .drop_duplicates()
        .groupby("condition")
        .size()
        .to_string()
    )

    return full


def summarize(df):
    summary = (
        df.groupby(["condition", "iteration"], as_index=False)
        .agg(
            mean_solve_rate=("solve_rate", "mean"),
            sem_solve_rate=("solve_rate", "sem"),
            n=("solve_rate", "count"),
        )
        .sort_values(["condition", "iteration"])
    )

    summary["sem_solve_rate"] = summary["sem_solve_rate"].fillna(0.0)

    alpha = 1.0 - SMOOTH_BETA

    summary["mean_smooth"] = (
        summary.groupby("condition")["mean_solve_rate"]
        .transform(lambda s: s.ewm(alpha=alpha, adjust=False).mean())
    )
    summary["sem_smooth"] = (
        summary.groupby("condition")["sem_solve_rate"]
        .transform(lambda s: s.ewm(alpha=alpha, adjust=False).mean())
    )

    summary.to_csv(EXPORT_DIR / "training_summary.csv", index=False)
    summary.to_parquet(EXPORT_DIR / "training_summary.parquet", index=False)

    print("\nNumber of runs contributing per condition/iteration:")
    print(summary.groupby("condition")["n"].describe().to_string())

    return summary


def plot_training_solve_rate(summary):
    apply_style()

    fig, ax = plt.subplots(figsize=(7, 3.5))

    for condition in CONDITION_ORDER:
        sub = summary[summary["condition"] == condition].sort_values("iteration")
        if sub.empty:
            print(f"Skipping empty condition: {condition}")
            continue

        # x = sub["iteration"].to_numpy()
        # y = sub["mean_smooth"].to_numpy()
        # e = sub["sem_smooth"].to_numpy()

        # ax.plot(
        #     x,
        #     y,
        #     label=CONDITION_LABELS[condition],
        #     linewidth=1.5,
        # )
        # ax.fill_between(
        #     x,
        #     y - e,
        #     y + e,
        #     alpha=0.2,
        #     linewidth=0,
        # )

        x = sub["iteration"].to_numpy()
        y = sub["mean_smooth"].to_numpy()
        e = sub["sem_smooth"].to_numpy()

        color = CONDITION_COLORS[condition]
        ax.plot(
            x,
            y,
            label=CONDITION_LABELS[condition],
            linewidth=1.5,
            color=color,
        )
        ax.fill_between(
            x,
            y - e,
            y + e,
            alpha=0.2,
            linewidth=0,
            color=color,
        )

    ax.set_xlabel("Training iteration")
    ax.set_ylabel("Training solve rate (%)")
    ax.set_ylim(0.0, 1.0)
    ax.set_yticks([i / 10 for i in range(0, 11)])
    ax.set_yticklabels([str(10 * i) for i in range(0, 11)])
    ax.legend(
        fontsize=7,
        bbox_to_anchor=(1.02, 0.5),
        loc="center left",
        borderaxespad=0,
    )
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    pdf_path = OUT_DIR / "training_solve_rate.pdf"
    png_path = OUT_DIR / "training_solve_rate.png"

    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"\nWrote {pdf_path}")
    print(f"Wrote {png_path}")


def main():
    df = export_wandb_runs()
    summary = summarize(df)
    plot_training_solve_rate(summary)


if __name__ == "__main__":
    main()