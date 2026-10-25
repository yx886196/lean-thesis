import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-!
# 第 3 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。
-/

theorem ch03_demo (x : ℝ) (h : x ≥ 0) : x + 1 ≥ 1 := by
  linarith
