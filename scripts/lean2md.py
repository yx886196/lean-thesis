#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lean2md.py —— 把 Lean 4 源文件转成可读的数学讲义（Markdown）

这是"Lean 代码 → 数学语言"这一半的落地工具。

提取规则
--------
1. `/-! ... -/`        模块文档  → 讲义正文（原样保留 Markdown）
2. `Example/Lemma/...` 受控自然语言块 → 定理陈述 + 证明
   - 把 Given / Assume / Conclusion 改写成"给定 / 假设 / 求证"
   - 证明部分保留 Lean 代码（可折叠），因为那本身就是一步步的推理
3. `theorem/example ... := by` 普通 Lean 声明 → 定理 + 代码块

用法
----
    python lean2md.py CH01.lean CH02.lean -o paper/handout.md
    python lean2md.py Chapters/ -o paper/handout.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------- 正则 ----------

MODULE_DOC = re.compile(r"/-!(.*?)-/", re.S)

VERBOSE_CMD = re.compile(
    r'^(?P<kind>Example|Exercise|Lemma|Exercise-lemma)\s+"(?P<title>[^"]*)"\s*$'
)

PLAIN_DECL = re.compile(
    r"^(?P<kind>theorem|lemma|example|def|noncomputable def)\s+(?P<name>[A-Za-z_][\w'.]*)?"
)

SECTION = {
    "given": ("**给定**", "Given"),
    "assume": ("**假设**", "Assume"),
    "conclusion": ("**求证**", "Conclusion"),
    "proof": ("**证明**", "Proof"),
}


def split_blocks(text: str):
    """把文件切成 (kind, content) 序列：doc / verbose / plain / other"""
    pos = 0
    out = []

    for m in MODULE_DOC.finditer(text):
        if m.start() > pos:
            out.append(("other", text[pos:m.start()]))
        out.append(("doc", m.group(1).strip("\n")))
        pos = m.end()
    if pos < len(text):
        out.append(("other", text[pos:]))

    # 在 other 段内部继续切出 verbose / plain 块
    result = []
    for kind, chunk in out:
        if kind != "other":
            result.append((kind, chunk))
            continue
        result.extend(_split_code(chunk))
    return result


def _split_code(chunk: str):
    lines = chunk.splitlines()
    buf = []
    pieces = []
    i = 0
    while i < len(lines):
        line = lines[i]
        vm = VERBOSE_CMD.match(line.strip())
        if vm:
            if buf:
                pieces.append(("other", "\n".join(buf)))
                buf = []
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip() == "QED":
                    i += 1
                    break
                i += 1
            pieces.append(("verbose", "\n".join(block)))
            continue

        pm = PLAIN_DECL.match(line)
        if pm and pm.group("name"):
            if buf:
                pieces.append(("other", "\n".join(buf)))
                buf = []
            block = [line]
            i += 1
            # 收集到空行且缩进结束为止（简易启发式）
            indented = False
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    block.append(nxt)
                    i += 1
                    if indented:
                        break
                    continue
                if nxt.startswith(" ") or nxt.startswith("\t"):
                    indented = True
                    block.append(nxt)
                    i += 1
                    continue
                break
            pieces.append(("plain", "\n".join(block).rstrip()))
            continue

        buf.append(line)
        i += 1

    if buf:
        pieces.append(("other", "\n".join(buf)))
    return pieces


def render_verbose(block: str) -> str:
    lines = block.splitlines()
    head = VERBOSE_CMD.match(lines[0].strip())
    title = head.group("title") if head else ""
    kind = head.group("kind") if head else "Example"

    sections: dict[str, list[str]] = {}
    order: list[str] = []
    cur = None

    for line in lines[1:]:
        s = line.strip()
        low = s.lower()
        matched = None
        for key, (_, en) in SECTION.items():
            if low.startswith(en.lower() + ":"):
                matched = key
                break
        if matched:
            cur = matched
            order.append(matched)
            sections.setdefault(cur, [])
            rest = s[len(SECTION[cur][1]) + 1:].strip()
            if rest:
                sections[cur].append(rest)
            continue
        if s == "QED":
            continue
        if cur:
            sections[cur].append(line.rstrip())

    out = []
    header = "### " + ("命题" if kind != "Example" else "例") + (f"：{title}" if title else "")
    out.append(header)
    out.append("")

    def emit(key: str, fence: bool = False):
        body = "\n".join(sections.get(key, [])).strip()
        if not body:
            return
        label = SECTION[key][0]
        if fence:
            out.append(f"{label}：")
            out.append("")
            out.append("```lean")
            out.append(body)
            out.append("```")
        else:
            out.append(f"{label}：{body}")
        out.append("")

    emit("given")
    emit("assume")
    emit("conclusion")
    emit("proof", fence=True)
    return "\n".join(out)


def render_plain(block: str) -> str:
    first = block.splitlines()[0].strip()
    m = PLAIN_DECL.match(first)
    name = m.group("name") if m and m.group("name") else ""
    kind = m.group("kind") if m else "theorem"
    label = {
        "theorem": "定理",
        "lemma": "引理",
        "example": "例",
        "def": "定义",
        "noncomputable def": "定义",
    }.get(kind, "声明")
    out = [f"### {label}" + (f"：`{name}`" if name else ""), ""]
    out += ["```lean", block.strip(), "```", ""]
    return "\n".join(out)


def convert(paths: list[Path]) -> str:
    parts = []
    for p in paths:
        parts.append(f"\n<!-- source: {p.name} -->\n")
        text = p.read_text(encoding="utf-8")
        for kind, chunk in split_blocks(text):
            if kind == "doc":
                parts.append(chunk)
                parts.append("")
            elif kind == "verbose":
                parts.append(render_verbose(chunk))
            elif kind == "plain":
                parts.append(render_plain(chunk))
    return "\n".join(parts)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--output", default="handout.md")
    args = ap.parse_args()

    files: list[Path] = []
    for item in args.inputs:
        p = Path(item)
        if p.is_dir():
            files.extend(sorted(p.glob("*.lean")))
        else:
            files.append(p)

    if not files:
        print("没有找到 .lean 文件")
        return 1

    md = convert(files)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"已生成 {out}（{len(files)} 个源文件，{len(md.splitlines())} 行）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
