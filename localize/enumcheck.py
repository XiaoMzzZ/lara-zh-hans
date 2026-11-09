#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字典键与枚举 rawValue 逐字符比对，防止拼写不一致导致静默回退英文。"""

import io
import os
import re

LOC = "lara/Localization.swift"


def dict_keys():
    src = io.open(LOC, encoding="utf-8").read()
    return set(re.findall(r'^\s*"([^"]*)":\s*"', src, re.M))


ENUMS = [
    # (文件, 枚举名)
    ("lara/views/app/settings/SettingsView.swift", "method"),
    ("lara/views/app/settings/SettingsView.swift", "fmAppsDisplayMode"),
    ("lara/views/app/settings/SettingsView.swift", "logsdisplaymode"),
    ("lara/views/tweaks/CardView.swift", "replaceoption"),
    ("lara/views/tweaks/FontPicker.swift", "styletarget"),
    ("lara/classes/tweaks/darkboard/IconThemeGalleryManager.swift", "IconThemeGalleryFilter"),
]

# 有意不译：领域内通行的技术缩写，译成中文反而增加理解成本
KEEP_AS_IS = {
    "VFS",        # 漏洞利用方式名，全 UI 通用
    "SBX",        # 同上
    "UUID",       # 容器目录名格式
    "Bundle ID",  # 包标识符，开发者通用叫法
}


def enum_cases(path, name):
    src = io.open(path, encoding="utf-8").read()
    m = re.search(r"enum\s+%s\s*:[^{]*\{" % re.escape(name), src)
    if not m:
        return None
    body_start = m.end()
    depth = 1
    i = body_start
    while i < len(src) and depth > 0:
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
        i += 1
    body = src[body_start:i - 1]
    return re.findall(r'case\s+\w+\s*=\s*"([^"]*)"', body)


def main():
    keys = dict_keys()
    print("dictionary keys: %d\n" % len(keys))
    problems = 0
    for path, name in ENUMS:
        cases = enum_cases(path, name)
        if cases is None:
            print("  !! enum %s not found in %s" % (name, path))
            problems += 1
            continue
        print("  enum %-28s %d case(s)" % (name, len(cases)))
        for c in cases:
            if c in KEEP_AS_IS:
                print("       [KEEP] %r" % c)
                continue
            mark = "OK  " if c in keys else "MISS"
            if c not in keys:
                problems += 1
            print("       [%s] %r" % (mark, c))

    # 反向：字典里有没有永远不会用到的键（脏数据）
    all_cases = set()
    for path, name in ENUMS:
        for c in (enum_cases(path, name) or []):
            all_cases.add(c)
    print("\nmissing keys: %d" % problems)
    if problems == 0:
        print("RESULT: PASS — every enum rawValue displayed via L() has a dictionary entry")


if __name__ == "__main__":
    main()
