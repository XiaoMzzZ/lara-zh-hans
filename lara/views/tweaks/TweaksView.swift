//
//  TweaksView.swift
//  lara
//
//  Created by lunginspector on 5/3/26.
//

import SwiftUI

struct TweaksView: View {
    @AppStorage("logsdisplaymode") private var selectedlogsdisplaymode: logsdisplaymode = .toolbar
    @ObservedObject var mgr: laramgr
    
    var body: some View {
        NavigationStack {
            List {
                Section(header: HeaderLabel(text: "SpringBoard", icon: "house")) {
                    NavigationLink("RemoteCall 定制器", destination: RemoteView(mgr: mgr))
                        .disabled(!mgr.rcready)
                    NavigationLink("液态玻璃", destination: LiquidGlassView())
                        .disabled(!mgr.vfsready)
                    NavigationLink("SpringBoard 定制器", destination: SpringBoardView(mgr: mgr))
                        .disabled(!mgr.vfsready)
                }
                
                Section(header: HeaderLabel(text: "锁屏", icon: "lock")) {
                    NavigationLink("密码界面主题", destination: PasscodeView(mgr: mgr))
                        .disabled(!mgr.sbxready)
                }
                
                Section(header: HeaderLabel(text: "应用", icon: "app")) {
                    NavigationLink("卡片覆盖", destination: CardView())
                        .disabled(!mgr.vfsready)
                    NavigationLink("应用解密", destination: DecryptView())
                        .disabled(!mgr.sbxready)
                    NavigationLink("绕过 3 个应用限制", destination: AppsView())
                        .disabled(!mgr.sbxready)
                    NavigationLink("解除黑名单", destination: WhitelistView())
                        .disabled(!mgr.sbxready)
                    NavigationLink("JIT 启用器", destination: JitView())
                        .disabled(!mgr.sbxready)
                }
                
                Section(header: HeaderLabel(text: "用户界面", icon: "eye")) {
                    NavigationLink("dirtyZero", destination: dirtyZeroView())
                        .disabled(!mgr.vfsready)
                    NavigationLink("显示隐藏图标", destination: ShowHiddenIconsView(mgr: mgr))
                        .disabled(!mgr.sbxready && !mgr.vfsready)
                    NavigationLink("MobileGestalt", destination: GestaltView(mgr: mgr))
                        .disabled(!mgr.sbxready)
                    NavigationLink("字体覆盖", destination: FontPicker(mgr: mgr))
                        .disabled(!mgr.vfsready)
                    NavigationLink("SystemColor 修补器", destination: SystemColor(mgr: mgr))
                        .disabled(!mgr.sbxready || !mgr.vfsready)
                }
                
                Section(header: HeaderLabel(text: "系统", icon: "gear")) {
                    NavigationLink("VarClean 清理", destination: VarCleanView())
                        .disabled(!mgr.sbxready)
                    NavigationLink("自定义覆盖", destination: CustomView(mgr: mgr))
                        .disabled(!mgr.vfsready)
                    NavigationLink("OTA 更新", destination: OTAView(mgr: mgr))
                    NavigationLink("屏幕使用时间", destination: ScreenTimeView(mgr: mgr))
                }
                
                Section(header: HeaderLabel(text: "已失效", icon: "exclamationmark.triangle.fill")) {
                    NavigationLink("DarkBoard", destination: DarkBoardView())
                        .disabled(true)
                }
                
                NavigationLink("额外工具", destination: ToolsView())
            }
            .disabled(!mgr.dsready)
            .navigationTitle("调整")
            .toolbar {
                if selectedlogsdisplaymode == .toolbar {
                    Button(action: {
                        mgr.showLogs.toggle()
                    }) {
                        Image(systemName: "terminal")
                    }
                }
            }
        }
    }
}
