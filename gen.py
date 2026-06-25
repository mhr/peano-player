"""
Synthetic Peano Arithmetic Theorem + Tactic Proof Generator for Lean 4.

Generates equational theorems over a custom PNat type (zero, succ, pred, add)
with multi-step rewrite proofs. Designed for training language models on tactic
prediction — proofs use explicit `rw` steps (not `simp`/`omega`/`decide`).

Tactic vocabulary (intentionally minimal):
  - rw [pred_succ]  : pred (succ n) = n
  - rw [pred_zero]  : pred zero = zero
  - rw [add_zero]   : add n zero = n
  - rw [add_succ]   : add n (succ m) = succ (add n m)

Strategy:
  1. Generate a random normal-form expression (no reducible redexes).
  2. "Complicate" it by inserting redexes (inverse rewrites).
  3. For both-sides theorems, complicate the same normal form differently
     for LHS and RHS.
  4. Simulate Lean 4's `rw` tactic (leftmost-outermost matching) to find
     a valid proof as a sequence of tactic steps.

Output:
  - A .lean file (self-contained, type-checkable in Lean 4)
  - A .jsonl file (one JSON object per theorem, for ML training)

Usage:
  python gen.py --num 500 --seed 0 --out-lean dataset.lean --out-jsonl dataset.jsonl
"""

import random
import json
import argparse
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Set


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Expr:
    """Base class for PNat expressions."""
    pass

class Zero(Expr):
    def __eq__(self, other): return isinstance(other, Zero)
    def __hash__(self): return hash("Zero")
    def __repr__(self): return "Zero()"

class Succ(Expr):
    __slots__ = ["inner"]
    def __init__(self, inner: Expr):
        self.inner = inner
    def __eq__(self, other):
        return isinstance(other, Succ) and self.inner == other.inner
    def __hash__(self): return hash(("Succ", self.inner))
    def __repr__(self): return f"Succ({self.inner!r})"

class Pred(Expr):
    __slots__ = ["inner"]
    def __init__(self, inner: Expr):
        self.inner = inner
    def __eq__(self, other):
        return isinstance(other, Pred) and self.inner == other.inner
    def __hash__(self): return hash(("Pred", self.inner))
    def __repr__(self): return f"Pred({self.inner!r})"

class Var(Expr):
    __slots__ = ["name"]
    def __init__(self, name: str):
        self.name = name
    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name
    def __hash__(self): return hash(("Var", self.name))
    def __repr__(self): return f"Var({self.name!r})"

class Add(Expr):
    __slots__ = ["left", "right"]
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
    def __eq__(self, other):
        return isinstance(other, Add) and self.left == other.left and self.right == other.right
    def __hash__(self): return hash(("Add", self.left, self.right))
    def __repr__(self): return f"Add({self.left!r}, {self.right!r})"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pretty printing (Lean 4 syntax, assuming `open PNat`)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _needs_parens(expr: Expr) -> bool:
    """Does this subexpression need parentheses when used as an argument?"""
    return isinstance(expr, (Succ, Pred, Add))

