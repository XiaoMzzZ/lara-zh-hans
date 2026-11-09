#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二批补丁：显示上下文扫描出的遗漏项。"""

import io
import os
import sys

ROOT = "lara"

PATCHES = [
    # ---- DirectoryView ----
    ("views/fm/DirectoryView.swift",
     r'"Operation completed."',
     r'"操作已完成。"'),
    ("views/fm/DirectoryView.swift",
     r'"Operation failed."',
     r'"操作失败。"'),

    # ---- FileView ----
    ("views/fm/FileView.swift",
     r'"VFS overwrite failed."',
     r'"VFS 覆盖写入失败。"'),
    ("views/fm/FileView.swift",
     r'"Unable to write file."',
     r'"无法写入文件。"'),

    # ---- SystemColor ----
    ("views/tweaks/SystemColor.swift",
     r'"Patched!"',
     r'"已修补！"'),
    ("views/tweaks/SystemColor.swift",
     r'"Failed: \(res.message)"',
     r'"失败：\(res.message)"'),

    # ---- PasscodeView ----
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Importing theme..."',
     r'"正在导入主题…"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Imported \(extractedKeys.count) key(s)"',
     r'"已导入 \(extractedKeys.count) 个键"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"applied \(successCount) file(s)"',
     r'"已应用 \(successCount) 个文件"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"applied \(successCount), failed \(failCount)\n\n\(errors.joined(separator: "\n"))"',
     r'"已应用 \(successCount) 个，失败 \(failCount) 个\n\n\(errors.joined(separator: "\n"))"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Originals restored"',
     r'"原始文件已恢复"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Error: \(error.localizedDescription)"',
     r'"错误：\(error.localizedDescription)"'),

    # ---- GestaltFileView ----
    ("views/tweaks/mobilegestalt/GestaltFileView.swift",
     r'case let v as Bool: return v ? "True" : "False"',
     r'case let v as Bool: return v ? "是" : "否"'),
    ("views/tweaks/mobilegestalt/GestaltFileView.swift",
     r'default: return "Unknown"',
     r'default: return "未知"'),
]


def main():
    apply = "--apply" in sys.argv
    total = 0
    for rel, old, new in PATCHES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print("MISSING FILE %s" % rel)
            continue
        with io.open(path, encoding="utf-8") as f:
            src = f.read()
        n = src.count(old)
        if n == 0:
            if new in src:
                print("ALREADY  %s :: %s" % (rel, old[:55]))
            else:
                print("NOTFOUND %s :: %s" % (rel, old[:70]))
            continue
        print("PATCH %dx %s :: %s" % (n, rel, old[:55]))
        total += n
        if apply:
            src = src.replace(old, new)
            with io.open(path, "w", encoding="utf-8", newline="") as f:
                f.write(src)
    print("total replacements: %d%s" % (total, "" if apply else " (dry-run, add --apply)"))


if __name__ == "__main__":
    main()
