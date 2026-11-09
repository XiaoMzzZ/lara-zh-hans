#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补丁：翻译赋值给 status / message 等变量、仅用于显示的英文文本。"""

import io
import os
import sys

ROOT = "lara"

# (相对路径, 原文, 译文)
PATCHES = [
    # ---- ShowHiddenIconsView ----
    ("views/tweaks/ShowHiddenIconsView.swift",
     '"Sandbox escape or VFS is not ready."',
     '"沙盒逃逸或 VFS 尚未就绪。"'),
    ("views/tweaks/ShowHiddenIconsView.swift",
     '"SBIconVisibility enabled. If there is no visible effect, you may need to rebuild SpringBoard\'s Application State DB, then reboot the device."',
     '"已启用 SBIconVisibility。如果看不到效果，可能需要重建 SpringBoard 的应用状态数据库，然后重启设备。"'),
    ("views/tweaks/ShowHiddenIconsView.swift",
     '"SBIconVisibility preference removed. If there is no visible effect, rebuild SpringBoard\'s Application State DB, then reboot the device."',
     '"已移除 SBIconVisibility 偏好设置。如果看不到效果，请重建 SpringBoard 的应用状态数据库，然后重启设备。"'),
    ("views/tweaks/ShowHiddenIconsView.swift",
     '"Application State DB cleared. Reboot the device now. Do not rely on respring; it may leave SpringBoard on a black screen. Some widget configuration may be lost."',
     '"应用状态数据库已清空。请立即重启设备，不要依赖注销重启——它可能让 SpringBoard 停在黑屏。部分小组件配置可能会丢失。"'),

    # ---- SystemColor ----
    ("views/tweaks/SystemColor.swift",
     '@State private var status = "Not loaded"',
     '@State private var status = "未加载"'),
    ("views/tweaks/SystemColor.swift",
     'status = "Loaded \\(entries.count) colors"',
     'status = "已加载 \\(entries.count) 种颜色"'),
    ("views/tweaks/SystemColor.swift",
     'status = "Failed: \\(error.localizedDescription)"',
     'status = "失败：\\(error.localizedDescription)"'),
    ("views/tweaks/SystemColor.swift",
     'status = "No original data"',
     'status = "没有原始数据"'),
    ("views/tweaks/SystemColor.swift",
     'status = "Temp write failed: \\(error.localizedDescription)"',
     'status = "临时写入失败：\\(error.localizedDescription)"'),

    # ---- ToolsView ----
    ("views/tweaks/ToolsView.swift",
     'status = "Succeeded. Open the Pocket Poster app, open settings and tap Detect."',
     'status = "成功。请打开 Pocket Poster App，进入设置并点击“检测”。"'),
    ("views/tweaks/ToolsView.swift",
     'status = "Failed. Check logs."',
     'status = "失败。请查看日志。"'),

    # ---- WhitelistView ----
    ("views/tweaks/WhitelistView.swift",
     'status = "sandbox escape not ready"',
     'status = "沙盒逃逸尚未就绪"'),
    ("views/tweaks/WhitelistView.swift",
     'status = "failed to build empty plist"',
     'status = "构建空白 plist 失败"'),
    ("views/tweaks/WhitelistView.swift",
     'status = "Patched all files!"',
     'status = "已修补所有文件！"'),
    ("views/tweaks/WhitelistView.swift",
     'status = "Failed to patch: \\(failures.joined(separator: ", "))"',
     'status = "修补失败：\\(failures.joined(separator: ", "))"'),

    # ---- PasscodeView ----
    ("views/tweaks/passcode/PasscodeView.swift",
     'passcodeThemeManager.message = "Done"',
     'passcodeThemeManager.message = "完成"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     'passcodeThemeManager.message = "Completed with errors"',
     'passcodeThemeManager.message = "已完成，但存在错误"'),
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
            # 可能已经替换过
            if new in src:
                print("ALREADY  %s :: %s" % (rel, old[:50]))
            else:
                print("NOTFOUND %s :: %s" % (rel, old[:60]))
            continue
        print("PATCH %dx %s :: %s" % (n, rel, old[:50]))
        total += n
        if apply:
            src = src.replace(old, new)
            with io.open(path, "w", encoding="utf-8", newline="") as f:
                f.write(src)
    print("total replacements: %d%s" % (total, "" if apply else " (dry-run, add --apply)"))


if __name__ == "__main__":
    main()
