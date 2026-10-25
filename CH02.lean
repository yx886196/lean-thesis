import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

/-!
# 第 2 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。
-/

theorem ch02_demo (x : ℝ) : x * 0 = 0 := by
  ring

theorem ch02_demo2 (x y : ℝ) : x - y = x + -y := by
  ring
