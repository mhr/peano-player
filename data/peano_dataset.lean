/-
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

theorem t0001 (n : PNat) : pred (pred (succ (succ (add (pred (succ n)) (succ (pred (succ (succ zero)))))))) = add (add n (succ (succ zero))) zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0002 : pred (succ (add (pred (succ (pred (succ (pred (succ zero)))))) zero)) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0003 : add (add (succ (add (succ zero) (add zero zero))) (succ zero)) zero = succ (succ (succ zero)) := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0004 : add zero zero = zero := by
  rw [add_zero]

theorem t0005 (n : PNat) : pred (pred (succ (pred (succ (succ (add n zero)))))) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0006 : pred (succ (add (pred (succ (add (pred zero) zero))) (pred zero))) = pred (succ (add (add zero zero) zero)) := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0007 : pred (succ (pred (add (add (pred zero) (pred (add zero zero))) (succ zero)))) = zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0008 (n : PNat) : pred (succ (pred (succ (pred (pred (succ (pred (succ n)))))))) = pred n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0009 (m : PNat) : add (add m zero) zero = pred (succ m) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0010 (m : PNat) : succ (add (pred (pred (succ m))) zero) = pred (succ (succ (pred m))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0011 : pred (succ (pred (succ (pred (succ (add (pred (pred zero)) zero)))))) = zero := by
  rw [pred_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0012 (k : PNat) : succ (add k zero) = succ k := by
  rw [add_zero]

theorem t0013 : pred (succ (add (add zero zero) zero)) = pred (succ zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0014 : succ (add (pred (add (succ zero) zero)) (pred zero)) = succ zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0015 (n : PNat) : pred (succ (add zero (add (add n zero) zero))) = add zero n := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0016 : pred (succ (pred (succ (pred (pred zero))))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]
  rw [pred_succ]

theorem t0017 (k : PNat) : pred (succ (pred (succ (add (pred (pred (pred (succ k)))) zero)))) = pred (add (pred (succ (pred k))) zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0018 : add (pred (succ (pred (succ (pred (succ (succ zero))))))) (succ (succ zero)) = succ (pred (add (succ zero) (succ (succ zero)))) := by
  rw [add_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0019 : add zero (add (pred zero) zero) = zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0020 (m : PNat) : pred (succ m) = add m zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0021 : pred (pred (succ (pred (add zero (pred (succ (pred (succ zero)))))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [pred_zero]

theorem t0022 : pred (succ (add (pred (add zero zero)) zero)) = pred (succ (pred (succ zero))) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0023 : pred (add (add (add (add (add zero zero) (add zero zero)) zero) zero) (pred (succ (succ zero)))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0024 (n : PNat) : pred (succ (pred (succ (pred (succ (pred (succ (pred (succ (add (pred (succ (pred (succ n)))) zero)))))))))) = pred (succ (pred (add (add n zero) (succ zero)))) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0025 (m : PNat) : pred (succ (pred m)) = pred (add m zero) := by
  rw [pred_succ]
  rw [add_zero]

theorem t0026 (n : PNat) : pred (add (succ (add (add (pred (pred n)) zero) zero)) zero) = add (pred (pred n)) (pred (succ zero)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0027 : add (add (pred (succ (pred zero))) (pred (succ (pred (succ zero))))) zero = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0028 (n : PNat) : pred (succ (add (pred (succ (add n (pred (succ zero))))) zero)) = pred (pred (succ (succ n))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0029 (n : PNat) : add (pred (succ n)) (pred (pred (succ (succ zero)))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0030 (n : PNat) : pred (succ (add (add (pred (succ (add n zero))) zero) (succ (pred (succ zero))))) = add (pred (succ (pred (succ (succ n))))) zero := by
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0031 (n : PNat) : add (add n zero) (pred (add (pred (pred (pred (succ (succ (pred (succ zero))))))) zero)) = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0032 (n : PNat) : succ (pred (pred (succ (add n zero)))) = succ (pred (pred (succ n))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0033 : pred (add zero zero) = pred (succ zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]

theorem t0034 (n : PNat) : pred (succ (add n zero)) = pred (succ n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0035 : pred (succ zero) = zero := by
  rw [pred_succ]

theorem t0036 (n : PNat) : pred (succ n) = n := by
  rw [pred_succ]

theorem t0037 : add (pred (add (pred (pred (succ (succ (pred (succ (add (pred (succ (succ zero))) zero))))))) zero)) zero = pred (succ (pred (succ (pred (pred (succ zero)))))) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0038 : pred (succ (add (add (pred zero) zero) zero)) = zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0039 (m : PNat) : succ (succ (add (add (add (add m zero) zero) (pred zero)) (succ zero))) = succ (succ (succ (add m (pred zero)))) := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0040 : pred (succ (pred (succ zero))) = zero := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0041 : add (add (add zero zero) (succ zero)) (pred zero) = add (succ (pred (succ zero))) zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0042 : pred (pred (succ (succ (add zero (pred (succ (add zero zero))))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0043 : succ (pred (succ (pred (pred (add (succ zero) (succ zero)))))) = succ zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0044 (n : PNat) : add (add (add (pred (succ n)) (pred (succ (add n (add zero zero))))) (pred zero)) zero = add (pred (succ (add n (pred zero)))) n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0045 : add (add (pred (succ (pred (pred (succ (pred zero)))))) (pred (succ zero))) zero = zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0046 (n : PNat) (m : PNat) : pred (succ (add (pred (succ (pred (succ (pred (succ (pred (succ (pred (add (succ m) (pred zero))))))))))) n)) = add m n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0047 : pred (succ (pred (succ (pred (succ (add (pred (pred (add (succ (succ zero)) zero))) (pred (succ zero)))))))) = pred (succ (pred (succ (pred (succ (pred (succ zero))))))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0048 (n : PNat) : add (add (pred (succ n)) zero) (pred (pred (add zero (succ zero)))) = add (pred (succ (pred (succ n)))) zero := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0049 (n : PNat) : pred (pred (succ (succ (pred (succ (add n zero)))))) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0050 (m : PNat) : pred (add (pred (add (pred (succ m)) zero)) (succ zero)) = pred (succ (pred (pred (succ m)))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0051 (n : PNat) : add (pred (succ (pred (succ n)))) zero = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0052 (n : PNat) : pred (succ (add (pred (succ zero)) (pred (succ (pred (succ n)))))) = add zero n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0053 : pred (succ (add zero zero)) = zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0054 (m : PNat) : pred (succ (pred (add (pred (add (succ m) zero)) zero))) = pred (pred (pred (succ (succ m)))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0055 (m : PNat) : add (add (pred (succ m)) zero) (pred (succ zero)) = pred (add (succ m) zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0056 (n : PNat) : add (pred (succ (succ (succ (succ (add n zero)))))) zero = succ (succ (succ n)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0057 : add zero (add (pred (pred (succ zero))) zero) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0058 (n : PNat) : add n (pred (succ (pred (add (succ zero) zero)))) = add (add n zero) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0059 (m : PNat) (k : PNat) : add (add (pred (succ (pred (succ m)))) zero) k = add (pred (succ m)) k := by
  rw [pred_succ]
  rw [add_zero]

theorem t0060 (k : PNat) : add zero (pred (add k (succ zero))) = add zero k := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0061 : succ (pred (succ (pred (succ zero)))) = succ zero := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0062 (n : PNat) : pred (succ (pred (succ n))) = pred (succ n) := by
  rw [pred_succ]

theorem t0063 : succ (pred (succ (add zero (succ (pred (succ (pred (succ zero)))))))) = succ (succ zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0064 (n : PNat) : pred (succ (pred n)) = pred n := by
  rw [pred_succ]

theorem t0065 : add (pred (succ (pred (add (add zero (succ zero)) zero)))) zero = add (add zero zero) zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0066 (n : PNat) : pred (succ (add n zero)) = n := by
  rw [add_zero]
  rw [pred_succ]

theorem t0067 (m : PNat) : add (succ (pred (succ m))) (succ (succ zero)) = succ (add m (succ (succ zero))) := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0068 (n : PNat) : add (succ (add (pred (succ (pred (succ n)))) zero)) zero = succ (add (add n zero) zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0069 : add zero zero = zero := by
  rw [add_zero]

theorem t0070 : pred (succ (pred (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0071 (n : PNat) : pred (pred (pred (succ (pred (succ (add (pred (succ (add (pred (succ n)) zero))) zero)))))) = pred (pred n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0072 (n : PNat) : succ (pred (succ n)) = add n (succ zero) := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0073 : pred (pred (succ (succ (pred (succ (add zero zero)))))) = pred (pred (succ (succ zero))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0074 : add (pred (succ (add zero (pred (succ zero))))) (pred (succ zero)) = add zero (pred zero) := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0075 (m : PNat) : pred (succ (add (add m (pred zero)) zero)) = add (pred (succ m)) zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0076 : pred (add (pred (succ zero)) zero) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]

theorem t0077 : pred (add (succ (pred (succ (add (add zero zero) zero)))) zero) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0078 (m : PNat) : pred (succ (pred (add m zero))) = pred m := by
  rw [pred_succ]
  rw [add_zero]

theorem t0079 : add (pred (add (pred zero) zero)) zero = zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0080 (n : PNat) : add (pred (succ (add (add (succ n) zero) zero))) zero = succ n := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0081 (n : PNat) : pred (add (pred (pred (succ (succ n)))) (succ zero)) = add n (pred (succ zero)) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0082 (n : PNat) : pred (add (pred (succ (pred (succ (pred (pred (succ (succ n)))))))) zero) = pred n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0083 (n : PNat) : pred (succ (pred (add (pred (succ (add n (succ zero)))) zero))) = n := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0084 (n : PNat) : add (pred (succ (pred (succ zero)))) (pred (add (succ (add n zero)) zero)) = pred (succ (add (pred (succ zero)) n)) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0085 : pred (add (succ zero) zero) = zero := by
  rw [add_zero]
  rw [pred_succ]

theorem t0086 : add (add (add (pred (succ (pred (succ (add zero (pred (succ (pred zero)))))))) zero) zero) zero = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0087 : add (add zero (pred (succ zero))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0088 : add (pred (succ (pred zero))) (add zero zero) = zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0089 (n : PNat) : pred (succ (succ (pred (succ (add n (pred zero)))))) = add (succ n) (pred (succ zero)) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0090 : pred (pred (succ (succ (succ (pred (pred zero)))))) = succ zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]

theorem t0091 : add (pred (succ (pred (succ (succ zero))))) zero = succ zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0092 (m : PNat) : pred (pred (pred (add (pred (succ (succ (pred (succ m))))) zero))) = pred (pred m) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0093 : pred zero = pred (succ zero) := by
  rw [pred_zero]
  rw [pred_succ]

theorem t0094 : add (pred (succ (pred zero))) (succ zero) = succ zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0095 : pred (pred (succ (pred (succ (succ zero))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0096 (n : PNat) : pred (succ (add (add (pred zero) (pred (pred (succ n)))) (pred (add (succ (add zero zero)) zero)))) = add zero (pred n) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0097 : add (add (pred (add zero (succ zero))) zero) zero = zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0098 : add (add (add zero zero) (pred zero)) zero = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0099 : pred (succ (pred (succ (add (pred (succ (succ zero))) zero)))) = succ zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0100 : add (add (pred (pred (succ (succ zero)))) zero) zero = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0101 : pred (add (pred (succ zero)) (succ zero)) = pred zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0102 (n : PNat) : add (pred (succ (pred (add n (succ zero))))) (pred (succ zero)) = n := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0103 : pred (add (add (pred (succ zero)) (succ zero)) zero) = zero := by
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0104 : succ (pred (succ (pred (succ zero)))) = succ (pred (succ zero)) := by
  rw [pred_succ]

theorem t0105 (m : PNat) : pred (succ (pred (succ (pred (succ (add (pred (succ m)) zero)))))) = add (pred (succ m)) zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0106 (m : PNat) : pred (succ m) = m := by
  rw [pred_succ]

theorem t0107 : add (add (succ (pred (succ zero))) zero) zero = pred (succ (succ zero)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0108 (n : PNat) : pred (pred (add (succ (succ (pred (succ (pred (succ n)))))) zero)) = add (add n zero) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0109 (n : PNat) : add (add (add (add (pred (succ (pred (add (pred (succ n)) zero)))) (pred (succ zero))) zero) zero) zero = pred (pred (succ (pred (succ (pred (succ (pred (succ n)))))))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0110 (n : PNat) : add (succ (pred (succ (pred (succ n))))) (pred (pred (pred (succ (succ n))))) = pred (succ (add (add (succ n) zero) (pred n))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0111 : pred (pred (add (succ (succ (pred (succ zero)))) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0112 (n : PNat) : pred (succ (add (pred (succ (succ n))) zero)) = succ (pred (succ n)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0113 : add (pred (succ (pred (succ (add zero zero))))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0114 : pred (succ (add (pred (succ (succ zero))) zero)) = add zero (succ zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0115 (n : PNat) : pred (add (succ (add n (pred (succ (pred zero))))) (pred (succ (pred zero)))) = n := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0116 (m : PNat) : pred (add (add (pred (succ m)) (add zero zero)) (succ zero)) = m := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0117 : add (add (add zero (pred (succ (pred (succ (succ zero)))))) (pred (succ zero))) zero = succ zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0118 (n : PNat) : pred (succ (pred (add (succ (pred (succ n))) zero))) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0119 (n : PNat) : pred (pred (succ (pred (succ (pred (succ (succ (succ n)))))))) = add (add (succ n) zero) zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0120 : pred (succ (add (pred (succ (pred (succ (add zero (add (add zero zero) (pred zero))))))) zero)) = add (add (pred (succ (pred (succ zero)))) zero) zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0121 (n : PNat) : pred (succ (pred (succ (add (succ n) (pred (add n (succ zero))))))) = pred (succ (pred (succ (add (succ n) n)))) := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0122 : pred (succ (pred (add (succ zero) (pred (succ (add (add zero zero) zero)))))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0123 : pred (succ (pred (succ (add (add zero zero) zero)))) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0124 (n : PNat) : pred (succ (pred (succ (pred (succ (add n zero)))))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0125 (n : PNat) : pred (add n (succ zero)) = n := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0126 : add (add (pred (succ (pred zero))) zero) zero = zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0127 : succ (add (pred (pred (add (pred (succ (succ zero))) zero))) zero) = succ zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0128 (n : PNat) : add (pred (succ (add (succ (pred (succ (pred (add n (pred (succ zero))))))) zero))) zero = succ (pred n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0129 (n : PNat) : pred (succ (succ (add n (succ (pred (succ (pred (succ zero)))))))) = succ (succ n) := by
  rw [pred_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0130 : succ (pred (pred (succ (succ (succ (pred (succ (pred (succ zero))))))))) = add (add (succ (succ zero)) zero) zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0131 (n : PNat) : add (pred (add (succ (pred (succ (pred (pred n))))) zero)) zero = pred (pred n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0132 (n : PNat) : pred (add (pred (succ (add (pred (succ (succ n))) (pred (succ zero))))) zero) = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0133 : pred (succ (pred (pred (succ (add (add (add (pred zero) (add zero zero)) zero) zero))))) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0134 (n : PNat) : pred (succ (pred (succ (add n n)))) = add (add n zero) n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0135 (n : PNat) : add (pred (pred (succ (pred (succ (pred (add n zero))))))) (pred (succ n)) = add (pred (pred (pred (succ n)))) (pred (succ n)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0136 : succ (add (pred (succ (pred (succ (add (pred (pred (succ zero))) zero))))) zero) = add (pred (succ zero)) (add zero (succ zero)) := by
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0137 (m : PNat) : pred (add (pred (succ m)) (succ (add (pred (succ zero)) zero))) = pred (succ (pred (succ m))) := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0138 : pred (succ (add zero zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]

theorem t0139 (n : PNat) : pred (succ (add (pred (succ (pred (add (pred (pred n)) (add (add (succ zero) zero) zero))))) zero)) = pred (pred n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0140 (n : PNat) : pred (succ (add n (add (add (pred zero) zero) (add (pred (succ (pred (succ zero)))) zero)))) = n := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0141 : pred (succ (add (pred (succ (add zero zero))) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0142 : pred (pred (pred (succ (succ (succ (pred zero)))))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0143 : pred (pred (succ (succ zero))) = add zero zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0144 (n : PNat) : succ (add (add (succ (add (pred (succ n)) n)) (pred (succ (add (pred n) zero)))) zero) = succ (add (succ (add n n)) (pred n)) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0145 : pred (succ (pred (add (pred (add (succ zero) (add (add zero zero) zero))) (add zero zero)))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0146 (n : PNat) : pred (succ (pred (pred (succ (succ (pred (succ (add n (pred (pred (succ (succ (pred zero))))))))))))) = pred (succ (add (pred (succ (pred (succ n)))) zero)) := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0147 (n : PNat) : add (succ (succ (succ (pred (succ (add (pred zero) n)))))) (pred (succ zero)) = succ (succ (succ (add zero n))) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0148 : pred (succ (add zero (pred (succ (add zero zero))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0149 (n : PNat) : add (pred (succ (add (add n zero) zero))) zero = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0150 : pred (succ (add zero (pred (pred (succ (succ zero)))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0151 (n : PNat) : pred (succ (add (add (pred (succ n)) (add zero (add zero zero))) (pred zero))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0152 (n : PNat) : add (add n zero) (pred (succ zero)) = add n zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0153 : pred (add zero (succ zero)) = zero := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0154 (n : PNat) : add n zero = n := by
  rw [add_zero]

theorem t0155 (n : PNat) : pred (pred (pred (succ (succ (pred (succ (add (add n (pred (succ (pred (pred (succ (succ zero))))))) zero))))))) = pred n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0156 (m : PNat) : pred (succ (succ (succ (add (add (add m (succ zero)) zero) zero)))) = succ (succ (succ m)) := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0157 (n : PNat) : add (pred (succ (add n (pred (pred (succ (succ zero))))))) zero = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0158 (m : PNat) : pred (succ (pred (succ (pred (succ (add (succ m) zero)))))) = succ m := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0159 (m : PNat) : pred (add (pred (pred (succ (add (pred (succ (add (succ m) zero))) zero)))) (succ zero)) = m := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0160 (k : PNat) : add (pred (add (succ (pred (succ k))) zero)) (pred (succ zero)) = k := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0161 (n : PNat) : add zero (pred (succ n)) = add zero n := by
  rw [pred_succ]

theorem t0162 : add (pred (succ (pred (succ (pred (pred (succ (add (succ (pred (succ (add zero zero)))) zero)))))))) zero = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0163 (m : PNat) : pred (succ (pred (succ m))) = add m zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0164 (m : PNat) : add (pred (add m (succ zero))) zero = m := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0165 : add (add zero (succ zero)) (succ zero) = succ (succ zero) := by
  rw [add_succ]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0166 (n : PNat) : pred (succ (pred (succ (add (pred (succ (pred (succ n)))) zero)))) = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0167 (n : PNat) : pred (succ (add (pred (succ n)) (pred zero))) = n := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0168 (n : PNat) : pred (pred (succ (succ (add zero n)))) = pred (succ (add zero n)) := by
  rw [pred_succ]

theorem t0169 (n : PNat) : pred (succ (add (add (add n zero) zero) zero)) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0170 : pred (add (add (pred (succ (succ zero))) zero) (pred zero)) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0171 : pred (pred zero) = pred (succ zero) := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]

theorem t0172 : pred (add (succ (succ (pred (succ (pred (succ zero)))))) zero) = add zero (add zero (succ zero)) := by
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0173 : pred (add (succ (succ (pred (succ (succ (add (pred zero) zero)))))) zero) = succ (add (add (succ zero) zero) zero) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]

theorem t0174 (n : PNat) (m : PNat) : succ (pred (succ (add (add n zero) (pred (pred (succ (pred (succ (pred (succ m)))))))))) = succ (add n (pred m)) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0175 : pred (add zero zero) = add zero zero := by
  rw [add_zero]
  rw [pred_zero]

theorem t0176 : add (pred (succ (pred (succ (add (pred (succ zero)) zero))))) zero = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0177 : pred (succ (pred (add zero (pred (succ (succ zero)))))) = pred (succ (pred zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0178 (n : PNat) : add (pred (succ n)) zero = n := by
  rw [pred_succ]
  rw [add_zero]

theorem t0179 : add zero (add (pred (succ (add zero zero))) zero) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0180 (m : PNat) : succ (pred (succ m)) = succ m := by
  rw [pred_succ]

theorem t0181 (n : PNat) : pred (succ (add (pred (succ (add (succ (pred (pred (succ zero)))) n))) zero)) = add (succ zero) n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0182 : pred (pred (succ (succ (pred (succ (pred (pred (succ (pred (succ (succ zero))))))))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0183 : pred (succ (add (succ zero) zero)) = succ zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0184 (m : PNat) : add (pred (succ (pred zero))) (pred (succ (pred (pred (succ (succ (add (pred (succ m)) zero))))))) = add (pred (pred (succ (succ (pred zero))))) m := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0185 : add (pred (pred (succ (succ (pred (succ zero)))))) (succ zero) = succ zero := by
  rw [pred_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0186 (k : PNat) : add (succ (succ (pred (succ (pred (succ k)))))) (pred (succ zero)) = succ (succ k) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0187 (m : PNat) : pred (add (pred (succ (add (pred (succ m)) zero))) (succ zero)) = m := by
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0188 (n : PNat) : pred (succ (pred (succ n))) = add n zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0189 (n : PNat) : add (pred (succ n)) zero = pred (succ n) := by
  rw [pred_succ]
  rw [add_zero]

theorem t0190 (n : PNat) : succ (pred (succ (add (pred (succ (succ n))) zero))) = succ (succ n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0191 : add (add zero (pred (succ zero))) (pred (add zero zero)) = pred (pred (succ (succ zero))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0192 (n : PNat) : add (succ n) (succ (pred zero)) = add (succ n) (succ zero) := by
  rw [add_succ]
  rw [pred_zero]
  rw [add_succ]

theorem t0193 (m : PNat) : pred (succ (add (add (succ zero) m) (pred (succ (pred zero))))) = pred (succ (add (succ (add zero zero)) m)) := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0194 : add (pred (pred zero)) zero = add zero zero := by
  rw [pred_zero]
  rw [pred_zero]

theorem t0195 (n : PNat) : pred (succ (pred (succ (pred n)))) = pred (succ (pred n)) := by
  rw [pred_succ]

theorem t0196 : pred (succ (pred (add (succ (add zero (pred (succ zero)))) zero))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0197 : pred zero = add zero zero := by
  rw [pred_zero]
  rw [add_zero]

theorem t0198 : pred (add (succ zero) zero) = add zero zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0199 (n : PNat) : pred (succ (pred (pred (succ (succ (add (pred (succ n)) zero)))))) = add (pred (succ n)) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0200 : add (pred (add zero (succ zero))) (succ zero) = succ zero := by
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0201 (n : PNat) : add (pred (pred (pred (succ (succ (pred (pred (add (pred (succ n)) (succ zero))))))))) (succ zero) = succ (pred (pred n)) := by
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0202 : pred (pred (succ (succ (add (pred zero) zero)))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0203 : add (pred (add (succ (pred (succ zero))) zero)) (pred zero) = pred (succ (add zero zero)) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0204 (n : PNat) : succ (pred (succ (pred (succ (pred (succ (pred (pred (pred (succ n)))))))))) = succ (pred (pred n)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0205 (n : PNat) : add (add n (pred zero)) zero = n := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0206 (m : PNat) : pred (succ (pred (add (succ m) zero))) = add m zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0207 : pred (succ (pred (succ (pred (succ (pred (pred (succ zero)))))))) = add zero (pred (succ zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0208 : add (add (pred (succ zero)) zero) (pred (succ zero)) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0209 : pred (succ (add (pred (succ zero)) (add zero zero))) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0210 : add (pred zero) (succ zero) = succ (pred (succ zero)) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0211 (n : PNat) : add (add (pred (succ (pred (succ (pred (succ n)))))) zero) zero = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0212 : pred (succ (pred (succ (add (add (pred zero) (pred (succ zero))) (pred (succ zero)))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0213 : add (add (pred (succ zero)) zero) (pred (succ zero)) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0214 : pred (add (add zero (succ zero)) (pred (succ zero))) = add zero (pred (succ zero)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0215 (k : PNat) : pred (succ (pred (succ k))) = pred (succ k) := by
  rw [pred_succ]

theorem t0216 : pred (succ (pred (succ (add zero zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0217 : pred (succ (succ zero)) = succ zero := by
  rw [pred_succ]

theorem t0218 : pred (succ (pred (pred (add (succ zero) zero)))) = pred (pred zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]

theorem t0219 (n : PNat) : add (add zero (pred (succ n))) zero = add zero n := by
  rw [pred_succ]
  rw [add_zero]

theorem t0220 (m : PNat) : add m zero = m := by
  rw [add_zero]

theorem t0221 : pred (succ (pred (add (succ zero) zero))) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0222 : add zero zero = zero := by
  rw [add_zero]

theorem t0223 (n : PNat) : succ (pred (add (add n zero) (add (succ zero) zero))) = succ n := by
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0224 : succ (add (add (add (add (pred (succ (pred (add zero (succ zero))))) zero) zero) zero) zero) = succ zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0225 : add (succ (pred (add (succ (pred (succ zero))) (add zero (pred (succ zero)))))) zero = pred (pred (succ (succ (succ (pred zero))))) := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0226 : add (pred zero) zero = zero := by
  rw [add_zero]
  rw [pred_zero]

theorem t0227 (m : PNat) : pred (add (pred (succ m)) zero) = pred m := by
  rw [pred_succ]
  rw [add_zero]

theorem t0228 : add (pred (pred (succ zero))) zero = pred (succ zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0229 (n : PNat) : succ (pred (add (succ n) zero)) = succ (pred (succ n)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0230 : add (pred zero) zero = add zero zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0231 (n : PNat) : pred (succ (pred (add (pred (succ n)) (succ zero)))) = n := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0232 (n : PNat) : add zero (pred (succ (pred (succ n)))) = pred (succ (add zero n)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0233 (n : PNat) : add (add n zero) (add (pred (add (succ (pred (succ (pred (succ (pred zero)))))) zero)) zero) = n := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0234 : pred (add (pred (succ (add (pred (succ zero)) zero))) (succ (pred (pred zero)))) = zero := by
  rw [add_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0235 (n : PNat) : pred (add (add (succ (pred (pred (succ (succ (add (succ (pred (add n (succ zero)))) zero)))))) (succ zero)) zero) = succ (succ n) := by
  rw [add_succ]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0236 (m : PNat) : add (add m zero) zero = pred (succ m) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0237 (k : PNat) : add (add (succ (pred zero)) zero) (pred (succ (pred (succ (pred k))))) = add (succ zero) (pred k) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0238 : pred (succ (add zero (pred (succ zero)))) = pred (succ zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0239 (n : PNat) : pred (succ (pred (succ (add n zero)))) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0240 : add (pred (pred (succ (succ (pred (succ zero)))))) zero = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0241 (n : PNat) : add (pred (succ (succ n))) zero = succ (pred (succ n)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0242 : pred (succ (succ (pred (pred (succ (pred (succ (succ (pred (pred (succ (succ (pred (pred (succ zero))))))))))))))) = pred (pred (succ (succ (pred (succ (pred (succ (succ zero)))))))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0243 (m : PNat) : add (pred (pred (succ (succ (succ m))))) zero = succ m := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0244 : add (pred (add (pred (succ (add zero zero))) (succ zero))) zero = zero := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0245 : succ (pred (succ zero)) = succ zero := by
  rw [pred_succ]

theorem t0246 (n : PNat) : pred (succ (add (pred (succ n)) zero)) = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0247 (n : PNat) : add (pred n) zero = pred n := by
  rw [add_zero]

theorem t0248 (n : PNat) : pred (succ (succ (pred (add (succ (pred (succ n))) zero)))) = succ n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0249 (n : PNat) : pred (add (add (succ (pred (add n zero))) zero) zero) = pred (add (pred (succ n)) zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0250 (n : PNat) : add (pred (add (pred (add (succ (pred (succ (succ n)))) zero)) zero)) zero = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0251 : add zero (succ (add (pred zero) zero)) = succ (pred (succ zero)) := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0252 : add (pred (succ (add (add (succ zero) zero) zero))) zero = succ zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0253 (n : PNat) : add (pred (add (add (succ n) zero) zero)) zero = pred (succ (add n zero)) := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0254 : pred (succ zero) = zero := by
  rw [pred_succ]

theorem t0255 (n : PNat) : pred (pred (succ (pred (add n (add (succ zero) (pred (pred (succ (pred zero))))))))) = pred n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0256 (n : PNat) : succ (succ (pred (pred (succ (add (add (succ n) zero) zero))))) = succ (succ n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0257 (n : PNat) : pred (succ (add (succ (add zero (add (add n zero) zero))) (succ zero))) = succ (succ (add zero (add (pred (succ n)) zero))) := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0258 (n : PNat) : add (pred (pred (succ n))) (pred zero) = pred n := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0259 : pred (add (succ (succ (pred (succ (pred zero))))) zero) = succ zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0260 : add (add (pred (succ (pred (pred (succ (pred (succ (succ zero)))))))) (add zero zero)) zero = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0261 (n : PNat) : pred (succ (pred (add (add n (succ zero)) zero))) = n := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0262 : add zero (add zero (add (pred (succ zero)) zero)) = pred (succ (pred (succ zero))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0263 : add (add (add (pred zero) (pred (succ zero))) (add (add zero zero) zero)) zero = pred (succ (add (pred zero) zero)) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0264 : add (add (pred (pred zero)) zero) zero = zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0265 (n : PNat) : pred (pred (add (pred (add (succ (add (pred (succ n)) zero)) zero)) zero)) = pred (pred n) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0266 : add zero zero = pred (succ zero) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0267 (m : PNat) : add (pred (add m (succ (pred (succ (pred (succ zero))))))) zero = pred (pred (succ (succ m))) := by
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0268 : pred (succ (pred (add (add (succ zero) zero) (pred (succ (pred zero)))))) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0269 (n : PNat) : add (add n zero) zero = pred (succ n) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0270 : pred (succ (pred (succ (add (pred (succ zero)) zero)))) = pred (add (succ zero) zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0271 (n : PNat) : pred (pred (succ (succ (pred (succ n))))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0272 (n : PNat) (m : PNat) : pred (add (succ (add (pred (succ (pred (pred (add (pred (succ (add (pred (succ m)) zero))) zero))))) n)) zero) = add (pred (pred (add m zero))) (pred (succ (pred (succ n)))) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0273 : pred (succ zero) = add zero zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0274 (n : PNat) : pred (add (add (pred (pred (succ (succ n)))) zero) (succ zero)) = pred (pred (succ (pred (succ (succ n))))) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0275 : pred (add (pred (succ (pred (pred (succ (pred (succ (succ zero)))))))) (succ (add zero zero))) = zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0276 : add (add (pred (succ (pred (add (succ zero) zero)))) zero) zero = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0277 (n : PNat) : pred (pred (succ (pred (pred (succ (add n (pred (succ (pred (succ zero)))))))))) = pred (pred n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0278 : add (pred zero) zero = zero := by
  rw [pred_zero]
  rw [add_zero]

theorem t0279 : add (add zero zero) zero = zero := by
  rw [add_zero]
  rw [add_zero]

theorem t0280 (n : PNat) : pred (add (succ (add (pred (succ n)) zero)) zero) = n := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0281 : add (add (add (add zero zero) zero) zero) zero = add zero (pred zero) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0282 (n : PNat) : succ (add n (pred (add (succ n) (pred (succ zero))))) = succ (add (add n n) zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0283 (n : PNat) : add (succ (pred (succ n))) zero = succ n := by
  rw [pred_succ]
  rw [add_zero]

theorem t0284 : succ (pred (pred (succ (add zero (succ (pred (succ zero))))))) = succ zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0285 : pred (succ (pred zero)) = zero := by
  rw [pred_succ]
  rw [pred_zero]

theorem t0286 : succ (pred (pred (succ (succ (add (add (pred (succ (pred (succ (succ (pred zero)))))) zero) zero))))) = succ (succ zero) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0287 (n : PNat) : add (add (add (add zero (pred (succ n))) n) zero) zero = add (add zero n) n := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0288 (n : PNat) : pred (succ (add (pred (succ (pred (pred (succ (pred n)))))) zero)) = pred (add (pred n) (add zero zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0289 : pred (succ (add (pred (succ (pred (succ (pred (add (pred zero) (succ zero))))))) zero)) = zero := by
  rw [pred_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0290 (m : PNat) : pred (succ (add (pred (succ (pred (succ (add (pred m) zero))))) (pred (succ zero)))) = pred m := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0291 : pred (succ (add (pred (add (succ (pred (succ (pred (pred zero))))) (add zero zero))) zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0292 : pred (pred (add (succ (pred (succ (pred zero)))) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0293 (n : PNat) : add (pred (pred (succ (succ (pred (pred (succ (add (add n zero) zero)))))))) (add zero zero) = pred n := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0294 : pred (succ (add (add (pred (succ (pred zero))) zero) zero)) = add (pred (succ zero)) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0295 (k : PNat) : succ (pred (add (add (add (pred (pred (succ k))) zero) zero) (succ (add zero (succ zero))))) = add (add (add (pred k) zero) (succ (succ zero))) zero := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_succ]
  rw [add_succ]
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0296 : add (pred (succ zero)) zero = zero := by
  rw [add_zero]
  rw [pred_succ]

theorem t0297 : add zero (pred (succ (add (pred zero) zero))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0298 : pred (succ (add (pred (succ (add (add zero zero) zero))) zero)) = add (pred zero) zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0299 : pred (succ (pred (pred (succ (pred zero))))) = add zero (pred zero) := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0300 (m : PNat) : pred (succ (add (add (pred (succ (pred (succ m)))) zero) (succ zero))) = succ (pred (succ (add m zero))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0301 (m : PNat) : add (add (pred (succ zero)) (pred (succ zero))) (add m zero) = add zero m := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0302 (n : PNat) : add n (add (add zero zero) (add zero zero)) = pred (succ (pred (succ n))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0303 (m : PNat) : add (pred (succ (pred zero))) m = add zero m := by
  rw [pred_succ]
  rw [pred_zero]

theorem t0304 : pred (pred (add zero (succ (pred zero)))) = zero := by
  rw [pred_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]

theorem t0305 : add (pred zero) (pred (pred (succ (add zero zero)))) = pred (succ (pred zero)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0306 : pred (add (add (pred zero) (succ (pred zero))) zero) = zero := by
  rw [add_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0307 (n : PNat) : pred (succ (pred (succ (add (add zero (pred (succ (pred (add (succ (pred (succ (add n zero)))) zero))))) zero)))) = add zero n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0308 : add (pred (succ (add zero zero))) zero = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0309 : add (pred (succ (pred (succ (pred (add (add (succ (pred (succ (pred zero)))) zero) zero)))))) zero = add zero (add (pred zero) (pred zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0310 (n : PNat) : pred (succ (pred (pred (succ (succ n))))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0311 (m : PNat) : pred (add (add (pred (pred (succ m))) zero) (succ zero)) = pred m := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0312 (m : PNat) : pred (succ (succ (pred (succ m)))) = succ m := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0313 (m : PNat) : add (succ (succ (add m (add (pred (succ zero)) zero)))) (pred (succ zero)) = succ (succ m) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0314 : pred (succ (pred (succ (pred (succ (pred (succ zero))))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0315 : add (add (pred (add zero zero)) (add (pred (succ zero)) zero)) zero = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0316 : add (add (add zero zero) zero) (pred (succ zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0317 (n : PNat) : pred (add (add (pred (pred (succ (succ n)))) (add zero zero)) zero) = pred n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0318 : pred (succ (pred (succ (pred zero)))) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_succ]

theorem t0319 : pred (pred (succ (succ (add zero (pred zero))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0320 (n : PNat) : add (add (add (pred (succ (pred (succ (pred n))))) (pred (succ zero))) zero) zero = pred n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0321 (k : PNat) : add (add k zero) zero = k := by
  rw [add_zero]
  rw [add_zero]

theorem t0322 : add zero (succ zero) = succ (pred (succ zero)) := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0323 : pred zero = zero := by
  rw [pred_zero]

theorem t0324 (m : PNat) : add (pred (add (succ (pred (succ m))) (pred (succ zero)))) zero = m := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0325 : pred (pred (pred (succ (succ (succ (add zero (pred (succ (pred (succ (pred (succ zero)))))))))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0326 (m : PNat) : add m (add zero zero) = m := by
  rw [add_zero]
  rw [add_zero]

theorem t0327 : pred (succ (add (succ (pred (succ zero))) (succ (pred (succ zero))))) = succ (succ (pred (succ (pred (succ zero))))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0328 (m : PNat) : add (add (add (add (pred m) zero) (pred (succ m))) (add zero zero)) zero = add (pred m) m := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0329 : pred (succ (pred (succ (succ (succ (pred zero)))))) = succ (succ zero) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0330 (n : PNat) : add (pred (succ (add n zero))) zero = n := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0331 (n : PNat) (m : PNat) : add (add (succ (pred (succ m))) zero) n = add (succ m) n := by
  rw [add_zero]
  rw [pred_succ]

theorem t0332 (n : PNat) : pred (pred (succ (pred (add (pred (succ (add n zero))) (succ zero))))) = pred (pred (succ (pred (succ (add n zero))))) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0333 (n : PNat) : pred (add (pred (add n (succ zero))) zero) = pred n := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0334 : pred (succ zero) = add zero zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0335 : pred (succ (add (add (add zero zero) zero) zero)) = add (add zero zero) zero := by
  rw [add_zero]
  rw [pred_succ]

theorem t0336 : add (add zero (pred (succ zero))) zero = pred (succ zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0337 (n : PNat) : add (pred (pred (succ (succ (add (pred (pred n)) n))))) zero = add (pred (pred n)) n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0338 : pred (succ (add (pred (pred (succ (add (succ zero) zero)))) zero)) = pred (succ (pred zero)) := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0339 (m : PNat) : pred (add (pred (pred (succ (succ (succ m))))) zero) = m := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0340 (n : PNat) : pred (pred (succ (add n (add (succ (add (pred zero) zero)) (add zero zero))))) = add (add (pred (succ n)) zero) zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0341 : pred (succ (add (pred zero) (succ (pred (succ zero))))) = succ zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0342 (k : PNat) : add (add (pred (succ (add zero k))) zero) (pred (succ zero)) = add zero k := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0343 : pred (succ (pred (succ zero))) = add zero zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0344 : pred (succ (pred zero)) = add zero zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]

theorem t0345 (n : PNat) : add (add n (add zero zero)) zero = n := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0346 : add (pred (succ zero)) (add zero zero) = pred (succ zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0347 : add (pred zero) zero = pred zero := by
  rw [add_zero]

theorem t0348 (k : PNat) : pred (pred (succ (succ k))) = k := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0349 (n : PNat) : add (succ (pred (succ (add (add zero n) zero)))) (pred (succ (add (add (pred (succ n)) (pred zero)) zero))) = add (succ (pred (succ (add (pred zero) n)))) (add n zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0350 (n : PNat) : add (pred (succ (add (add (pred (succ (pred (succ n)))) (add zero zero)) zero))) zero = pred (succ (pred (succ (add n zero)))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0351 : add (add zero zero) (pred (add (add zero (succ (pred (succ zero)))) zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0352 : succ (pred (pred (succ (succ zero)))) = succ (pred (succ zero)) := by
  rw [pred_succ]

theorem t0353 (m : PNat) : pred (pred (succ (add (add (pred (add (succ m) (pred zero))) (succ zero)) zero))) = pred (add (add (succ m) zero) zero) := by
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0354 (n : PNat) : add (add (add (pred (pred (succ (succ n)))) (pred (succ zero))) zero) zero = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0355 : pred (succ (pred (succ (pred (add (succ zero) zero))))) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0356 : add (pred (succ (pred (succ zero)))) zero = add zero zero := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0357 : pred (pred (succ (succ zero))) = add zero zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0358 : pred (succ (pred (succ (pred (pred (succ (succ (pred (succ (pred (pred (succ zero)))))))))))) = pred (succ (add (pred zero) zero)) := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0359 : add (pred (succ (add (pred (succ zero)) zero))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0360 (n : PNat) : add (pred (pred (succ (pred (succ (add (pred (succ zero)) (pred (succ zero)))))))) n = add (pred (succ zero)) (add (add n zero) zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]

theorem t0361 : pred (pred (succ (add (succ (pred zero)) zero))) = pred (succ (pred (succ zero))) := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0362 : add (add (add zero zero) (add (pred zero) zero)) zero = zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0363 : pred (add zero (succ zero)) = zero := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0364 : pred (add (pred (pred (succ zero))) (succ zero)) = pred (add zero zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0365 : add (pred (add zero (succ zero))) (pred (pred (succ (add (succ (pred zero)) zero)))) = zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0366 (n : PNat) : add (pred (succ (add (pred (add (succ n) zero)) zero))) zero = n := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0367 (n : PNat) : add n zero = n := by
  rw [add_zero]

theorem t0368 : pred (succ (pred (succ (add (pred (succ (add (add (add zero zero) zero) zero))) (add zero zero))))) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0369 : add (add zero (add zero zero)) zero = pred zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0370 (n : PNat) : pred (succ (add (pred (succ n)) zero)) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0371 (n : PNat) : pred (succ (add (pred (succ (pred (succ n)))) zero)) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0372 : pred (add (pred (add (add (succ zero) zero) zero)) zero) = pred (add zero zero) := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0373 : add (add (pred zero) zero) (pred (succ zero)) = add zero (pred zero) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0374 : add (pred (pred zero)) (add zero zero) = zero := by
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0375 : pred (succ (add (pred (succ (add zero zero))) (add zero zero))) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0376 (k : PNat) : add (pred (add (add (pred (pred (succ k))) zero) zero)) zero = pred (pred k) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0377 : succ (add (add zero zero) zero) = pred (succ (succ zero)) := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0378 : succ (add (add zero (pred (succ zero))) zero) = succ zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0379 (n : PNat) : add (pred (succ (pred (succ (pred (pred (pred (succ (pred (add (succ n) zero)))))))))) (add zero zero) = pred (pred n) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0380 (n : PNat) : add (add n zero) (add (add (add zero zero) zero) zero) = pred (succ (pred (succ n))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0381 : add (add (add zero (pred (pred (succ (pred (succ (succ zero))))))) zero) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0382 (n : PNat) (m : PNat) : succ (pred (succ (pred (succ (add (pred n) (pred (succ m))))))) = succ (add (pred n) m) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0383 (k : PNat) : add (add k (pred (succ (pred (succ k))))) (add zero zero) = add k k := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0384 : pred (pred (add (pred (succ (add (succ zero) zero))) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0385 : pred (succ (add (succ (succ zero)) zero)) = succ (succ (pred zero)) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0386 (n : PNat) : succ (add (add (pred (add (add n zero) (succ zero))) zero) zero) = succ n := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0387 (m : PNat) : pred (pred (succ (pred (pred (succ m))))) = pred (pred (pred (succ m))) := by
  rw [pred_succ]

theorem t0388 (n : PNat) : succ (pred (succ (add (pred (succ n)) (pred (succ (pred (succ n))))))) = succ (add n n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0389 (m : PNat) : pred (succ (pred (pred (add m (pred (pred (succ (succ zero)))))))) = pred (pred m) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0390 (k : PNat) : pred (pred (succ (pred (succ (pred (succ (add (pred (succ (succ (pred (succ k))))) zero))))))) = k := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0391 : pred (succ (add (pred (succ (add zero zero))) zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0392 (m : PNat) : add (pred (succ (pred (succ (pred (add (add (succ m) zero) zero)))))) (pred m) = add m (pred m) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0393 (n : PNat) : pred (succ n) = n := by
  rw [pred_succ]

theorem t0394 : pred (pred (succ (succ (pred (succ zero))))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0395 : pred (succ zero) = zero := by
  rw [pred_succ]

theorem t0396 (m : PNat) : add (add (add m zero) (pred (add (add (succ zero) (add zero zero)) (pred (succ zero))))) zero = m := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0397 (n : PNat) : add (pred (succ n)) (add (pred (succ zero)) zero) = add n (pred (succ zero)) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0398 : pred (pred (succ (add (succ (add zero zero)) zero))) = zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0399 (n : PNat) : pred (succ (add (succ (add n zero)) (pred (succ (succ zero))))) = succ (succ n) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0400 : pred (succ (pred (pred (succ (add zero zero))))) = pred (succ (pred (succ zero))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0401 (n : PNat) : pred (succ (add (add (add (pred (succ (add n zero))) n) (pred n)) zero)) = add (add n n) (pred n) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0402 (k : PNat) : pred (succ (add k zero)) = pred (succ k) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0403 (n : PNat) : pred (succ (pred (succ (add (add (add n (pred (succ zero))) zero) zero)))) = add (add (pred (succ n)) zero) zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0404 (n : PNat) : add (succ (add (pred (succ (pred (succ n)))) zero)) zero = pred (succ (pred (succ (succ n)))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0405 : pred (pred (succ (succ zero))) = zero := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0406 : succ (add (add zero (succ (add (pred (succ zero)) zero))) zero) = succ (succ zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0407 : add zero (add zero zero) = zero := by
  rw [add_zero]
  rw [add_zero]

theorem t0408 (n : PNat) : pred (add (succ (pred (succ (add (pred (succ (add (add n zero) zero))) zero)))) zero) = n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0409 (n : PNat) : pred (pred (succ (add (pred (succ (pred (pred (succ (succ (pred (add n zero)))))))) (add zero zero)))) = pred (pred n) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0410 (n : PNat) : pred (succ (pred (add (add (pred (succ n)) zero) zero))) = pred (add (add n zero) zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0411 : add zero zero = zero := by
  rw [add_zero]

theorem t0412 : add (pred zero) (pred (succ zero)) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0413 : add (pred (succ (pred zero))) (pred (pred (succ (add zero (pred zero))))) = zero := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]

theorem t0414 (n : PNat) : succ (succ (add (add n zero) (add (add (add (add zero zero) zero) zero) zero))) = succ (succ n) := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0415 : pred (succ (pred zero)) = zero := by
  rw [pred_succ]
  rw [pred_zero]

theorem t0416 : add (add (add (pred zero) zero) zero) (succ zero) = succ (pred (succ (pred zero))) := by
  rw [add_succ]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0417 : pred (add (add zero zero) (succ zero)) = zero := by
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0418 (m : PNat) : add (pred (succ (pred (succ (pred (succ m)))))) (pred zero) = m := by
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0419 (n : PNat) : add (add (pred (succ (succ (pred (succ (pred n)))))) zero) zero = succ (pred n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0420 : pred (add (add zero zero) zero) = add zero zero := by
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0421 : pred (pred (succ (succ (add zero zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0422 (n : PNat) : add (pred (succ (add (pred n) n))) zero = add (pred n) n := by
  rw [add_zero]
  rw [pred_succ]

theorem t0423 (k : PNat) : pred (succ (pred (pred (pred (pred (succ (add k (succ zero)))))))) = pred (pred k) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0424 : pred (pred (add (add zero zero) (succ zero))) = zero := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0425 (n : PNat) : add (add (pred (succ n)) (pred (succ (add zero zero)))) zero = pred (succ (pred (succ n))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0426 (m : PNat) : pred (pred (pred (succ (succ (add (add (pred (succ (pred (succ m)))) zero) (add zero zero)))))) = pred m := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0427 : add (add (pred (succ zero)) (pred zero)) (add (pred (succ (add zero zero))) zero) = pred (succ (pred (add zero zero))) := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0428 : add (pred (succ zero)) (add (add zero zero) zero) = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0429 : add zero (succ zero) = pred (succ (succ zero)) := by
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]

theorem t0430 : succ (add (pred (succ zero)) (pred (succ (pred zero)))) = succ zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0431 : succ (pred (succ (pred (succ (add (succ (pred (succ (pred (succ zero))))) zero))))) = succ (succ zero) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0432 : add (pred (succ (pred (pred (succ zero))))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0433 : pred (succ (add (pred (succ (pred (succ zero)))) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0434 : pred (pred (succ (succ (pred (succ (add (pred (add (succ zero) zero)) zero)))))) = add zero (pred (pred (succ (succ zero)))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0435 : add (pred (succ (add (add (succ zero) zero) zero))) zero = succ zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0436 (n : PNat) : pred (pred (succ (succ (pred (succ (add n zero)))))) = pred (succ (pred (succ n))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0437 : pred (succ (succ (add (pred (succ (add zero zero))) zero))) = succ zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0438 : add (add (pred (add (succ (pred (pred (succ zero)))) zero)) zero) zero = pred (succ (add zero (pred (succ zero)))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0439 : add (pred (succ (pred (succ zero)))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0440 (n : PNat) : pred (succ (add (pred (add (succ (pred (succ (add (pred (succ n)) zero)))) zero)) zero)) = pred (succ (add n (pred (succ zero)))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0441 : add zero (add (pred (succ zero)) (succ zero)) = succ zero := by
  rw [add_succ]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0442 : pred (add (pred (succ (add zero (pred zero)))) (pred zero)) = zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0443 : add (add zero zero) zero = pred (succ zero) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0444 (n : PNat) : pred (add (succ (pred (succ n))) zero) = pred (succ n) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0445 : add (pred (pred (pred (succ (succ zero))))) zero = zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]

theorem t0446 : pred (add (add zero (succ zero)) (succ zero)) = succ zero := by
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0447 : add zero (pred zero) = zero := by
  rw [pred_zero]
  rw [add_zero]

theorem t0448 (n : PNat) : pred (succ (pred (succ (pred (add n (succ zero)))))) = n := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0449 : add (pred (succ (add (add zero zero) (pred zero)))) (pred (pred (pred (succ (succ zero))))) = zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_zero]
  rw [add_zero]

theorem t0450 : pred (succ (pred (succ (pred (succ (pred (pred (pred (succ (add zero (succ zero))))))))))) = zero := by
  rw [pred_succ]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0451 : add (pred (succ zero)) (pred (succ (add zero zero))) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0452 : pred (succ (add (pred (pred (succ zero))) zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]

theorem t0453 (n : PNat) : pred (succ (add (pred (succ (pred (succ (pred n))))) zero)) = pred (succ (pred (succ (pred n)))) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0454 : pred (succ (succ (add zero (add (pred (pred (succ (succ (pred (succ (pred zero))))))) zero)))) = succ zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0455 : add (pred (succ (succ (pred (succ zero))))) zero = succ zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0456 (n : PNat) : pred (succ (pred (succ (add (pred (succ n)) zero)))) = pred (pred (succ (succ n))) := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0457 (n : PNat) : pred (pred (succ (add (pred (succ (pred (succ n)))) (pred (succ (pred zero)))))) = pred n := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0458 : pred (pred (succ (succ (pred zero)))) = zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0459 (n : PNat) : add (add (add (pred (succ (pred (succ (add n zero))))) zero) zero) zero = add (pred (succ (add n zero))) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0460 : pred (add (add zero (pred (succ zero))) zero) = add (add zero zero) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]

theorem t0461 : succ (pred (pred (succ (succ (pred (pred zero)))))) = succ zero := by
  rw [pred_succ]
  rw [pred_zero]
  rw [pred_zero]
  rw [pred_succ]

theorem t0462 (m : PNat) : add zero (add (pred (succ (pred (succ (pred (pred (succ (pred (add (succ (succ (add m zero))) zero))))))))) zero) = add (add zero (pred (succ (add m zero)))) (pred (succ zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0463 : pred (pred (succ (succ (add (pred (succ (pred (succ zero)))) zero)))) = pred (succ (pred zero)) := by
  rw [add_zero]
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0464 (n : PNat) : pred (pred (pred (add (succ (succ (pred (add (succ n) (pred zero))))) zero))) = pred n := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0465 (n : PNat) : pred (succ (pred (succ n))) = n := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0466 (n : PNat) : add zero (pred (succ (pred (succ n)))) = add (add zero n) zero := by
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0467 (n : PNat) : add (pred (succ (pred (pred (succ (succ n)))))) zero = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0468 : pred (succ (succ (add (succ zero) zero))) = succ (succ zero) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0469 (n : PNat) : pred (pred (succ (succ (succ (succ (pred (succ n))))))) = succ (pred (succ (succ n))) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0470 : add (succ (succ (add (pred (succ (pred (pred (succ (pred (succ (succ (succ zero))))))))) zero))) zero = succ (succ (succ zero)) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0471 (n : PNat) : pred (pred (add (pred (succ n)) (succ zero))) = pred n := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0472 (n : PNat) : add n (add zero zero) = n := by
  rw [add_zero]
  rw [add_zero]

theorem t0473 (n : PNat) : pred (succ n) = add n zero := by
  rw [pred_succ]
  rw [add_zero]

theorem t0474 : add (pred (succ (pred (add (add (succ (succ (succ (add (add zero (add zero zero)) (succ (succ zero)))))) zero) zero)))) zero = succ (succ (add (add (add (pred (succ zero)) zero) zero) (succ (succ zero)))) := by
  rw [add_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0475 (n : PNat) : pred (succ (add (pred (succ zero)) (pred (pred (succ n))))) = add zero (pred (pred (succ n))) := by
  rw [pred_succ]
  rw [pred_succ]

theorem t0476 : add (add (add (pred (succ zero)) zero) zero) (add zero zero) = pred (succ (pred (succ zero))) := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0477 : pred (add (succ (add (add zero (pred (succ zero))) zero)) (add zero zero)) = zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]

theorem t0478 (n : PNat) : pred (add (succ (add (add n n) (add zero zero))) zero) = add n n := by
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0479 (n : PNat) (m : PNat) : pred (succ (add (add (pred (succ (pred (succ m)))) zero) (add n zero))) = add m n := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]

theorem t0480 : pred (add (add (pred (succ (succ (pred zero)))) zero) (pred (succ zero))) = pred (succ (add (pred zero) zero)) := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0481 (n : PNat) : add (pred (pred (succ (add (pred n) zero)))) zero = pred (pred n) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]

theorem t0482 : add (add (pred (add zero zero)) (add (succ zero) zero)) zero = succ zero := by
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0483 (n : PNat) : pred (pred (succ (succ (pred (succ n))))) = n := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0484 (n : PNat) : pred (pred (succ (succ (add (pred (succ n)) zero)))) = pred (succ (pred (succ n))) := by
  rw [add_zero]
  rw [pred_succ]

theorem t0485 (n : PNat) : pred (succ (add (add (add n (pred zero)) zero) zero)) = pred (succ (pred (succ n))) := by
  rw [pred_zero]
  rw [add_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0486 (n : PNat) : pred (succ (add (pred (pred (succ (add n (succ zero))))) zero)) = n := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0487 : pred (add (pred (succ (pred (succ zero)))) (succ zero)) = add (pred zero) zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]

theorem t0488 : pred (succ (add (add (pred (succ zero)) (add zero zero)) zero)) = add (add zero zero) zero := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0489 : pred (add (succ (add zero zero)) zero) = add zero zero := by
  rw [add_zero]
  rw [pred_succ]

theorem t0490 (n : PNat) : add (pred (succ n)) zero = n := by
  rw [add_zero]
  rw [pred_succ]

theorem t0491 (n : PNat) : add (pred (succ (succ (succ n)))) (pred (succ zero)) = succ (succ n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0492 (n : PNat) : pred (pred (succ (pred (pred (succ (succ (succ (add n (pred (succ zero)))))))))) = add (add n zero) (pred zero) := by
  rw [add_zero]
  rw [pred_succ]
  rw [pred_zero]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0493 (m : PNat) : pred (add (add (pred m) zero) (succ zero)) = pred m := by
  rw [add_zero]
  rw [add_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0494 (m : PNat) : pred (succ (add (add (pred (succ (pred (succ (pred (succ m)))))) (succ zero)) zero)) = succ m := by
  rw [add_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [add_zero]
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0495 (n : PNat) : succ (add n (pred (succ (pred (succ (pred (succ n))))))) = succ (add n n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [pred_succ]

theorem t0496 : add zero (add (succ zero) zero) = add (succ zero) zero := by
  rw [add_zero]
  rw [add_succ]
  rw [add_zero]

theorem t0497 : add (add (succ (add zero (add zero zero))) (pred (succ (pred (succ zero))))) zero = add (add (succ zero) zero) (pred (succ zero)) := by
  rw [pred_succ]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]
  rw [add_zero]

theorem t0498 : add (pred zero) (pred (succ zero)) = zero := by
  rw [pred_zero]
  rw [pred_succ]
  rw [add_zero]

theorem t0499 (n : PNat) (m : PNat) : add (pred (succ (pred (succ (succ (add m n)))))) zero = succ (add m n) := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]

theorem t0500 : pred (succ (add (pred (succ zero)) (pred (succ zero)))) = zero := by
  rw [pred_succ]
  rw [pred_succ]
  rw [add_zero]
