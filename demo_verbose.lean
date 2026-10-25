import Mathlib.Data.Real.Basic
import Verbose.English.All

open Verbose English

Example "Squares are nonnegative"
  Given: (x : ℝ)
  Assume:
  Conclusion: x ^ 2 ≥ 0
Proof:
  positivity
QED
