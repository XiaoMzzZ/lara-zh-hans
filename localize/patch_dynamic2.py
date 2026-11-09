# -*- coding: utf-8 -*-
"""Second batch: strings embedded in ternaries / ?? fallbacks."""

PATCHES = [
    ("lara/views/app/ContentView.swift", [
        ('Text("Running...")', 'Text("运行中…")'),
    ]),
    ("lara/views/tweaks/RemoteView.swift", [
        ('Text("Running...")', 'Text("运行中…")'),
    ]),
    ("lara/views/fm/DirectoryView.swift", [
        ('Text(model.emptymsg ?? "Directory is empty.")', 'Text(model.emptymsg ?? "目录为空。")'),
        ('Label(model.showhidden ? "Hide hidden files" : "Display hidden files", systemImage: "eye")',
         'Label(model.showhidden ? "隐藏隐藏文件" : "显示隐藏文件", systemImage: "eye")'),
    ]),
    ("lara/views/fm/FileView.swift", [
        ('Button(editing ? "Save" : "Edit")', 'Button(editing ? "保存" : "编辑")'),
    ]),
    ("lara/views/tweaks/broken/darkboard/DarkBoardExploreView.swift", [
        ('Text(isImported ? "Reimport Theme" : "Import Theme")', 'Text(isImported ? "重新导入主题" : "导入主题")'),
        ('Label(candidate.rawValue, systemImage: "checkmark")', 'Label(L(candidate.rawValue), systemImage: "checkmark")'),
        ('Text(candidate.rawValue)', 'Text(L(candidate.rawValue))'),
        ('Label(filter.rawValue, systemImage: "line.3.horizontal.decrease.circle")',
         'Label(L(filter.rawValue), systemImage: "line.3.horizontal.decrease.circle")'),
    ]),
    ("lara/views/tweaks/broken/darkboard/DarkBoardView.swift", [
        ('Text("\\(manager.themes.count) imported")', 'Text("已导入 \\(manager.themes.count) 个")'),
        ('Text(selectionIndex == nil ? "Select" : "Selected: \\(selectionIndex! + 1)")',
         'Text(selectionIndex == nil ? "选择" : "已选：\\(selectionIndex! + 1)")'),
        ('? "Current override" : "Tap to set"', '? "当前覆盖" : "点击设置"'),
    ]),
    ("lara/views/tweaks/CardView.swift", [
        ('Text(currentcardnum.isEmpty ? "Current suffix: (none)" : "Current suffix: \\(currentcardnum)")',
         'Text(currentcardnum.isEmpty ? "当前后缀：（无）" : "当前后缀：\\(currentcardnum)")'),
    ]),
    ("lara/views/tweaks/CustomView.swift", [
        ('Button(isoverwriting ? "Overwriting..." : "Overwrite Target")',
         'Button(isoverwriting ? "正在覆盖…" : "覆盖目标")'),
        ('Text(globallogger.logs.last ?? "No logs yet")', 'Text(globallogger.logs.last ?? "暂无日志")'),
    ]),
    ("lara/views/tweaks/FontPicker.swift", [
        ('Text(globallogger.logs.last ?? "No logs yet")', 'Text(globallogger.logs.last ?? "暂无日志")'),
    ]),
    ("lara/views/tweaks/DecryptView.swift", [
        ('Text(query.isEmpty ? "Loading..." : "No matches.")', 'Text(query.isEmpty ? "加载中…" : "没有匹配项。")'),
    ]),
    ("lara/views/tweaks/JitView.swift", [
        ('Text(query.isEmpty ? "No apps found." : "No matches.")', 'Text(query.isEmpty ? "未找到 App。" : "没有匹配项。")'),
    ]),
    ("lara/views/tweaks/OTAView.swift", [
        ('Text(otaDisabled ? "Disabled" : "Enabled")', 'Text(otaDisabled ? "已禁用" : "已启用")'),
    ]),
    ("lara/views/tweaks/ScreenTimeView.swift", [
        ('Text(screenTimeDisabled ? "Disabled" : "Enabled")', 'Text(screenTimeDisabled ? "已禁用" : "已启用")'),
        ('Text(backupExists ? "Found" : "Not found")', 'Text(backupExists ? "已找到" : "未找到")'),
    ]),
    ("lara/views/tweaks/ShowHiddenIconsView.swift", [
        ('Text(isEnabled ? "Enabled" : "Disabled")', 'Text(isEnabled ? "已启用" : "已禁用")'),
    ]),
    ("lara/views/tweaks/ToolsView.swift", [
        ('Text(isaslr ? "enabled" : "disabled")', 'Text(isaslr ? "已启用" : "已禁用")'),
        ('Text(mgr.sbxready ? "tkn" : "No Saved Token.")', 'Text(mgr.sbxready ? "tkn" : "没有已保存的令牌。")'),
    ]),
    ("lara/views/tweaks/VarCleanView.swift", [
        ('Button(selectedcount == 0 ? "Select All" : "Clear")', 'Button(selectedcount == 0 ? "全选" : "取消全选")'),
    ]),
    ("lara/views/tweaks/WhitelistView.swift", [
        ('Text(contents[f.path] ?? "(not loaded)")', 'Text(contents[f.path] ?? "（未加载）")'),
    ]),
]

fail = 0
for path, pairs in PATCHES:
    src = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in src:
            print(f"MISS  {path}: {old[:70]}")
            fail += 1
            continue
        src = src.replace(old, new)
    open(path, "w", encoding="utf-8", newline="").write(src)
    print(f"OK    {path}")

print("failures:", fail)
