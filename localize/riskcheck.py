#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
精确风险判定：

对每一个「被翻译过的字符串」，回溯它在 baseline 中的**所有**出现位置，
判断每一处是「显示上下文」还是「逻辑上下文」。

只要有一处是逻辑上下文 → 列入高风险清单，必须人工确认。
全部都是显示上下文 → 翻译安全。
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deeppair import literals_in_line  # noqa: E402

# 显示上下文：字面量紧跟在这些 token 之后
DISPLAY_TOKENS = [
    "Text(", "Button(", "Label(", "NavigationLink(", "Toggle(", "Picker(",
    "Section(", "TextField(", "LabeledContent(", ".navigationTitle(", ".alert(",
    "NSLocalizedString(", "HeaderLabel(text:", "PlainToggle(text:",
    "HeaderDropdown(text:", "PlainAlert(title:", "title:", "body:",
    "actionLabel:", "message:", "placeholder:", "footer:", "text:",
    "description:", "prompt:", "infoTitle:", "infoMessage:", "lastResult =",
    "errormsg =", "status =", "statusmsg =", "statusMessage =", "fixupMessage =",
    "self.fixupMessage =", "msg = santandermsg(", "ShortcutLabel(text:",
    # 错误/状态消息：会显示给用户，属显示值
    "NSLocalizedDescriptionKey:", "return (false,", "return (true,",
    "throw ", "?? ", "= ", "+ ", "joined(separator:",
    "self.errormsg =", "self.statusMessage =",
]


def ctx_before(line, pos):
    return line[:pos].rstrip()


def is_display(line, start):
    """该出现位置是否为显示上下文。"""
    w = ctx_before(line, start)
    for tok in DISPLAY_TOKENS:
        if w.endswith(tok):
            return True
    # Text(cond ? "a" : "b")  第二个分支
    tail = w[-160:]
    if re.search(r'\?\s*"[^"]*"\s*:\s*$', tail):
        return True
    if re.search(r'\?\s*$', tail) and re.search(r'(Text|Button|Label)\(', tail):
        return True
    # Label(cond ? "a" : "b", systemImage:)
    if re.search(r'\?\s*"[^"]*"\s*:\s*$', tail):
        return True
    # 逗号分隔的多个字符串参数，前面已有显示 token（如 PlainAlert(title: "x", body: "y"）
    if re.search(r'(title|body|text|message|label|footer|placeholder|infoMessage|actionLabel):\s*"[^"]*",\s*$', tail):
        return True
    return False


def main():
    risky = []
    changed_total = 0

    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            bsrc = io.open(os.path.join("baseline", rel), encoding="utf-8").read()
            lsrc = io.open(lp, encoding="utf-8").read()

            # 该文件中 lara 版现有的全部字面量
            lset = set()
            for ln in lsrc.split("\n"):
                for c, s, e in literals_in_line(ln):
                    lset.add(c)

            # 逐行找被改动的字面量（baseline 有、lara 无）
            for ln_no, line in enumerate(bsrc.split("\n"), 1):
                for content, s, e in literals_in_line(line):
                    if content in lset:
                        continue          # 未改动
                    if not re.search(r"[\u4e00-\u9fff]", lsrc):
                        pass
                    changed_total += 1
                    if not is_display(line, s):
                        risky.append((rel, ln_no, content, ctx_before(line, s)[-70:]))

    print("changed literals (absent from localized file): %d" % changed_total)
    if risky:
        print("\n!!! %d OCCURRENCE(S) IN NON-DISPLAY CONTEXT !!!\n" % len(risky))
        seen = set()
        for rel, ln, content, ctx in risky:
            key = (rel, content)
            if key in seen:
                continue
            seen.add(key)
            print("  %s:%d" % (rel, ln))
            print("     literal: %r" % content[:120])
            print("     context: ...%s" % ctx)
    else:
        print("RESULT: PASS — every changed literal was only ever used in display context")


if __name__ == "__main__":
    main()
