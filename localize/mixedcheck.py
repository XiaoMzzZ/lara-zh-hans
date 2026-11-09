#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""质量检查 v2：剔除 \(...) 插值后再找中英混杂。"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402

ALLOW = set("""
VFS SBX Hybrid UUID JIT ASLR EDR OTA PID UID URL UTType PNG JPG JPEG IPA
SpringBoard MobileGestalt RemoteCall DarkBoard dirtyZero LaraJIT Pocket Poster
RespringCC LiveContainer DarkSword Darkboard
App Apple iOS iPadOS iPhone iPad Mac
CC BG DB plist json txt zip ttc ttf AirDrop Helvetica Wi-Fi Wi Fi
Cowabunga HelveticaNeue
""".split())
ALLOW_LOWER = {a.lower() for a in ALLOW}

INTERP = re.compile(r"\\\((?:[^()]|\([^()]*\))*\)")


def main():
    suspicious = []
    for dp, _, fs in os.walk("lara"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, "lara")
            for ln_no, line in enumerate(io.open(p, encoding="utf-8").read().split("\n"), 1):
                for content, s, e in literals_in_line(line):
                    if not any("\u4e00" <= ch <= "\u9fff" for ch in content):
                        continue
                    stripped = INTERP.sub(" ", content)     # 去掉插值
                    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", stripped)
                    bad = [w for w in words if w.lower() not in ALLOW_LOWER]
                    if bad:
                        suspicious.append((rel, ln_no, bad, content))

    print("mixed-language candidates (interpolation excluded): %d" % len(suspicious))
    for rel, ln, bad, content in suspicious:
        print("  %s:%d  %s" % (rel, ln, bad))
        print("      %s" % content[:160])


if __name__ == "__main__":
    main()
