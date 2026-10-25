
<!-- source: CH01.lean -->

# 第 1 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。

注意：这里刻意只导入需要的模块（而不是整包 `import Mathlib`），
这样 VS Code 的 Lean 服务器只需加载几百 MB 而非 6 GB，响应快很多。
写真实内容时如需更多数学内容，再按需补充 import。

### 定理：`ch01_demo`

```lean
theorem ch01_demo (x y : ℝ) : (x + y) ^ 2 = x ^ 2 + 2 * x * y + y ^ 2 := by
  ring
```


<!-- source: CH02.lean -->

# 第 2 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。

### 定理：`ch02_demo`

```lean
theorem ch02_demo (x : ℝ) : x * 0 = 0 := by
  ring
```

### 定理：`ch02_demo2`

```lean
theorem ch02_demo2 (x y : ℝ) : x - y = x + -y := by
  ring
```


<!-- source: CH03.lean -->

# 第 3 章

占位文件 —— 原项目中此文件为教材正文，此处仅用于验证环境可用。

### 定理：`ch03_demo`

```lean
theorem ch03_demo (x : ℝ) (h : x ≥ 0) : x + 1 ≥ 1 := by
  linarith
```


<!-- source: demo_verbose.lean -->

### 例：One plus one is two

**给定**：(_ : ℝ)

**求证**：(1 : ℝ) + 1 = 2

**证明**：

```lean
norm_num
```

### 例：Squares are nonnegative

**给定**：(x : ℝ)

**求证**：x ^ 2 ≥ 0

**证明**：

```lean
positivity
```
