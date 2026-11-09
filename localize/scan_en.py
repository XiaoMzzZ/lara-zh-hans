#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量扫描 v2：单遍分词，正确处理字符串内的 // 与 /*，列出仍含英文人话的字面量。"""

import io
import os
import re
import sys

ROOT = "lara"

COMMON = set("""the you your this that with from have will can not are was for and but
please make sure if then than when what which how why all any some may must should
would could does did done use used using need want try again error failed success
open close enable disable device app apps file files path version check select
""".split())


def tokenize_literals(src):
    """单遍扫描，返回 [(line, content)]，只取普通/多行字符串。"""
    res = []
    i, n = 0, len(src)
    line = 1
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if src.startswith("//", i):
            j = src.find("\n", i)
            if j == -1:
                break
            i = j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j == -1:
                break
            line += src.count("\n", i, j)
            i = j + 2
            continue
        if src.startswith('"""', i):
            start_line = line
            j = src.find('"""', i + 3)
            if j == -1:
                break
            content = src[i + 3:j]
            res.append((start_line, content))
            line += src.count("\n", i, j)
            i = j + 3
            continue
        if c == '"':
            start_line = line
            j = i + 1
            buf = []
            while j < n:
                if src[j] == "\\":
                    buf.append(src[j:j + 2])
                    j += 2
                    continue
                if src[j] == '"':
                    break
                buf.append(src[j])
                j += 1
            res.append((start_line, "".join(buf)))
            i = j + 1
            continue
        i += 1
    return res


def is_candidate(s):
    """判断是否像给人看的英文句子。"""
    if len(s) > 4000:
        return False
    # 去掉插值段
    t = re.sub(r"\\\([^)]*\)", " ", s)
    words = re.findall(r"[A-Za-z]{2,}", t)
    if len(words) < 4:
        return False
    low = [w.lower() for w in words]
    common_hits = sum(1 for w in low if w in COMMON)
    # 至少命中 2 个常见英文功能词，才算人话
    return common_hits >= 2


def main():
    hits = []
    for dirpath, _, files in os.walk(ROOT):
        for fn in sorted(files):
            if not fn.endswith(".swift"):
                continue
            path = os.path.join(dirpath, fn)
            with io.open(path, encoding="utf-8") as f:
                src = f.read()
            for line, content in tokenize_literals(src):
                if is_candidate(content):
                    hits.append((os.path.relpath(path, ROOT), line, content))
    for rel, line, content in hits:
        print("%s:%d\t%s" % (rel, line, content.replace("\n", " ")[:300]))
    print("---- candidates: %d ----" % len(hits))


if __name__ == "__main__":
    main()
