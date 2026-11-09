#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
逻辑键安全检查：找出 baseline 中处于「逻辑上下文」的字符串字面量，
确认它们在 lara 中**原样存在**。

逻辑上下文（这些位置的字符串一旦改动，功能必然受影响）：
  - 比较:        == "x"   != "x"
  - 字符串方法:  .contains("x") .hasPrefix("x") .hasSuffix("x")
  - switch:      case "x"
  - 持久化:      forKey: "x"   @AppStorage("x")
  - 字典键:      "x": value
  - plist 键:    key: "x"
  - 文件路径:    "/..."
  - bundle id:   "com.apple..."
  - 枚举 tag:    .tag("x")
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402

# 出现在字面量「之前」的上下文标记
LOGIC_BEFORE = [
    (re.compile(r"==\s*$"), "EQ"),
    (re.compile(r"!=\s*$"), "NEQ"),
    (re.compile(r"\.contains\(\s*$"), "CONTAINS"),
    (re.compile(r"\.hasPrefix\(\s*$"), "HASPREFIX"),
    (re.compile(r"\.hasSuffix\(\s*$"), "HASSUFFIX"),
    (re.compile(r"\bcase\s*$"), "CASE"),
    (re.compile(r"\bcase\s+.*,\s*$"), "CASE"),
    (re.compile(r"forKey:\s*$"), "FORKEY"),
    (re.compile(r"@AppStorage\(\s*$"), "APPSTORAGE"),
    (re.compile(r"\bkey:\s*$"), "KEY"),
    (re.compile(r"\.tag\(\s*$"), "TAG"),
    (re.compile(r"\bswitch\s+\w+\s*$"), "SWITCH"),
    (re.compile(r"\[[^\]]*$"), "DICT"),
]

# 出现在字面量「之后」的上下文标记
LOGIC_AFTER = [
    (re.compile(r"^\s*:"), "DICT_KEY"),
]


def classify(line, start, end):
    """返回该字面量所处的逻辑上下文标签列表。"""
    before = line[:start]
    after = line[end:]
    tags = []
    for rx, name in LOGIC_BEFORE:
        if rx.search(before):
            tags.append(name)
            break
    for rx, name in LOGIC_AFTER:
        if rx.search(after):
            tags.append(name)
            break
    # 内容自身特征
    raw = line[start:end]
    inner = raw[1:-1] if raw.startswith('"') and raw.endswith('"') else raw
    if inner.startswith("/"):
        tags.append("PATH")
    if inner.startswith("com.apple"):
        tags.append("BUNDLEID")
    if re.match(r"^[a-zA-Z0-9_]+\.[a-zA-Z0-9_.]+$", inner) and "/" not in inner:
        tags.append("DOTTED_ID")
    return tags


def main():
    problems = []
    checked = 0

    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            bsrc = io.open(os.path.join("baseline", rel), encoding="utf-8").read()
            lsrc = io.open(lp, encoding="utf-8").read()
            lset = set()
            for ln in lsrc.split("\n"):
                for content, s, e in literals_in_line(ln):
                    lset.add(content)

            for ln_no, line in enumerate(bsrc.split("\n"), 1):
                for content, s, e in literals_in_line(line):
                    tags = classify(line, s, e)
                    if not tags:
                        continue
                    checked += 1
                    if content not in lset:
                        problems.append((rel, ln_no, ",".join(tags), content))

    print("logic-context literals checked: %d" % checked)
    if problems:
        print("\n!!! %d LOGIC KEY(S) NO LONGER PRESENT VERBATIM !!!\n" % len(problems))
        for rel, ln, tags, content in problems:
            print("  %s:%d [%s]  %r" % (rel, ln, tags, content[:120]))
    else:
        print("RESULT: PASS — every logic-context literal is still present verbatim")


if __name__ == "__main__":
    main()
