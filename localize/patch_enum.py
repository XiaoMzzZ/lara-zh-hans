# -*- coding: utf-8 -*-
"""Wrap enum display values with L() so their raw values (used as tags / storage keys)
stay untouched."""

PATCHES = [
    ("lara/views/app/settings/SettingsView.swift", [
        ("Text(method.rawValue).tag(method)", "Text(L(method.rawValue)).tag(method)"),
        ("Text(mode.rawValue).tag(mode)", "Text(L(mode.rawValue)).tag(mode)"),
    ]),
    ("lara/views/tweaks/CardView.swift", [
        ("Text(option.rawValue).tag(Optional(option))", "Text(L(option.rawValue)).tag(Optional(option))"),
    ]),
    ("lara/views/tweaks/FontPicker.swift", [
        ("Text(target.rawValue).tag(target)", "Text(L(target.rawValue)).tag(target)"),
    ]),
    ("lara/views/tweaks/ToolsView.swift", [
        ("Text(tokenClass.label).tag(tokenClass)", "Text(L(tokenClass.label)).tag(tokenClass)"),
    ]),
]

fail = 0
for path, pairs in PATCHES:
    src = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in src:
            print(f"MISS  {path}: {old[:70]}")
            fail += 1
            continue
        src = src.replace(old, new)
    open(path, "w", encoding="utf-8", newline="").write(src)
    print(f"OK    {path}")
print("failures:", fail)
