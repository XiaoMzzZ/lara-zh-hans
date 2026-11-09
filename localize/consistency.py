#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译一致性检查：同一英文原文是否被译成了不同中文。"""

import io
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402


def main():
    mapping = defaultdict(set)      # english -> {chinese}
    where = defaultdict(list)

    # 同一英文在不同语境下应有不同译法，属正确行为
    EXCEPTIONS = {
        # "Clear" 在 VarClean 是「清除选择」，在 ContentView 是「清空日志」
        "Clear": {"取消全选", "清空"},
    }

    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            b = io.open(os.path.join("baseline", rel), encoding="utf-8").read().split("\n")
            l = io.open(lp, encoding="utf-8").read().split("\n")
            if len(b) != len(l):
                continue
            for idx, (bl, ll) in enumerate(zip(b, l), 1):
                if bl == ll:
                    continue
                bs = [x[0] for x in literals_in_line(bl)]
                ls = [x[0] for x in literals_in_line(ll)]
                if len(bs) != len(ls):
                    continue
                for o, nw in zip(bs, ls):
                    if o == nw:
                        continue
                    if not any("\u4e00" <= ch <= "\u9fff" for ch in nw):
                        continue
                    mapping[o].add(nw)
                    where[(o, nw)].append("%s:%d" % (rel, idx))

    conflicts = {k: v for k, v in mapping.items()
                 if len(v) > 1 and EXCEPTIONS.get(k) != v}
    print("distinct english sources: %d" % len(mapping))
    if conflicts:
        print("\n!!! %d SOURCE(S) WITH INCONSISTENT TRANSLATIONS !!!\n" % len(conflicts))
        for eng, zhs in sorted(conflicts.items()):
            print("  EN: %r" % eng[:110])
            for z in zhs:
                print("      -> %r   (%s)" % (z[:110], ", ".join(where[(eng, z)][:3])))
    else:
        print("RESULT: PASS — every english source maps to exactly one chinese translation")


if __name__ == "__main__":
    main()
