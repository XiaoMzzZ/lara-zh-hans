#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
深度审查 v2：逐行配对 baseline 与 lara 的字符串字面量。

正确处理 Swift 字符串插值 \( ... ) 内嵌套的字符串与括号，
验证每对「原文 -> 译文」：
  1. 插值表达式是否完整保留
  2. 格式符 %d %@ %04o 数量是否一致
  3. 转义序列是否合法（\( 合法，\q 非法）
  4. 是否引入空字符串
  5. 是否把路径 / bundle id 等非显示字符串翻译掉
"""

import io
import os
import re
import sys

STR_ESCAPES_OK = set('0\\tnrvf"\'u(')


def literals_in_line(line):
    """返回该行所有字符串字面量（不含外层引号），正确处理插值嵌套。"""
    res = []
    i, n = 0, len(line)
    while i < n:
        if line[i] != '"':
            i += 1
            continue
        # 多行字符串在本审查中不处理（改动均为单行）
        start = i
        i += 1
        buf = []
        while i < n:
            ch = line[i]
            if ch == "\\":
                nxt = line[i + 1] if i + 1 < n else ""
                if nxt == "(":
                    # 插值：整体原样保留，内部字符串不再拆分
                    depth = 1
                    buf.append("\\(")
                    i += 2
                    while i < n and depth > 0:
                        c2 = line[i]
                        if c2 == "(":
                            depth += 1
                        elif c2 == ")":
                            depth -= 1
                        elif c2 == '"':
                            # 插值内嵌套字符串：原样吞掉
                            buf.append('"')
                            i += 1
                            while i < n:
                                if line[i] == "\\":
                                    buf.append(line[i:i + 2])
                                    i += 2
                                    continue
                                buf.append(line[i])
                                if line[i] == '"':
                                    i += 1
                                    break
                                i += 1
                            continue
                        buf.append(c2)
                        i += 1
                    continue
                buf.append(line[i:i + 2])
                i += 2
                continue
            if ch == '"':
                i += 1
                break
            buf.append(ch)
            i += 1
        res.append(("".join(buf), start, i))
    return res


INTERP_RE = re.compile(r"\\\((?:[^()]|\([^()]*\))*\)")
FMT_RE = re.compile(
    r"%(?:\d+\$)?[-+ 0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|q|L|z|j|t)?[diouxXeEfgGaAcspn@%]"
)


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    issues = []
    pairs = 0
    files = 0

    for dp, _, fs in os.walk("baseline"):
        for f in sorted(fs):
            if not f.endswith(".swift"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), "baseline")
            lp = os.path.join("lara", rel)
            if not os.path.exists(lp):
                continue
            files += 1
            b = io.open(os.path.join("baseline", rel), encoding="utf-8").read().split("\n")
            l = io.open(lp, encoding="utf-8").read().split("\n")

            if len(b) != len(l):
                issues.append((rel, 0, "LINE COUNT %d -> %d" % (len(b), len(l))))
                continue

            for idx, (bl, ll) in enumerate(zip(b, l), 1):
                if bl == ll:
                    continue
                bs = [x[0] for x in literals_in_line(bl)]
                ls = [x[0] for x in literals_in_line(ll)]
                if len(bs) != len(ls):
                    issues.append((rel, idx,
                                   "LITERAL COUNT %d -> %d | OLD=%s"
                                   % (len(bs), len(ls), norm_ws(bl)[:120])))
                    continue
                for o, nw in zip(bs, ls):
                    if o == nw:
                        continue
                    pairs += 1

                    # 1. 插值保留
                    oi = sorted(INTERP_RE.findall(o))
                    ni = sorted(INTERP_RE.findall(nw))
                    if oi != ni:
                        missing = set(oi) - set(ni)
                        # 允许移除单复数三元 ? "" : "s"
                        plural_only = missing and all('?' in x and '"' in x for x in missing)
                        if not plural_only:
                            issues.append((rel, idx, "INTERP LOST %s | NEW=%s" % (sorted(missing), nw[:110])))

                    # 2. 格式符保留
                    of = sorted(FMT_RE.findall(o))
                    nf = sorted(FMT_RE.findall(nw))
                    if of != nf:
                        issues.append((rel, idx, "FORMAT %s -> %s | OLD=%s NEW=%s"
                                       % (of, nf, o[:90], nw[:90])))

                    # 3. 转义合法
                    for m in re.finditer(r"\\(.)", nw):
                        if m.group(1) not in STR_ESCAPES_OK:
                            issues.append((rel, idx, "BAD ESCAPE \\%s | %s" % (m.group(1), nw[:110])))

                    # 4. 空字符串
                    if nw == "" and o != "":
                        issues.append((rel, idx, "EMPTY STRING from %s" % o[:100]))

                    # 5. 非显示字符串被翻译
                    if o.startswith("/") or o.startswith("com.apple"):
                        issues.append((rel, idx, "NON-DISPLAY %s -> %s" % (o[:70], nw[:70])))

    print("files compared: %d | string pairs changed: %d" % (files, pairs))
    if issues:
        print("\n!!! %d ISSUE(S) !!!\n" % len(issues))
        for rel, idx, msg in issues:
            print("  %s:%d  %s" % (rel, idx, msg))
    else:
        print("RESULT: PASS — every changed string preserves interpolation, format specifiers and escapes")


if __name__ == "__main__":
    main()
