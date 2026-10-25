import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

/-!
# Chapter 1: Limits of real sequences

This file is the formal counterpart of the blueprint in `blueprint/src/content.tex`.
Every definition and theorem here is referenced from the blueprint with
`\lean{...}` and marked as formalized with `\leanok`.
-/

/-- A sequence `u : ℕ → ℝ` **converges** to `l` if for every `ε > 0`
there is `N` such that `|u n - l| ≤ ε` for all `n ≥ N`. -/
def ConvergesTo (u : ℕ → ℝ) (l : ℝ) : Prop :=
  ∀ ε > 0, ∃ N : ℕ, ∀ n ≥ N, |u n - l| ≤ ε

/-- A constant sequence converges to its value. -/
theorem convergesTo_const (l : ℝ) : ConvergesTo (fun _ => l) l := by
  intro ε hε
  refine ⟨0, ?_⟩
  intro n _
  simpa using le_of_lt hε

/-- Binomial expansion, used as a toy example of a formalized identity. -/
theorem ch01_demo (x y : ℝ) : (x + y) ^ 2 = x ^ 2 + 2 * x * y + y ^ 2 := by
  ring
