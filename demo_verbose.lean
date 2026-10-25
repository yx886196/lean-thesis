import Mathlib.Data.Real.Basic
import Verbose.English.All

open Verbose English

Example "One plus one is two"
  Given: (_ : ℝ)
  Assume:
  Conclusion: (1 : ℝ) + 1 = 2
Proof:
  norm_num
QED

Example "Squares are nonnegative"
  Given: (x : ℝ)
  Assume:
  Conclusion: x ^ 2 ≥ 0
Proof:
  positivity
QED
