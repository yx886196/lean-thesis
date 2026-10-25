import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

/-!
# 第 1 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。

注意：这里刻意只导入需要的模块（而不是整包 `import Mathlib`），
这样 VS Code 的 Lean 服务器只需加载几百 MB 而非 6 GB，响应快很多。
写真实内容时如需更多数学内容，再按需补充 import。
-/

example (x : ℝ) : x + 0 = x := by ring

theorem ch01_demo (x y : ℝ) : (x + y) ^ 2 = x ^ 2 + 2 * x * y + y ^ 2 := by
  ring
