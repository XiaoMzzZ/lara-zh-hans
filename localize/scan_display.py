#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出所有处于「显示位置」但仍是英文的字面量。"""

import io
import os
import re

ROOT = "lara"

DISPLAY_TOKENS = [
    "Text(", "Button(", "Label(", "NavigationLink(", "Toggle(", "Picker(",
    "Section(", "TextField(", "LabeledContent(", ".navigationTitle(", ".alert(",
    "NSLocalizedString(", "HeaderLabel(text:", "PlainToggle(text:",
    "HeaderDropdown(text:", "PlainAlert(title:", "title:", "body:",
    "actionLabel:", "message:", "placeholder:", "footer:", "text:",
    "description:", "prompt:", "infoTitle:", "infoMessage:", "lastResult =",
    "errormsg =", "status =", "statusmsg =", "statusMessage =", "fixupMessage =",
]


def strip_comments(src):
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == '"':
                    break
                j += 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(" " * (j - i))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def find_literals(src):
    res = []
    i, n = 0, len(src)
    while i < n:
        if src[i] == '"':
            if src.startswith('"""', i):
                j = src.find('"""', i + 3)
                if j == -1:
                    break
                res.append((i, j + 3, src[i + 3:j]))
                i = j + 3
                continue
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == '"':
                    break
                j += 1
            res.append((i, j + 1, src[i + 1:j]))
            i = j + 1
        else:
            i += 1
    return res


def is_display_context(src, pos):
    window = src[max(0, pos - 180):pos]
    window = window.rstrip()
    for tok in DISPLAY_TOKENS:
        if window.endswith(tok):
            return True
    # Text(cond ? "a" : "b") 里的第二个分支
    tail = window[-200:]
    if re.search(r'\?\s*"[^"]*"\s*:\s*$', tail):
        return True
    if re.search(r'Text\([^()]*\?\s*$', tail):
        return True
    return False


def main():
    hits = []
    for dirpath, _, files in os.walk(ROOT):
        for fn in sorted(files):
            if not fn.endswith(".swift"):
                continue
            path = os.path.join(dirpath, fn)
            with io.open(path, encoding="utf-8") as f:
                raw = f.read()
            src = strip_comments(raw)
            for s, e, content in find_literals(src):
                if not re.search(r"[A-Za-z]{3,}", content):
                    continue
                if re.search(r"[\u4e00-\u9fff]", content):
                    continue
                if not is_display_context(src, s):
                    continue
                line = src.count("\n", 0, s) + 1
                hits.append((os.path.relpath(path, ROOT), line, content))
    for rel, line, content in hits:
        print("%s:%d\t%s" % (rel, line, content.replace("\n", "\\n")[:200]))
    print("---- display-context English left: %d ----" % len(hits))


if __name__ == "__main__":
    main()
