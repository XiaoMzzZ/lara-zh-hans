# -*- coding: utf-8 -*-
import os, sys, json

BASE = "baseline"
NEW = "lara"

def stats(path):
    s = open(path, encoding="utf-8").read()
    return {
        "braces": s.count("{") - s.count("}"),
        "parens": s.count("(") - s.count(")"),
        "brackets": s.count("[") - s.count("]"),
        "quotes": s.count('"'),
        "lines": s.count("\n"),
    }

bad = 0
changed = 0
for dp, _, fs in os.walk(NEW):
    for f in fs:
        if not f.endswith(".swift"):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, NEW)
        old = os.path.join(BASE, rel)
        if not os.path.exists(old):
            print(f"NEW FILE  {rel}")
            continue
        a, b = stats(old), stats(p)
        if a["braces"] or a["parens"] or a["brackets"]:
            print(f"BASELINE IMBALANCE {rel}: {a}")
        if (a["braces"], a["parens"], a["brackets"]) != (b["braces"], b["parens"], b["brackets"]):
            print(f"STRUCT CHANGED {rel}: {a} -> {b}")
            bad += 1
        if a["quotes"] != b["quotes"]:
            print(f"QUOTE COUNT {rel}: {a['quotes']} -> {b['quotes']} ({b['quotes']-a['quotes']:+d})")
        if a["lines"] != b["lines"]:
            print(f"LINE COUNT {rel}: {a['lines']} -> {b['lines']}")
        changed += 1

print(f"\nchecked {changed} files, structural issues: {bad}")
