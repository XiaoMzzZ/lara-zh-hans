#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
严格 Swift 词法分析器。

目的：验证每个 .swift 文件能被正确切分为 token 流，
从而证明不存在「字符串未闭合」「插值括号不平衡」「块注释未闭合」等致命语法错误。

按 Swift 语言规范处理：
  - 行注释 //
  - 块注释 /* */，**支持嵌套**
  - 普通字符串 "..."，转义 \n \t \\ \" \0 \u{...}
  - 字符串插值 \( ... )，内部可再嵌套字符串与括号
  - 多行字符串 \"\"\"...\"\"\"
  - 原始字符串 #"..."# / ##"..."##
  - 标识符、数字、运算符等（仅用于推进位置，不深入语义）
"""

import io
import os
import sys

OPERATORS = set("+-*/%=<>!&|^~?.")
PUNCT = set("(){}[],;:")


class LexError(Exception):
    pass


def lex_swift(src, path):
    """返回 (tokens, errors)。tokens 只统计字符串数量，errors 记录致命问题。"""
    i = 0
    n = len(src)
    line = 1
    strings = 0
    errors = []
    depth_stack = []          # 用于插值/普通括号跟踪: ('interp'|'paren'|'brace'|'bracket', line)

    def err(msg):
        errors.append("line %d: %s" % (line, msg))

    while i < n:
        c = src[i]

        # ---------- 换行 ----------
        if c == "\n":
            line += 1
            i += 1
            continue

        # ---------- 行注释 ----------
        if src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j == -1 else j
            continue

        # ---------- 块注释（可嵌套） ----------
        if src.startswith("/*", i):
            start_line = line
            depth = 1
            i += 2
            while i < n and depth > 0:
                if src.startswith("/*", i):
                    depth += 1
                    i += 2
                elif src.startswith("*/", i):
                    depth -= 1
                    i += 2
                else:
                    if src[i] == "\n":
                        line += 1
                    i += 1
            if depth > 0:
                err("unterminated block comment opened at line %d" % start_line)
            continue

        # ---------- 原始字符串 #"..."# ----------
        if c == "#":
            k = i
            while k < n and src[k] == "#":
                k += 1
            if k < n and src[k] == '"':
                hashes = k - i
                close = '"' + "#" * hashes
                # 多行原始字符串
                if src.startswith('"""', k):
                    body_start = k + 3
                    j = src.find('"""' + "#" * hashes, body_start)
                    if j == -1:
                        err("unterminated raw multiline string at line %d" % line)
                        break
                    strings += 1
                    line += src.count("\n", i, j)
                    i = j + 3 + hashes
                    continue
                j = k + 1
                ok = False
                while j < n:
                    if src[j] == "\\" and src.startswith("\\" + "#" * hashes, j):
                        j += 1 + hashes
                        continue
                    if src.startswith(close, j):
                        ok = True
                        break
                    j += 1
                if not ok:
                    err("unterminated raw string at line %d" % line)
                    break
                strings += 1
                i = j + 1 + hashes
                continue
            i += 1
            continue

        # ---------- 多行字符串 """...""" ----------
        if src.startswith('"""', i):
            start_line = line
            j = i + 3
            ok = False
            while j < n:
                if src[j] == "\\":
                    # 转义，跳过下一个字符（含换行）
                    if j + 1 < n and src[j + 1] == "\n":
                        line += 1
                    j += 2
                    continue
                if src.startswith('"""', j):
                    ok = True
                    break
                if src[j] == "\n":
                    line += 1
                j += 1
            if not ok:
                err("unterminated multiline string opened at line %d" % start_line)
                break
            strings += 1
            i = j + 3
            continue

        # ---------- 普通字符串 ----------
        if c == '"':
            start_line = line
            i += 1
            closed = False
            while i < n:
                ch = src[i]
                if ch == "\\":
                    nxt = src[i + 1] if i + 1 < n else ""
                    if nxt == "(":
                        # ---- 字符串插值：跟踪括号深度 ----
                        i += 2
                        depth = 1
                        while i < n and depth > 0:
                            c2 = src[i]
                            if c2 == "(":
                                depth += 1
                                i += 1
                            elif c2 == ")":
                                depth -= 1
                                i += 1
                            elif c2 == '"':
                                # 插值内嵌套字符串
                                i += 1
                                while i < n:
                                    if src[i] == "\\":
                                        i += 2
                                        continue
                                    if src[i] == '"':
                                        i += 1
                                        break
                                    if src[i] == "\n":
                                        line += 1
                                    i += 1
                            elif c2 == "\n":
                                line += 1
                                i += 1
                            else:
                                i += 1
                        if depth > 0:
                            err("unbalanced interpolation paren in string at line %d" % start_line)
                        continue
                    else:
                        if nxt == "\n":
                            line += 1
                        i += 2
                        continue
                if ch == '"':
                    closed = True
                    i += 1
                    break
                if ch == "\n":
                    # Swift 普通字符串不允许裸换行
                    err("newline inside single-line string at line %d" % start_line)
                    break
                i += 1
            if not closed and i >= n:
                err("unterminated string opened at line %d" % start_line)
            strings += 1
            continue

        # ---------- 括号平衡 ----------
        if c in "([{":
            depth_stack.append((c, line))
            i += 1
            continue
        if c in ")]}":
            pairs = {")": "(", "]": "[", "}": "{"}
            if not depth_stack:
                err("unmatched closing '%s'" % c)
            else:
                op, opline = depth_stack[-1]
                if op != pairs[c]:
                    err("mismatched '%s' (opened '%s' at line %d)" % (c, op, opline))
                depth_stack.pop()
            i += 1
            continue

        i += 1

    if depth_stack:
        for op, opline in depth_stack[-3:]:
            errors.append("unclosed '%s' opened at line %d" % (op, opline))

    return strings, errors


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "lara"
    total_files = 0
    total_strings = 0
    bad = []
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            p = os.path.join(dp, f)
            with io.open(p, encoding="utf-8") as fh:
                src = fh.read()
            total_files += 1
            try:
                cnt, errs = lex_swift(src, p)
            except Exception as e:  # noqa
                errs = ["lexer crash: %r" % e]
                cnt = 0
            total_strings += cnt
            if errs:
                bad.append((p, errs))
    print("files lexed: %d, string literals: %d" % (total_files, total_strings))
    if bad:
        print("\n!!! %d FILE(S) WITH LEX ERRORS !!!" % len(bad))
        for p, errs in bad:
            print("\n%s" % p)
            for e in errs[:10]:
                print("   %s" % e)
    else:
        print("RESULT: all files lex cleanly (no unterminated strings/comments, balanced delimiters)")


if __name__ == "__main__":
    main()
