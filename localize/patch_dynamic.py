# -*- coding: utf-8 -*-
"""Manual patches for strings that are assigned to variables / embedded in ternaries,
so the generic context-aware replacer cannot see them."""

import io, os, sys

PATCHES = [
    ("lara/views/tweaks/CardView.swift", [
        ('status = "Invalid image data"', 'status = "图片数据无效"'),
        ('status = "Failed to encode image"', 'status = "图片编码失败"'),
        ('status = "Card updated. Respring now?"', 'status = "卡片已更新。现在注销重启？"'),
        ('status = "Failed to overwrite card"', 'status = "覆盖卡片失败"'),
        ('status = "No backup found"', 'status = "未找到备份"'),
        ('status = "Failed to read backup"', 'status = "读取备份失败"'),
        ('status = "Restored card image. Respring now?"', 'status = "卡片图片已恢复。现在注销重启？"'),
        ('status = "Restore failed"', 'status = "恢复失败"'),
        ('status = "Failed to read pass.json"', 'status = "读取 pass.json 失败"'),
        ('status = "Failed to encode pass.json"', 'status = "编码 pass.json 失败"'),
        ('status = "Card number updated"', 'status = "卡号已更新"'),
        ('status = "Failed to update pass.json"', 'status = "更新 pass.json 失败"'),
        ('status = "No pass.json backup"', 'status = "没有 pass.json 备份"'),
        ('status = "Restored pass.json"', 'status = "pass.json 已恢复"'),
        ('status = "Failed to restore pass.json"', 'status = "恢复 pass.json 失败"'),
    ]),
    ("lara/views/tweaks/VarCleanView.swift", [
        ('"Cleanup enabled via sandbox escape."', '"已通过沙盒逃逸启用清理。"'),
        ('"Detection only. Escape the sandbox to delete matched paths."', '"仅检测模式。逃逸沙盒后才能删除匹配路径。"'),
        (r'statusmsg = "Found \(matchcount) matched path\(matchcount == 1 ? "" : "s")."',
         r'statusmsg = "找到 \(matchcount) 个匹配路径。"'),
        (r'statusmsg = "Deleted \(deletedcount) path\(deletedcount == 1 ? "" : "s")."',
         r'statusmsg = "已删除 \(deletedcount) 个路径。"'),
        (r'statusmsg = "Deleted \(deletedcount) path\(deletedcount == 1 ? "" : "s"), failed \(failures.count)."',
         r'statusmsg = "已删除 \(deletedcount) 个路径，失败 \(failures.count) 个。"'),
        (r'Text("Delete \(selectedcount) matched path\(selectedcount == 1 ? "" : "s")?")',
         r'Text("删除 \(selectedcount) 个匹配路径？")'),
    ]),
    ("lara/views/fm/FileSystemHelpers.swift", [
        ('return "No matching items."', 'return "没有匹配的项目。"'),
        ('return "No visible items. Enable hidden files to show dotfiles."', 'return "没有可见项目。开启“显示隐藏文件”以显示点文件。"'),
    ]),
    ("lara/views/tweaks/passcode/PasscodeView.swift", [
        ('message = "preparing passcode theme..."', 'message = "正在准备密码主题…"'),
        (r'message = "applying \(keyId)"', r'message = "正在应用 \(keyId)"'),
    ]),
]

fail = 0
for path, pairs in PATCHES:
    src = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in src:
            print(f"MISS  {path}: {old[:60]}")
            fail += 1
            continue
        src = src.replace(old, new)
    open(path, "w", encoding="utf-8", newline="").write(src)
    print(f"OK    {path} ({len(pairs)} rules)")

print("failures:", fail)
