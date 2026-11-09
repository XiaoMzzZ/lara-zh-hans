#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
精确逻辑键比对（无启发式，无误报）。

只抽取**明确无疑的逻辑位置**上的字符串字面量，逐文件对比 baseline 与 lara 的集合：
  A. == "x"  /  != "x"
  B. .tag("x")
  C. forKey: "x"  /  @AppStorage("x")
  D. key: "x"
  E. case "x"
  F. 字典字面量的键   ["x": ...]  或  , "x": ...
  G. 以 / 开头的路径
  H. 以 com.apple 开头的 bundle id
  I. URL(fileURLWithPath: "x")

任何一处集合差异即为 FAIL。
"""

import io
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402

# (正则作用于字面量之前的文本, 名称)
BEFORE_PATTERNS = [
    (re.compile(r"==\s*$"), "EQ"),
    (re.compile(r"!=\s*$"), "NEQ"),
    (re.compile(r"\.tag\(\s*$"), "TAG"),
    (re.compile(r"forKey:\s*$"), "FORKEY"),
    (re.compile(r"@AppStorage\(\s*$"), "APPSTORAGE"),
    (re.compile(r"\bkey:\s*$"), "KEY"),
    (re.compile(r"\bcase\s*$"), "CASE"),
    (re.compile(r"URL\(fileURLWithPath:\s*$"), "URLPATH"),
    (re.compile(r"\[\s*$"), "DICTKEY_OPEN"),
]


def inside_bracket(before):
    """判断该位置是否处于未闭合的 [ 之内（同一行）。"""
    return before.count("[") > before.count("]")


def extract_keys(path):
    """返回 {literal: set(标签)}"""
    out = defaultdict(set)
    for line in io.open(path, encoding="utf-8").read().split("\n"):
        for content, s, e in literals_in_line(line):
            before = line[:s].rstrip()
            after = line[e:]
            tags = set()
            for rx, name in BEFORE_PATTERNS:
                if rx.search(before):
                    tags.add(name)
            # 字典键：处于 [ ] 内，且后面紧跟冒号，且不在三元表达式里
            if inside_bracket(before) and re.match(r"^\s*:", after) and "?" not in before[-40:]:
                tags.add("DICTKEY")
            # 内容特征
            if content.startswith("/"):
                tags.add("PATH")
            if content.startswith("com.apple"):
                tags.add("BUNDLEID")
            if tags:
                out[content] |= tags
    return out


def main():
    problems = []
    total = 0
    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            bk = extract_keys(os.path.join("baseline", rel))
            lk = extract_keys(lp)
            total += len(bk)
            for lit, tags in bk.items():
                if lit not in lk:
                    problems.append((rel, sorted(tags), lit))
                else:
                    lost = tags - lk[lit]
                    if lost:
                        problems.append((rel, sorted(lost), lit))

    print("logic-key literals in baseline: %d" % total)
    if problems:
        print("\n!!! %d LOGIC KEY(S) CHANGED !!!\n" % len(problems))
        for rel, tags, lit in problems:
            print("  %s  [%s]  %r" % (rel, ",".join(tags), lit[:110]))
    else:
        print("RESULT: PASS — all logic-key literals preserved verbatim")


if __name__ == "__main__":
    main()
