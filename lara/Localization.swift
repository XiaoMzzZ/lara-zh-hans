//
//  Localization.swift
//  lara
//
//  简体中文语言表。
//  仅用于“无法直接替换字面量”的动态文本（例如以字符串作为 id / 持久化键的数据模型），
//  在显示位置调用 L(...) 进行翻译，绝不改动原始值，避免影响逻辑与已保存的状态。
//

import Foundation

func L(_ value: String) -> String {
    laraZhHans[value] ?? value
}

let laraZhHans: [String: String] = [
    // 通用选项值（同时被用作 UserDefaults 的值与逻辑判断，故只在显示处翻译）
    "Visible": "显示",
    "Color": "颜色",
    "Blur": "模糊",
    "Disabled": "禁用",

    // 枚举显示值（rawValue 仍保持英文，仅显示时翻译）
    "Hybrid": "混合",
    "App Name": "应用名称",
    "In Tabs": "标签页内",
    "In Toolbar": "工具栏内",
    "Directly in ContentView": "直接显示在主界面",
    "Photos": "照片",
    "Files": "文件",
    "Regular": "常规",
    "Standard": "标准",
    "Mono": "等宽",
    "Italic": "斜体",
    "read": "只读",
    "write": "只写",
    "read-write": "读写",
    "Random": "随机",
    "Newest": "最新",
    "Oldest": "最早",

    // dirtyZero 分区名
    "Home Screen": "主屏幕",
    "Lock Screen": "锁屏",
    "Alerts & Overlays": "提醒与浮层",
    "Fonts & Icons": "字体与图标",
    "Control Center": "控制中心",
    "Sound Effects": "音效",
    "Risky Tweaks": "高风险调整",

    // dirtyZero 调整项
    "Blue Notifcation Shadows": "蓝色通知阴影",
    "Break Clock Font": "破坏时钟字体",
    "Break SpringBoard names": "破坏 SpringBoard 名称",
    "Break System Font": "破坏系统字体",
    "Clear App Library BG": "清除 App 资源库背景",
    "Clear App Switcher": "清除多任务切换器背景",
    "Clear CC Modules": "清除控制中心模块背景",
    "Clear Folder Backgrounds": "清除文件夹背景",
    "Clear Library Search BG": "清除资源库搜索背景",
    "Clear Notification & Widget BGs": "清除通知与小组件背景",
    "Clear Passcode Background": "清除密码界面背景",
    "Clear Spotlight Background": "清除聚焦搜索背景",
    "Clear Touch & Alert Backgrounds": "清除触摸与提醒背景",
    "Clear Widget Config BG": "清除小组件配置背景",
    "Disable ALL Accent Colors": "禁用所有强调色",
    "Disable ALL Banners": "禁用所有横幅",
    "Disable AirDrop Ping": "禁用 AirDrop 提示音",
    "Disable Charge Sound": "禁用充电提示音",
    "Disable Dialing Sounds": "禁用拨号音",
    "Disable Emojis": "禁用表情符号",
    "Disable Focus Module": "禁用专注模式模块",
    "Disable Low Battery Sound": "禁用低电量提示音",
    "Disable Orientation Lock Module": "禁用方向锁定模块",
    "Disable Payment Sounds": "禁用支付提示音",
    "Disable Screen Mirroring Module": "禁用屏幕镜像模块",
    "Disable Slider Icons": "禁用滑块图标",
    "Disable Slider Icons ": "禁用滑块图标",
    "Enable Helvetica Font": "启用 Helvetica 字体",
    "Enable Helvetica Font ": "启用 Helvetica 字体",
    "Hide DND Icon": "隐藏勿扰图标",
    "Hide Delete Icon": "隐藏删除图标",
    "Hide Dock Background": "隐藏程序坞背景",
    "Hide Home Bar": "隐藏主屏幕横条",
    "Hide Large Battery Icon": "隐藏大电池图标",
    "Hide Lock Icon": "隐藏锁图标",
    "Hide Player Buttons": "隐藏播放器按钮",
    "Hide Quick Action Icons": "隐藏快捷操作图标",
    "Hide Ringer Icon": "隐藏静音图标",
    "Hide Tethering Icon": "隐藏个人热点图标",
    "Hide WiFi & Bluetooth Icons": "隐藏 Wi-Fi 与蓝牙图标",
    "Remove CC Background": "移除控制中心背景",
    "Remove Glassy Overlays": "移除玻璃质感浮层",
]
