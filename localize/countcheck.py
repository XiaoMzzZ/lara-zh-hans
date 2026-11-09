#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐文件对比字符串字面量数量，任何变化都必须有解释。"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexcheck import lex_swift  # noqa: E402


def counts(root):
    out = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".swift"):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            with io.open(p, encoding="utf-8") as fh:
                src = fh.read()
            c, _ = lex_swift(src, p)
            out[rel] = c
    return out


b = counts("baseline")
l = counts("lara")

print("%-62s %6s %6s %6s" % ("file", "before", "after", "delta"))
print("-" * 84)
deltas = []
for rel in sorted(set(b) | set(l)):
    bc = b.get(rel, 0)
    lc = l.get(rel, 0)
    if bc != lc:
        deltas.append((rel, bc, lc, lc - bc))
        print("%-62s %6d %6d %+6d" % (rel, bc, lc, lc - bc))
print("-" * 84)
print("files with changed literal count: %d" % len(deltas))
print("net delta: %+d" % (sum(d[3] for d in deltas)))
