"""
proof_length_by_difficulty.py — Measure proof length as a function of difficulty d.

Generates theorems at each difficulty level and reports proof length statistics.
This produces the data for Table 3 in the paper.

Usage:
  python scripts/eval/proof_length_by_difficulty.py
"""

import random
from peano_player.gen import generate_one


def main():
    trials_per_d = 500
    max_d = 12  # extend beyond 8 if you want to see further scaling

    print(f"{'d':>3}  {'n':>4}  {'min':>4}  {'median':>6}  {'mean':>6}  {'max':>4}")
    for d in range(1, max_d + 1):
        lengths = []
        for seed in range(trials_per_d):
            random.seed(seed)
            thm = generate_one(
                name=f"t{seed}", difficulty=d,
                both_sides=random.random() < 0.35,
            )
            if thm is not None:
                lengths.append(len(thm.tactics))

        if not lengths:
            print(f"{d:3d}  {'—':>4}")
            continue

        lengths.sort()
        median = lengths[len(lengths) // 2]
        mean = sum(lengths) / len(lengths)
        print(f"{d:3d}  {len(lengths):4d}  {min(lengths):4d}  {median:6d}  {mean:6.1f}  {max(lengths):4d}")


if __name__ == "__main__":
    main()