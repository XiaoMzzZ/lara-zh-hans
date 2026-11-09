#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
部分替换检查：
同一字符串在文件中出现多次时，若只有部分被翻译，
必须确认**保留下来的那几处**都是逻辑用途，被翻译的那几处都是显示用途。
"""

import io
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402
from riskcheck import is_display  # noqa: E402


def occurrences(path):
    """返回 [(line_no, content, is_display_ctx)]"""
    out = []
    for ln_no, line in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        for content, s, e in literals_in_line(line):
            out.append((ln_no, content, is_display(line, s)))
    return out


def main():
    found = []
    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            bocc = occurrences(os.path.join("baseline", rel))
            locc = occurrences(lp)
            bcnt = Counter(c for _, c, _ in bocc)
            lcnt = Counter(c for _, c, _ in locc)

            for content, nb in bcnt.items():
                nl = lcnt.get(content, 0)
                if nl == 0 or nl == nb:
                    continue          # 全改 或 全留 —— 前者已由 riskcheck 覆盖
                # 部分替换：检查 baseline 中每一处是否为显示用途
                bad = [(ln, d) for ln, c, d in bocc if c == content and not d]
                if bad:
                    found.append((rel, content, nb, nl, bad[:3]))

    print("partial-replacement cases with remaining logic occurrence: %d" % len(found))
    if found:
        print("\n!!! REVIEW THESE !!!\n")
        for rel, content, nb, nl, bad in found:
            print("  %s  (baseline %d -> lara %d)" % (rel, nb, nl))
            print("     literal: %r" % content[:110])
            print("     logic occurrences still at lines: %s" % [b[0] for b in bad])
    else:
        print("RESULT: PASS — no case where a logic occurrence survived while a display occurrence was translated")


if __name__ == "__main__":
    main()
