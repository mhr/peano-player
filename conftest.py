"""Make the package and the training scripts importable during tests.

This lets ``pytest`` run from a fresh checkout without ``pip install -e .``:
it adds ``src/`` (for ``import peano_player``) and ``scripts/train/`` (for the
training modules the tests exercise directly) to ``sys.path``.
"""
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent
for _p in (_ROOT / "src", _ROOT / "scripts" / "train"):
    _p = str(_p)
    if _p not in sys.path:
        sys.path.insert(0, _p)
