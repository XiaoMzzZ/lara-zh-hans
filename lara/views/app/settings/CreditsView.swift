//
//  CreditsView.swift
//  lara
//
//  Created by lunginspector on 5/9/26.
//

import SwiftUI

struct CreditsView: View {
    var body: some View {
        NavigationStack {
            List {
                LinkCreditCell(name: "roooot", description: "主要开发者", url: "https://github.com/rooootdev") {
                    LinkCreditIcon(url: "https://github.com/rooootdev.png")
                }
                LinkCreditCell(name: "wh1te4ever", description: "制作了 darksword-kexploit-fun", url: "https://github.com/wh1te4ever") {
                    LinkCreditIcon(url: "https://github.com/wh1te4ever.png")
                }
                LinkCreditCell(name: "Duy Tran", description: "多项 RemoteCall 相关改进与功能", url: "https://github.com/khanhduytran0") {
                    LinkCreditIcon(url: "https://github.com/khanhduytran0.png")
                }
                LinkCreditCell(name: "AppInstalleriOS", description: "协助处理偏移以及大量其他工作", url: "https://github.com/AppInstalleriOSGH") {
                    LinkCreditIcon(url: "https://github.com/AppInstalleriOSGH.png")
                }
                LinkCreditCell(name: "jailbreak.party", description: "dirtyZero 调整", url: "https://github.com/jailbreakdotparty") {
                    LinkCreditIcon(url: "https://github.com/jailbreakdotparty.png")
                }
                LinkCreditCell(name: "lunginspector", description: "前端重写", url: "https://github.com/lunginspector") {
                    LinkCreditIcon(url: "https://github.com/lunginspector.png")
                }
                LinkCreditCell(name: "Jurre", description: "EditorView、PocketPoster 助手及多项改进", url: "https://github.com/jurre111") {
                    LinkCreditIcon(url: "https://github.com/jurre111.png")
                }
                LinkCreditCell(name: "neon", description: "注销重启脚本、zipmgr、修复密码主题、新增应用解密", url: "https://github.com/neonmodder123") {
                    LinkCreditIcon(url: "https://github.com/neonmodder123.png")
                }
                LinkCreditCell(name: "Skadz", description: "注销重启方式", url: "https://github.com/skadz108") {
                    LinkCreditIcon(url: "https://github.com/skadz108.png")
                }
                LinkCreditCell(name: "hxhlb", description: "多项问题修复", url: "https://github.com/hxhlb") {
                    LinkCreditIcon(url: "https://github.com/hxhlb.png")
                }
                LinkCreditCell(name: "leminlimez", description: "多项 Cowabunga 调整", url: "https://github.com/leminlimez") {
                    LinkCreditIcon(url: "https://github.com/leminlimez.png")
                }
            }
            .navigationTitle("致谢")
        }
    }
}
