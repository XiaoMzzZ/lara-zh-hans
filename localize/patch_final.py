#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终补丁：翻译剩余所有「用户可见」的英文文本。

严格不碰：
- isRemoteCallFailure 依赖的 "-> failed" / ": failed" / "failed to" / "-> -1" 标记
- logmsg / globallogger / print 调试输出
- NSError domain 名
- 文件路径、bundle id、plist key、SF Symbol
"""

import io
import os
import sys

ROOT = "lara"

PATCHES = [
    # ================= laramgr.swift =================
    ("classes/laramgr.swift",
     r'"clear immutable failed: \(error.localizedDescription)"',
     r'"清除不可变标志失败：\(error.localizedDescription)"'),
    ("classes/laramgr.swift",
     r'"\(prefix)sbx open failed: errno=\(errno) \(String(cString: strerror(errno)))"',
     r'"\(prefix)sbx 打开失败：errno=\(errno) \(String(cString: strerror(errno)))"'),
    ("classes/laramgr.swift",
     r'"sbx write failed: errno=\(errno) \(String(cString: strerror(errno)))"',
     r'"sbx 写入失败：errno=\(errno) \(String(cString: strerror(errno)))"'),
    ("classes/laramgr.swift",
     r'"sbx truncate failed: errno=\(errno) \(String(cString: strerror(errno)))"',
     r'"sbx 截断失败：errno=\(errno) \(String(cString: strerror(errno)))"'),
    ("classes/laramgr.swift",
     r'"ok (\(total) bytes)"',
     r'"成功（\(total) 字节）"'),
    ("classes/laramgr.swift",
     r'"source file not found: \(source)"',
     r'"找不到源文件：\(source)"'),
    ("classes/laramgr.swift",
     r'''"file at \(path) does not exist or couldn't be found"''',
     r'"文件不存在或无法访问：\(path)"'),
    ("classes/laramgr.swift",
     r'"overwrote plist at path \(path)"',
     r'"已覆盖 plist：\(path)"'),
    ("classes/laramgr.swift",
     r'"an error occurred: \(error)"',
     r'"发生错误：\(error)"'),
    ("classes/laramgr.swift",
     r'"key \(key) not found"',
     r'"找不到键：\(key)"'),

    # ================= DecryptView.swift =================
    ("views/tweaks/DecryptView.swift",
     r'"App is not running, try again."',
     r'"App 未运行，请重试。"'),
    ("views/tweaks/DecryptView.swift",
     r'"Darksword not ready, run the exploit first."',
     r'"Darksword 尚未就绪，请先运行漏洞利用。"'),
    ("views/tweaks/DecryptView.swift",
     r'"Sandbox not escaped."',
     r'"沙盒尚未逃逸。"'),
    ("views/tweaks/DecryptView.swift",
     r'"Could not launch app. Open it manually."',
     r'"无法启动 App，请手动打开。"'),
    ("views/tweaks/DecryptView.swift",
     r'"Process not found after launch. Try manually."',
     r'"启动后未找到进程，请手动尝试。"'),
    ("views/tweaks/DecryptView.swift",
     r'"Failed to enumerate bundle for copy"',
     r'"枚举 App 包内容失败，无法复制"'),
    ("views/tweaks/DecryptView.swift",
     r'"Failed to decrypt main binary"',
     r'"解密主二进制文件失败"'),
    ("views/tweaks/DecryptView.swift",
     r'"Failed to move app bundle: \(error.localizedDescription)"',
     r'"移动 App 包失败：\(error.localizedDescription)"'),
    ("views/tweaks/DecryptView.swift",
     r'"Failed to create ipa: \(error.localizedDescription)"',
     r'"创建 IPA 失败：\(error.localizedDescription)"'),

    # ================= OTAView.swift =================
    ("views/tweaks/OTAView.swift",
     r'"OTA updates disabled. Reboot to apply."',
     r'"OTA 更新已禁用，重启后生效。"'),
    ("views/tweaks/OTAView.swift",
     r'"OTA updates enabled. Reboot to apply."',
     r'"OTA 更新已启用，重启后生效。"'),
    ("views/tweaks/OTAView.swift",
     r'"Operation failed. Check logs for details."',
     r'"操作失败，请查看日志了解详情。"'),

    # ================= ScreenTimeView.swift =================
    ("views/tweaks/ScreenTimeView.swift",
     r'"Screen Time disabled. Reboot to apply."',
     r'"屏幕使用时间已禁用，重启后生效。"'),
    ("views/tweaks/ScreenTimeView.swift",
     r'"Screen Time enabled. Reboot to apply."',
     r'"屏幕使用时间已启用，重启后生效。"'),
    ("views/tweaks/ScreenTimeView.swift",
     r'"Operation failed. Check logs for details."',
     r'"操作失败，请查看日志了解详情。"'),

    # ================= SettingsView.swift =================
    ("views/app/settings/SettingsView.swift",
     r'"Please try manually stashing KRW a few more times."',
     r'"请再手动尝试暂存 KRW 几次。"'),

    # ================= PasscodeView.swift =================
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Error: SBX not ready"',
     r'"错误：SBX 尚未就绪"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Error: TelephonyUI cache not found"',
     r'"错误：未找到 TelephonyUI 缓存"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Error: failed to enumerate cache"',
     r'"错误：枚举缓存失败"'),
    ("views/tweaks/passcode/PasscodeView.swift",
     r'"Failed to enumerate cache"',
     r'"枚举缓存失败"'),

    # ================= RemoteView.swift（仅弹窗标题，不碰 result 判定字符串） =================
    ("views/tweaks/RemoteView.swift",
     r'run("Enable Grid App Switcher")',
     r'run("启用网格多任务切换")'),

    # ================= GestaltView.swift =================
    ("views/tweaks/mobilegestalt/GestaltView.swift",
     r'"MobileGestalt is not vaild! Please restart the app."',
     r'"MobileGestalt 无效！请重启 App。"'),

    # ================= FileSystemHelpers.swift =================
    ("views/fm/FileSystemHelpers.swift",
     r'"Failed to read file.\n\n"',
     r'"读取文件失败。\n\n"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Failed to read file."',
     r'"读取文件失败。"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Exists: \(exists ? "yes" : "no")"',
     r'"存在：\(exists ? "是" : "否")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Kind: \(isdir.boolValue ? "directory" : "regular item")"',
     r'"类型：\(isdir.boolValue ? "目录" : "普通项目")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Size: \(size) bytes"',
     r'"大小：\(size) 字节"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Symlink: \(sym ? "yes" : "no")"',
     r'"符号链接：\(sym ? "是" : "否")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Symlink target: \(target)"',
     r'"符号链接目标：\(target)"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Alias file: \(alias ? "yes" : "no")"',
     r'"替身文件：\(alias ? "是" : "否")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"File attribute type: \(filetype.rawValue)"',
     r'"文件属性类型：\(filetype.rawValue)"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Owner: \(owner)"',
     r'"所有者：\(owner)"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Group: \(group)"',
     r'"所属组：\(group)"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"POSIX perms: %04o"',
     r'"POSIX 权限：%04o"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Readable: \(fm.isReadableFile(atPath: path) ? "yes" : "no")"',
     r'"可读：\(fm.isReadableFile(atPath: path) ? "是" : "否")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Writable: \(fm.isWritableFile(atPath: path) ? "yes" : "no")"',
     r'"可写：\(fm.isWritableFile(atPath: path) ? "是" : "否")"'),
    ("views/fm/FileSystemHelpers.swift",
     r'"Executable: \(fm.isExecutableFile(atPath: path) ? "yes" : "no")"',
     r'"可执行：\(fm.isExecutableFile(atPath: path) ? "是" : "否")"'),

    # ================= IconThemeManager.swift =================
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Could not open image"',
     r'"无法打开图片"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Could not read themed icon image at \(icon.rawThemeIconURL.path)"',
     r'"无法读取主题图标：\(icon.rawThemeIconURL.path)"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Could not read original icon image at \(iconURL.path)"',
     r'"无法读取原始图标：\(iconURL.path)"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"\(bundleIdentifier): Could not fit icon \(iconName) inside original size budget"',
     r'"\(bundleIdentifier)：图标 \(iconName) 无法压缩到原始大小限制内"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"No icons were found in the imported theme. Expected `<bundle-id>.png` in a folder."',
     r'"导入的主题中未找到图标。需要文件夹内包含 `<bundle-id>.png`。"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Unsupported theme import type: \(workingURL.lastPathComponent)"',
     r'"不支持的主题导入类型：\(workingURL.lastPathComponent)"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Could not find icons in \(url.lastPathComponent). Expected PNGs named <bundle-id>.png."',
     r'"在 \(url.lastPathComponent) 中找不到图标。需要以 <bundle-id>.png 命名的 PNG 文件。"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'fixupMessage = "Restoring original app icons..."',
     r'fixupMessage = "正在恢复原始 App 图标…"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'self.fixupMessage = "Fixing \(app.name)"',
     r'self.fixupMessage = "正在修复 \(app.name)"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Your apps should now function properly."',
     r'"你的 App 现在应该可以正常使用了。"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Reopen lara after respring and initialize SBX so icon backups can be restored."',
     r'"注销重启后重新打开 lara 并初始化 SBX，这样才能恢复图标备份。"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'"Fixing apps..." : "Fixup complete"',
     r'"正在修复 App…" : "修复完成"'),
    ("classes/tweaks/darkboard/IconThemeManager.swift",
     r'? "Please wait" : "Close"',
     r'? "请稍候" : "关闭"'),

    # ================= IconThemeGalleryManager.swift =================
    ("classes/tweaks/darkboard/IconThemeGalleryManager.swift",
     r'"Could not fetch the Cowabunga theme gallery."',
     r'"无法获取 Cowabunga 主题库。"'),
    ("classes/tweaks/darkboard/IconThemeGalleryManager.swift",
     r'"Could not reach the Cowabunga gallery repository."',
     r'"无法连接 Cowabunga 主题库仓库。"'),
    ("classes/tweaks/darkboard/IconThemeGalleryManager.swift",
     r'"Could not resolve the Cowabunga gallery version."',
     r'"无法解析 Cowabunga 主题库版本。"'),
    ("classes/tweaks/darkboard/IconThemeGalleryManager.swift",
     r'"Could not download \(theme.name)."',
     r'"无法下载 \(theme.name)。"'),
    ("classes/tweaks/darkboard/IconThemeGalleryManager.swift",
     r'"Invalid gallery URL for \(relativePath)."',
     r'"图库 URL 无效：\(relativePath)。"'),

    # ================= resizetoapprox.swift =================
    ("funcs/resizetoapprox.swift",
     r'"Could not compress image low enough to fit inside the original size budget"',
     r'"无法把图片压缩到原始大小限制以内"'),
    ("funcs/resizetoapprox.swift",
     r'"Could not compress image"',
     r'"无法压缩图片"'),
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
