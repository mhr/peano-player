"""Peano Player — RL for Lean 4 tactic synthesis over Peano arithmetic.

Core library modules:
    peano_player.gen     synthetic theorem + proof generation
    peano_player.models  policy architectures (MonolithPolicy, AutoregressivePolicy)

Training / evaluation / plotting entry points live under ``scripts/`` and
import this package; run them from the repository root.
"""

__version__ = "1.0.0"
