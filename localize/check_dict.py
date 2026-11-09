#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核对 Localization.swift 字典对 dirtyZero 名称的覆盖率。"""

import io
import re

src = io.open("lara/views/tweaks/dirtyZero/dirtyZeroTweakArray.swift", encoding="utf-8").read()
names = re.findall(r'ZeroTweak\(name: "([^"]*)"', src)
sections = re.findall(r'ZeroSection\(name: "([^"]*)"', src)

loc = io.open("lara/Localization.swift", encoding="utf-8").read()
keys = set(re.findall(r'^\s*"([^"]*)":\s*"', loc, re.M))

print("sections: %d" % len(sections))
for s in sections:
    if s not in keys:
        print("  MISS section: %r" % s)

print("tweaks: %d" % len(names))
miss = 0
for n in names:
    if n not in keys:
        miss += 1
        print("  MISS tweak: %r" % n)
print("missing: %d / %d" % (miss, len(names)))
