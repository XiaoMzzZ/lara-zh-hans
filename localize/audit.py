#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键审计：运行全部检查，按各自的明确结论判定通过与否。"""

import os
import subprocess
import sys

# (标题, 命令, 判定通过的关键字, 判定失败的关键字)
CHECKS = [
    ("Swift 词法分析（字符串/注释/括号）",
     ["localize/lexcheck.py", "lara"],
     "all files lex cleanly", "FILE(S) WITH LEX ERRORS"),

    ("逻辑键字面量原样保留",
     ["localize/keycheck.py"],
     "RESULT: PASS", "LOGIC KEY(S) CHANGED"),

    ("逐对验证插值 / 格式符 / 转义",
     ["localize/deeppair.py"],
     "RESULT: PASS", "ISSUE(S)"),

    ("字符串字面量数量（仅新增文件可变化）",
     ["localize/countcheck.py"],
     None, None),          # 单独处理

    ("L() 字典覆盖率（dirtyZero）",
     ["localize/check_dict.py"],
     "missing: 0", "MISS "),

    ("L() 字典覆盖率（全部枚举）",
     ["localize/enumcheck.py"],
     "RESULT: PASS", "MISS"),

    ("翻译一致性",
     ["localize/consistency.py"],
     "RESULT: PASS", "INCONSISTENT"),

    ("结构平衡（对比基线）",
     ["localize/verify.py"],
     "structural issues: 0", "structural issues: [1-9]"),
]


def run(cmd):
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return (p.stdout or "") + (p.stderr or "")


def main():
    results = []
    for title, cmd, ok_marker, fail_marker in CHECKS:
        print("\n" + "=" * 76)
        print(title)
        print("=" * 76)
        out = run(cmd)
        print(out.rstrip())

        if ok_marker is None:
            # countcheck：只有 Localization.swift 允许新增
            bad = [ln for ln in out.split("\n")
                   if ln.strip() and "Localization.swift" not in ln
                   and ("+" in ln or "-" in ln) and "file " not in ln
                   and not ln.startswith("---") and not ln.startswith("net delta")
                   and not ln.startswith("files with")]
            st = "FAIL" if bad else "PASS"
        elif fail_marker and fail_marker in out:
            st = "FAIL"
        elif ok_marker in out:
            st = "PASS"
        else:
            st = "UNKNOWN"
        results.append((title, st))

    print("\n" + "=" * 76)
    print("审计汇总")
    print("=" * 76)
    for title, st in results:
        print("  [%-7s] %s" % (st, title))
    npass = sum(1 for _, s in results if s == "PASS")
    print("\n%d/%d 通过" % (npass, len(results)))
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