def to_lean(expr: Expr) -> str:
    """Render an expression as Lean 4 syntax."""
    if isinstance(expr, Zero):
        return "zero"
    elif isinstance(expr, Var):
        return expr.name
    elif isinstance(expr, Succ):
        inner = to_lean(expr.inner)
        return f"succ ({inner})" if _needs_parens(expr.inner) else f"succ {inner}"
    elif isinstance(expr, Pred):
        inner = to_lean(expr.inner)
        return f"pred ({inner})" if _needs_parens(expr.inner) else f"pred {inner}"
    elif isinstance(expr, Add):
        l = to_lean(expr.left)
        r = to_lean(expr.right)
        lp = f"({l})" if _needs_parens(expr.left) else l
        rp = f"({r})" if _needs_parens(expr.right) else r
        return f"add {lp} {rp}"
    raise ValueError(f"Unknown expression type: {type(expr)}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Expression utilities
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def depth(expr: Expr) -> int:
    if isinstance(expr, (Zero, Var)):
        return 0
    if isinstance(expr, (Succ, Pred)):
        return 1 + depth(expr.inner)
    if isinstance(expr, Add):
        return 1 + max(depth(expr.left), depth(expr.right))
    raise ValueError

def size(expr: Expr) -> int:
    if isinstance(expr, (Zero, Var)):
        return 1
    if isinstance(expr, (Succ, Pred)):
        return 1 + size(expr.inner)
    if isinstance(expr, Add):
        return 1 + size(expr.left) + size(expr.right)
    raise ValueError

def free_vars(expr: Expr) -> Set[str]:
    if isinstance(expr, Zero):
        return set()
    if isinstance(expr, Var):
        return {expr.name}
    if isinstance(expr, (Succ, Pred)):
        return free_vars(expr.inner)
    if isinstance(expr, Add):
        return free_vars(expr.left) | free_vars(expr.right)
    raise ValueError

def clone(expr: Expr) -> Expr:
    """Deep copy an expression tree."""
    if isinstance(expr, Zero):
        return Zero()
    if isinstance(expr, Var):
        return Var(expr.name)
    if isinstance(expr, Succ):
        return Succ(clone(expr.inner))
    if isinstance(expr, Pred):
        return Pred(clone(expr.inner))
    if isinstance(expr, Add):
        return Add(clone(expr.left), clone(expr.right))
    raise ValueError


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Rewrite rules — simulating Lean 4's `rw` tactic
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Lean's `rw [h]` finds the FIRST (leftmost-outermost) subterm matching
# the LHS of h, and replaces it with the RHS.  We simulate this exactly.

def _match_pred_succ(e):
    """pred (succ ?n) → ?n"""
    if isinstance(e, Pred) and isinstance(e.inner, Succ):
        return {"n": e.inner.inner}
    return None

def _result_pred_succ(b):
    return clone(b["n"])

def _match_pred_zero(e):
    """pred zero → zero"""
    if isinstance(e, Pred) and isinstance(e.inner, Zero):
        return {}
    return None

def _result_pred_zero(_b):
    return Zero()

def _match_add_zero(e):
    """add ?n zero → ?n"""
    if isinstance(e, Add) and isinstance(e.right, Zero):
        return {"n": e.left}
    return None

def _result_add_zero(b):
    return clone(b["n"])

def _match_add_succ(e):
    """add ?n (succ ?m) → succ (add ?n ?m)"""
    if isinstance(e, Add) and isinstance(e.right, Succ):
        return {"n": e.left, "m": e.right.inner}
    return None

def _result_add_succ(b):
    return Succ(Add(clone(b["n"]), clone(b["m"])))


class RewriteRule:
    """A named rewrite rule with pattern matching."""
    def __init__(self, lean_name: str, match_fn, result_fn):
        self.lean_name = lean_name
        self.match_fn = match_fn
        self.result_fn = result_fn

    def try_at_root(self, expr: Expr) -> Optional[Expr]:
        """Try to match and rewrite at the root of expr."""
        bindings = self.match_fn(expr)
        if bindings is not None:
            return self.result_fn(bindings)
        return None


RULES = [
    RewriteRule("pred_succ", _match_pred_succ, _result_pred_succ),
    RewriteRule("pred_zero", _match_pred_zero, _result_pred_zero),
    RewriteRule("add_zero",  _match_add_zero,  _result_add_zero),
    RewriteRule("add_succ",  _match_add_succ,  _result_add_succ),
]


TACTIC_TO_IDX = {
    "rw [pred_succ]": 0,
    "rw [pred_zero]": 1,
    "rw [add_zero]":  2,
    "rw [add_succ]":  3,
}


def find_first_match(expr: Expr, rule: RewriteRule
                     ) -> Optional[Tuple[Expr, Expr]]:
    """
    Find the first (leftmost-outermost) subterm matching rule.
    Returns (matched_subterm, replacement) or None.
    """
    bindings = rule.match_fn(expr)
    if bindings is not None:
        return (clone(expr), rule.result_fn(bindings))
    if isinstance(expr, (Succ, Pred)):
        return find_first_match(expr.inner, rule)
    elif isinstance(expr, Add):
        m = find_first_match(expr.left, rule)
        if m is not None:
            return m
        return find_first_match(expr.right, rule)
    return None


def replace_all(expr: Expr, old: Expr, new: Expr) -> Expr:
    """
    Replace ALL occurrences of `old` in `expr` with `new`.
    When a match is found, the entire subtree is replaced (no recursion
    into children of the match), mirroring Lean's kabstract behavior.
    """
    if expr == old:
        return clone(new)
    if isinstance(expr, Zero):
        return Zero()
    if isinstance(expr, Var):
        return Var(expr.name)
    if isinstance(expr, Succ):
        return Succ(replace_all(expr.inner, old, new))
    if isinstance(expr, Pred):
        return Pred(replace_all(expr.inner, old, new))
    if isinstance(expr, Add):
        return Add(replace_all(expr.left, old, new),
                   replace_all(expr.right, old, new))
    raise ValueError


def rewrite_in_goal(lhs: Expr, rhs: Expr, rule: RewriteRule
                    ) -> Optional[Tuple[Expr, Expr]]:
    """
    Apply one `rw [rule]` step to the goal  lhs = rhs.

    Simulates Lean 4's rw tactic:
      1. Find the FIRST (leftmost-outermost) match in the whole goal
         (LHS searched before RHS).
      2. Replace ALL occurrences of that concrete matched subterm
         throughout the entire goal (both LHS and RHS).

    Returns (new_lhs, new_rhs) or None.
    """
    # Search LHS first, then RHS, for the first match
    match = find_first_match(lhs, rule)
    if match is None:
        match = find_first_match(rhs, rule)
    if match is None:
        return None
    old_sub, new_sub = match
    # Replace ALL occurrences in the entire goal
    new_lhs = replace_all(lhs, old_sub, new_sub)
    new_rhs = replace_all(rhs, old_sub, new_sub)
    return (new_lhs, new_rhs)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Normal-form generation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# A "normal form" has no reducible redexes:
#   - No pred(succ(...)) or pred(zero)
#   - No add(_, zero) or add(_, succ(...))
#
# With variables, stuck terms are allowed:
#   - pred(var), pred(pred(var))          [pred stuck on variable]
#   - add(e, var), add(e, pred(var))      [add stuck: 2nd arg not zero/succ]
#
# Without variables, only succ^k(zero).

VAR_NAMES = ["n", "m", "k", "a", "b"]

def gen_numeral(max_val: int = 4) -> Expr:
    """Generate succ^k(zero) for random k in [0, max_val]."""
    e = Zero()
    for _ in range(random.randint(0, max_val)):
        e = Succ(e)
    return e

def gen_normal_form(max_depth: int = 3, var_names: Optional[List[str]] = None) -> Expr:
    """
    Generate a random normal-form expression (no reducible redexes).

    With variables, we can generate stuck pred-chains and stuck add-terms.
    Without variables, only succ^k(zero).
    """
    if var_names is None:
        var_names = []

    def _gen(d):
        if d <= 0:
            # Leaf
            if var_names and random.random() < 0.5:
                return Var(random.choice(var_names))
            return Zero()

        r = random.random()
        if r < 0.30:
            # succ(...)
            return Succ(_gen(d - 1))
        elif r < 0.45 and var_names:
            # Stuck pred chain: pred^j(var)
            return _gen_stuck_pred_chain(d)
        elif r < 0.60 and var_names:
            # Stuck add: add(e, stuck_arg) where stuck_arg is var or pred(var)
            left = _gen(d - 1)
            right = _gen_stuck_add_arg(d - 1)
            if right is not None:
                return Add(left, right)
            return _gen(d)   # fallback
        else:
            # Leaf
            if var_names and random.random() < 0.5:
                return Var(random.choice(var_names))
            return Zero()

    def _gen_stuck_pred_chain(d):
        """Generate pred^j(var) — a stuck pred chain."""
        if not var_names:
            return Zero()
        v = Var(random.choice(var_names))
        layers = random.randint(1, min(d, 2))
        e = v
        for _ in range(layers):
            e = Pred(e)
        return e

    def _gen_stuck_add_arg(d):
        """
        Generate an expression suitable as the 2nd arg of a stuck add:
        must NOT be Zero or Succ(...).  So: a variable, or a stuck pred chain.
        """
        if not var_names:
            return None
        if d <= 0 or random.random() < 0.6:
            return Var(random.choice(var_names))
        else:
            return _gen_stuck_pred_chain(d)

    return _gen(max_depth)


def is_normal(expr: Expr) -> bool:
    """Check that expr contains no reducible redexes."""
    if isinstance(expr, Pred):
        if isinstance(expr.inner, (Succ, Zero)):
            return False            # pred_succ or pred_zero redex
        return is_normal(expr.inner)
    if isinstance(expr, Succ):
        return is_normal(expr.inner)
    if isinstance(expr, Add):
        if isinstance(expr.right, (Zero, Succ)):
            return False            # add_zero or add_succ redex
        return is_normal(expr.left) and is_normal(expr.right)
    return True   # Zero, Var


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Expression complication (inverse rewrites)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# We build complicated expressions by choosing random subterm
# positions and wrapping them with redex-introducing patterns.

def _all_positions(expr: Expr) -> List[List[str]]:
    """
    Return all subterm positions as paths.
    Path steps: "i" = inner (unary), "l" = left (binary), "r" = right (binary).
    """
    paths = [[]]   # root
    if isinstance(expr, (Succ, Pred)):
        for sub in _all_positions(expr.inner):
            paths.append(["i"] + sub)
    elif isinstance(expr, Add):
        for sub in _all_positions(expr.left):
            paths.append(["l"] + sub)
        for sub in _all_positions(expr.right):
            paths.append(["r"] + sub)
    return paths

def _get_at(expr: Expr, path: List[str]) -> Expr:
    """Get the subexpression at the given path."""
    if not path:
        return expr
    step = path[0]
    if step == "i" and isinstance(expr, (Succ, Pred)):
        return _get_at(expr.inner, path[1:])
    if step == "l" and isinstance(expr, Add):
        return _get_at(expr.left, path[1:])
    if step == "r" and isinstance(expr, Add):
        return _get_at(expr.right, path[1:])
    raise ValueError(f"Bad path {path} for {expr}")

def _set_at(expr: Expr, path: List[str], replacement: Expr) -> Expr:
    """Return a new expression with the subterm at `path` replaced."""
    if not path:
        return replacement
    step = path[0]
    if step == "i":
        if isinstance(expr, Succ):
            return Succ(_set_at(expr.inner, path[1:], replacement))
        elif isinstance(expr, Pred):
            return Pred(_set_at(expr.inner, path[1:], replacement))
    elif step == "l" and isinstance(expr, Add):
        return Add(_set_at(expr.left, path[1:], replacement), expr.right)
    elif step == "r" and isinstance(expr, Add):
        return Add(expr.left, _set_at(expr.right, path[1:], replacement))
    raise ValueError(f"Bad path {path} for {expr}")


# Expansion operations: each takes a subexpression and returns a
# more complicated expression that reduces back to it.

def _expand_pred_succ(sub: Expr) -> Expr:
    """e  →  pred(succ(e))          [undone by rw [pred_succ]]"""
    return Pred(Succ(clone(sub)))

def _expand_pred_zero(sub: Expr) -> Optional[Expr]:
    """zero  →  pred(zero)          [undone by rw [pred_zero]]"""
    if isinstance(sub, Zero):
        return Pred(Zero())
    return None

def _expand_add_zero(sub: Expr) -> Expr:
    """e  →  add(e, zero)           [undone by rw [add_zero]]"""
    return Add(clone(sub), Zero())

def _expand_add_succ(sub: Expr) -> Optional[Expr]:
    """succ(add(n, m))  →  add(n, succ(m))   [undone by rw [add_succ]]"""
    if isinstance(sub, Succ) and isinstance(sub.inner, Add):
        return Add(clone(sub.inner.left), Succ(clone(sub.inner.right)))
    return None

def _expand_add_succ_compound(sub: Expr) -> Optional[Expr]:
    """
    succ(e)  →  add(e, succ(zero))
    Undone by:  rw [add_succ]  →  succ(add(e, zero))
                rw [add_zero]  →  succ(e)

    Also works with deeper nesting:
    succ(e)  →  add(e, succ(succ(zero)))  needs add_succ twice then add_zero.
    """
    if isinstance(sub, Succ):
        # Build add(inner, succ^k(zero)) for k in {1, 2}
        k = random.choice([1, 2])
        right = Zero()
        for _ in range(k):
            right = Succ(right)
        return Add(clone(sub.inner), right)
    return None


EXPANSIONS = [
    ("pred_succ",           _expand_pred_succ,           1.0),
    ("pred_zero",           _expand_pred_zero,           0.6),
    ("add_zero",            _expand_add_zero,            0.7),
    ("add_succ",            _expand_add_succ,            0.8),
    ("add_succ_compound",   _expand_add_succ_compound,   0.9),
]


def complicate(expr: Expr, num_steps: int, max_size: int = 60) -> Expr:
    """
    Apply `num_steps` random expansions to `expr`.
    Returns a complicated expression that is provably equal to `expr`.
    """
    e = clone(expr)
    for _ in range(num_steps):
        if size(e) >= max_size:
            break
        positions = _all_positions(e)
        random.shuffle(positions)

        applied = False
        for pos in positions:
            sub = _get_at(e, pos)
            # Collect applicable expansions at this position
            candidates = []
            for (name, fn, weight) in EXPANSIONS:
                result = fn(sub)
                if result is not None:
                    candidates.append((result, weight))
            if not candidates:
                continue
            # Weighted random choice
            total = sum(w for _, w in candidates)
            r = random.random() * total
            cum = 0
            chosen = candidates[0][0]
            for (c, w) in candidates:
                cum += w
                if r <= cum:
                    chosen = c
                    break
            e = _set_at(e, pos, chosen)
            applied = True
            break

        if not applied:
            break   # no position found (shouldn't happen normally)
    return e


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Proof search — find a valid tactic proof
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def find_proof(lhs: Expr, rhs: Expr, max_steps: int = 50) -> Optional[List[str]]:
    """
    Search for a tactic proof of  lhs = rhs  using rw steps.
    Returns a list of tactic strings, or None if search fails.

    Only tactics: rw [pred_succ], rw [pred_zero], rw [add_zero], rw [add_succ].

    At each step, all 4 rules are tried; any that produces a valid rewrite
    is a candidate.  One is chosen at random — this produces diverse proofs
    when multiple rules apply simultaneously at different subterms.
    """
    tactics: List[str] = []
    cur_lhs, cur_rhs = clone(lhs), clone(rhs)

    for _ in range(max_steps):
        if cur_lhs == cur_rhs:
            # Lean auto-closes with rfl after the last rw
            return tactics

        # Collect all applicable rewrites
        candidates: List[Tuple[str, Expr, Expr]] = []
        for rule in RULES:
            result = rewrite_in_goal(cur_lhs, cur_rhs, rule)
            if result is not None:
                new_l, new_r = result
                candidates.append((f"rw [{rule.lean_name}]", new_l, new_r))

        if not candidates:
            return None     # stuck — no applicable tactic

        # Pick one at random (diverse proofs for same theorem)
        tactic, cur_lhs, cur_rhs = random.choice(candidates)
        tactics.append(tactic)

    return None   # exceeded max steps


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Theorem generation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class GeneratedTheorem:
    name: str
    var_names: List[str]
    lhs: Expr
    rhs: Expr
    tactics: List[str]
    difficulty: int     # rough measure: number of expansion steps

    @property
    def statement(self) -> str:
        # Only bind variables that actually appear in LHS or RHS
        used = free_vars(self.lhs) | free_vars(self.rhs)
        used_vars = [v for v in self.var_names if v in used]
        binders = " ".join(f"({v} : PNat)" for v in used_vars)
        if binders:
            binders += " "
        return f"theorem {self.name} {binders}: {to_lean(self.lhs)} = {to_lean(self.rhs)}"

    @property
    def proof(self) -> str:
        lines = ["by"] + [f"  {t}" for t in self.tactics]
        return "\n".join(lines)

    @property
    def full_lean(self) -> str:
        return f"{self.statement} := {self.proof}"

    def to_jsonl_dict(self) -> dict:
        used = free_vars(self.lhs) | free_vars(self.rhs)
        used_vars = [v for v in self.var_names if v in used]
        return {
            "name": self.name,
            "statement": self.statement,
            "proof": self.proof,
            "full_lean": self.full_lean,
            "tactic_steps": self.tactics,
            "num_steps": len(self.tactics),
            "num_vars": len(used_vars),
            "difficulty": self.difficulty,
            "lhs_size": size(self.lhs),
            "rhs_size": size(self.rhs),
        }


def generate_one(name: str,
                 difficulty: int,
                 both_sides: bool = False) -> Optional[GeneratedTheorem]:
    """
    Generate one theorem + proof at the given difficulty level.

    difficulty roughly corresponds to the number of expansion steps.
    both_sides: if True, complicate BOTH sides (harder, more varied proofs).
    """
    # Decide on variables
    num_vars = random.choices([0, 1, 2, 3], weights=[0.20, 0.40, 0.25, 0.15])[0]
    chosen_vars = VAR_NAMES[:num_vars]

    # Generate normal form
    nf_depth = random.randint(0, min(difficulty, 4))
    nf = gen_normal_form(max_depth=nf_depth, var_names=chosen_vars)

    # Ensure normal form is actually normal
    if not is_normal(nf):
        # Retry with just numerals
        nf = gen_numeral(max_val=min(difficulty, 4))

    # Complicate to get LHS
    lhs_steps = max(1, difficulty)
    lhs = complicate(nf, num_steps=lhs_steps)

    # Optionally complicate RHS too
    if both_sides:
        rhs_steps = max(1, difficulty // 2)
        rhs = complicate(nf, num_steps=rhs_steps)
    else:
        rhs = clone(nf)

    # Sanity: LHS and RHS should differ (otherwise the theorem is trivial `rfl`)
    if lhs == rhs:
        lhs = complicate(nf, num_steps=max(2, lhs_steps))
        if lhs == rhs:
            return None

    # Find proof
    proof = find_proof(lhs, rhs, max_steps=50)
    if proof is None:
        return None

    return GeneratedTheorem(
        name=name,
        var_names=chosen_vars,
        lhs=lhs,
        rhs=rhs,
        tactics=proof,
        difficulty=difficulty,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Lean preamble and output
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEAN_PREAMBLE = r"""/-
  Auto-generated Peano arithmetic equational theorems.
  Type-check with: lake env lean <this_file>.lean
-/

-- Custom PNat to isolate from Lean's built-in Nat automation.
-- pred and add are opaque so Lean cannot reduce them; the only
-- way to rewrite terms is via the four axioms below.
inductive PNat where
  | zero : PNat
  | succ : PNat → PNat
  deriving Repr, DecidableEq

instance : Inhabited PNat := ⟨PNat.zero⟩

namespace PNat

opaque pred : PNat → PNat
opaque add : PNat → PNat → PNat

axiom pred_succ (n : PNat) : pred (succ n) = n
axiom pred_zero : pred zero = zero
axiom add_zero (n : PNat) : add n zero = n
axiom add_succ (n m : PNat) : add n (succ m) = succ (add n m)

end PNat

open PNat

-- ═══════════════════════════════════════════════════════════
-- Generated theorems
-- ═══════════════════════════════════════════════════════════
"""


def generate_dataset(num_theorems: int, seed: int = 42,
                     min_difficulty: int = 1, max_difficulty: int = 8
                     ) -> List[GeneratedTheorem]:
    """Generate a diverse dataset of theorems."""
    random.seed(seed)
    theorems: List[GeneratedTheorem] = []
    seen_statements: set = set()
    attempts = 0
    max_attempts = num_theorems * 10

    while len(theorems) < num_theorems and attempts < max_attempts:
        attempts += 1
        idx = len(theorems) + 1
        name = f"t{idx:04d}"

        # Sample difficulty with a distribution biased towards medium
        difficulty = random.choices(
            range(min_difficulty, max_difficulty + 1),
            weights=[1.0 / (1 + abs(d - (max_difficulty // 2)))
                     for d in range(min_difficulty, max_difficulty + 1)]
        )[0]

        # Randomly choose theorem style
        both_sides = random.random() < 0.35

        thm = generate_one(
            name=name,
            difficulty=difficulty,
            both_sides=both_sides,
        )

        if thm is None:
            continue

        # Deduplicate by statement
        stmt_key = (to_lean(thm.lhs), to_lean(thm.rhs), tuple(thm.var_names))
        if stmt_key in seen_statements:
            continue
        seen_statements.add(stmt_key)

        theorems.append(thm)

    return theorems


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Output
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def write_lean(theorems: List[GeneratedTheorem], path: str):
    with open(path, "w") as f:
        f.write(LEAN_PREAMBLE)
        for thm in theorems:
            f.write(f"\n{thm.full_lean}\n")
    print(f"Wrote {len(theorems)} theorems to {path}")

def write_jsonl(theorems: List[GeneratedTheorem], path: str):
    with open(path, "w") as f:
        for thm in theorems:
            f.write(json.dumps(thm.to_jsonl_dict()) + "\n")
    print(f"Wrote {len(theorems)} records to {path}")

def print_stats(theorems: List[GeneratedTheorem]):
    if not theorems:
        print("No theorems generated.")
        return
    steps = [len(t.tactics) for t in theorems]
    vars_counts = [len(t.var_names) for t in theorems]
    diffs = [t.difficulty for t in theorems]

    tactic_freq: Dict[str, int] = {}
    for t in theorems:
        for tac in t.tactics:
            tactic_freq[tac] = tactic_freq.get(tac, 0) + 1

    total_steps = sum(steps)

    print(f"\n{'='*50}")
    print(f"Dataset Statistics")
    print(f"{'='*50}")
    print(f"  Theorems generated : {len(theorems)}")
    print(f"  Proof steps        : min={min(steps)}, max={max(steps)}, "
          f"avg={sum(steps)/len(steps):.1f}")
    print(f"  Variables          : min={min(vars_counts)}, max={max(vars_counts)}, "
          f"avg={sum(vars_counts)/len(vars_counts):.1f}")
    print(f"  Difficulty         : min={min(diffs)}, max={max(diffs)}, "
          f"avg={sum(diffs)/len(diffs):.1f}")
    print(f"\n  Tactic frequencies:")
    for tac, count in sorted(tactic_freq.items(), key=lambda x: -x[1]):
        print(f"    {tac:30s} {count:5d}  ({100*count/total_steps:.1f}%)")

    # How often are multiple tactics valid at the same step?
    # (Re-run proofs to check)
    multi_valid_steps = 0
    total_proof_steps = 0
    for thm in theorems:
        cur_l, cur_r = clone(thm.lhs), clone(thm.rhs)
        for tac in thm.tactics:
            n_valid = sum(1 for rule in RULES
                         if rewrite_in_goal(cur_l, cur_r, rule) is not None)
            if n_valid > 1:
                multi_valid_steps += 1
            total_proof_steps += 1
            # Apply the tactic to advance
            for rule in RULES:
                if tac == f"rw [{rule.lean_name}]":
                    result = rewrite_in_goal(cur_l, cur_r, rule)
                    if result:
                        cur_l, cur_r = result
                    break

    print(f"\n  Goal-expert relevance:")
    print(f"    Steps where >1 tactic valid: {multi_valid_steps}/{total_proof_steps} "
          f"({100*multi_valid_steps/max(1,total_proof_steps):.1f}%)")
    print()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic Peano arithmetic theorems with tactic proofs for Lean 4."
    )
    parser.add_argument("--num", type=int, default=200,
                        help="Number of theorems to generate (default: 200)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--min-difficulty", type=int, default=1,
                        help="Minimum difficulty / expansion steps (default: 1)")
    parser.add_argument("--max-difficulty", type=int, default=8,
                        help="Maximum difficulty / expansion steps (default: 8)")
    parser.add_argument("--out-lean", type=str, default="peano_dataset.lean",
                        help="Output Lean 4 file (default: peano_dataset.lean)")
    parser.add_argument("--out-jsonl", type=str, default="peano_dataset.jsonl",
                        help="Output JSONL file (default: peano_dataset.jsonl)")
    parser.add_argument("--stats", action="store_true", default=True,
                        help="Print dataset statistics")
    args = parser.parse_args()

    theorems = generate_dataset(
        num_theorems=args.num,
        seed=args.seed,
        min_difficulty=args.min_difficulty,
        max_difficulty=args.max_difficulty,
    )

    write_lean(theorems, args.out_lean)
    write_jsonl(theorems, args.out_jsonl)

    if args.stats:
        print_stats(theorems)

    # Print a few examples to stdout
    print("─" * 60)
    print("Sample theorems:")
    print("─" * 60)
    for thm in theorems[:5]:
        print(f"\n{thm.full_lean}")


if __name__ == "__main__":
    main()