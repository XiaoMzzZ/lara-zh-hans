#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context-aware Chinese localization applier for lara.

Only string literals that sit in a *display* argument position get replaced,
so identifiers, UserDefaults keys, plist keys, paths and SF Symbol names that
happen to share the same English spelling are left untouched.
"""
import json, os, re, sys

ROOTS = ["lara/views", "lara/PartyUI", "lara/classes", "lara/funcs", "lara/lara.swift"]

# tokens that, when they immediately precede a literal, mean "this is shown to the user"
DISPLAY_TOKENS = [
    "Text(", "Button(", "Label(", "NavigationLink(", "Toggle(", "Picker(",
    "Section(", "TextField(", "SecureField(", "LabeledContent(",
    ".navigationTitle(", ".navigationBarTitle(", ".alert(", ".confirmationDialog(",
    "NSLocalizedString(",
    "HeaderLabel(text:", "PlainToggle(text:", "HeaderDropdown(text:",
    "PlainAlert(title:", "PlainAlert(text:",
    "title:", "body:", "actionLabel:", "message:", "placeholder:", "footer:", "text:", "description:", "prompt:",
]

def find_literals(src):
    """yield (start_index, end_index, literal) for every plain string literal"""
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            i = n if j == -1 else j
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c == '"':
            start = i + 1
            j = start
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == '"':
                    break
                j += 1
            yield (i, j, src[start:j])
            i = j + 1
            continue
        i += 1

def is_display_context(src, lit_start):
    window = src[max(0, lit_start - 160):lit_start]
    window = re.sub(r"\s+", " ", window).strip()
    for tok in DISPLAY_TOKENS:
        t = tok if tok.endswith(":") else tok
        if window.endswith(t):
            return True
        # allow "Label(\"x\"" style where window ends with the token plus a space
        if window.endswith(t.rstrip()):
            return True
    return False

def main():
    apply_changes = "--apply" in sys.argv
    mapping = {}
    for fn in sorted(os.listdir("localize")):
        if fn.startswith("zh_map") and fn.endswith(".json"):
            mapping.update(json.load(open(os.path.join("localize", fn), encoding="utf-8")))
    # longest first so that "Apply Tweaks" wins over "Apply"
    keys = sorted(mapping, key=len, reverse=True)
    changed_total = 0
    files_changed = 0
    report = []

    targets = []
    for root in ROOTS:
        if os.path.isfile(root):
            targets.append(root)
            continue
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.endswith(".swift"):
                    targets.append(os.path.join(dp, f))

    for path in targets:
        src = open(path, encoding="utf-8").read()
        out = []
        last = 0
        hits = 0
        for (s, e, lit) in find_literals(src):
            key = lit if lit in mapping else lit.replace('\\"', '"')
            if key not in mapping:
                continue
            if not is_display_context(src, s):
                continue
            zh = mapping[key]
            if "\\(" in key:
                # keep every interpolation segment exactly as-is
                interps = re.findall(r"\\\([^)]*\)", key)
                if any(x not in zh for x in interps):
                    report.append(f"SKIP interpolation mismatch: {path} :: {lit!r}")
                    continue
            if "--verbose" in sys.argv:
                line = src.count("\n", 0, s) + 1
                print(f"  {path}:{line}  {lit!r} -> {zh!r}")
            out.append(src[last:s + 1])
            out.append(zh)
            last = e
            hits += 1
        if hits:
            out.append(src[last:])
            new = "".join(out)
            files_changed += 1
            changed_total += hits
            report.append(f"{hits:3d}  {path}")
            if apply_changes:
                open(path, "w", encoding="utf-8", newline="").write(new)

    print("\n".join(report))
    print(f"\n{'APPLIED' if apply_changes else 'DRY-RUN'}: {changed_total} strings in {files_changed} files")

if __name__ == "__main__":
    main()
