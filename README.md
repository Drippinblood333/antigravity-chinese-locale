# Antigravity Chinese Locale (Chinesizing)

A robust, enterprise-grade Chinese localization package and autonomous engineering skill for Google Antigravity. Designed with full WebContents lifecycle guards, zero runtime microtask loops, Base UI / React controlled component bridges, dynamic duration self-healing, and automated syntax gatekeepers to deliver a 100% persistent, crash-free, smooth native experience.

[English](#english) | [中文说明](#chinese)

---

<a name="english"></a>

## Overview

**Antigravity Chinese Locale** provides an enterprise-ready solution for translating Google Antigravity's desktop interface into Simplified Chinese. 

Unlike naive string-replacement scripts that cause Electron startup crashes (`SyntaxError`), dropdown freezes (from `characterData` microtask loops and Base UI key mismatch), or lose translations upon app restart/refresh (due to single-point `dom-ready` hooks and background tray process persistence), this project introduces an advanced **Full-Lifecycle Guard** and **Value-Matching Self-Healing Engine** that guarantees 100% persistence, speed, and rock-solid stability.

Available both as an **Autonomous Agent Skill** (`Chinesizing`) for Antigravity, and as an **Independent One-Click Python Installer & Restorer**.

## Features (v3.0 Milestone)

- 🌐 **Comprehensive Coverage (2,075+ Entries & 55 Rules)**: Fully localizes General Settings, Preferences, Appearance & Themes, Model Selectors & Tags, Dynamic Quotas, MCP Server Management, Knowledge Cards, Project Configuration, Session History, and Native Window Top Menus.
- ⏱️ **Intelligent Dynamic Duration Parsing**: Accurately localizes relative timestamps and quota replenishment countdowns (e.g., `it will fully refresh in 6 days, 17 hours` ➔ `将在 6 天 17 小时后完全重置`) without interfering with high-frequency timer cycles.
- 🖥️ **Full Antigravity 2.32+ Compatibility**: Robust AST/regex matching supporting Electron 2.32+ multi-line `app.whenReady()` initialization and `hubContents` window lifecycles.
- 🔄 **Persistent Lifecycle Guards (Solves Restart/Reload Bug)**:
  - Hooks directly into Electron's global `app.on('web-contents-created')` to monitor `dom-ready`, `did-finish-load`, and `did-navigate-in-page`.
  - Injects wake-up compensation into `showOrCreateWindow` to seamlessly re-apply localization when restoring from the background tray.
- ⚡ **Value-Matching Self-Healing (No Harmful WeakSet)**:
  - Abandons permanent `WeakSet` node blacklisting. Uses pure value comparison so dynamically rendered React nodes and SPA route changes are instantly and progressively localized without recursion.
- 🧩 **Fragmented TextNode Alignment**:
  - Handles nested tags (`<a>`, `<span>`, badges) by gracefully decomposing and pairing sliced text nodes, eliminating mixed Chinese/English sentences.
- 🛡️ **Zero-Hang Architecture**:
  - Excludes `characterData` from `MutationObserver` to prevent microtask recursive storms.
  - Implements an atomic `isTranslating` re-entrancy lock with a passive 3-second self-healing cycle.
- 🔄 **Bidirectional Map Bridge**:
  - Global `Map.prototype` proxy hook that automatically maps localized Chinese labels back to original English keys, fixing focus traps and selection freezes in Base UI & Radix UI dropdowns.
- 🔒 **Syntax Gatekeeper Pipeline**:
  - Enforces static code validation (`node --check`) in a temporary sandbox on `main.js`, `utils.js`, `menu.js`, and `i18n_runner.js` before modifying any production `app.asar` bundle.
- ⚡ **Zero-Restart Live Reload & Clean Uninstaller**:
  - Supports instant hot-reloading through Chrome DevTools Protocol (CDP).
  - Includes full `--restore` / `--uninstall` CLI capability to safely revert to original untouched binaries.

## Requirements

- **Google Antigravity Client** (Windows, macOS, or Linux)
- **Node.js**: v22.12.0 or later (with `npx` available in PATH)
- **Python**: 3.8 or later (Standard library only, no external pip dependencies needed)

## Quick Start

### Method 1: Standalone One-Click Installer (Recommended)

```bash
git clone https://github.com/Drippinblood333/antigravity-chinese-locale.git
cd antigravity-chinese-locale

# Run the installer
python scripts/deploy_chinese.py
```

The installer will automatically detect your Antigravity installation, create an `app.asar.bak` backup, verify syntax, pack the bundle, and hot-reload your interface.

#### Restoring / Uninstalling

To safely revert to the original unmodified official version:

```bash
python scripts/deploy_chinese.py --restore
```

> **Note on App Restart**: Antigravity runs in the background / system tray by default. If Windows reports file access permission errors during installation or restore, right-click the Antigravity icon in your system tray and select **Quit** (or terminate the process in Task Manager) before running the command.

### Method 2: Use as an Antigravity Skill

1. Copy the [`skills/Chinesizing`](skills/Chinesizing) folder directly into your Antigravity global skills directory:
   - **Windows**: `%USERPROFILE%\.gemini\config\skills\Chinesizing\`
   - **macOS / Linux**: `~/.gemini/config/skills/Chinesizing/`
2. In your Antigravity chat, prompt:
   > "请根据 Chinesizing 技能对当前客户端进行汉化部署"
3. The agent will automatically run the safe deployment pipeline.

## License

This project builds on [renkeshui/antigravity-chinese-locale](https://github.com/renkeshui/antigravity-chinese-locale). Drippinblood333 maintains the v3.0 updates in this repository. See the [MIT license](LICENSE) for the copyright notices and license terms.

## Disclaimer

This project is an independent open-source localization enhancement tool and is not officially affiliated with or endorsed by Google. Use responsibly for personal productivity.

---

<a name="chinese"></a>

## 中文说明

**Antigravity Chinese Locale** 是一个专为 Google Antigravity 打造的桌面端深度中文化补丁。

如果你用过早期的汉化脚本，大概率遇到过这些糟心问题：
- 软件关掉或者缩小到系统托盘再打开，**汉化直接失效**，又变回全英文；
- 点开设置里的模型下拉框，**界面直接卡死**、CPU 瞬间飙到 100%；
- 句子中间夹着链接或标签，翻译出来**半中半英**；
- 甚至打完补丁后客户端直接报 `SyntaxError` 白屏闪退。

本项目就是为了彻底终结这些痛点而开发的。它不是无脑的文本粗暴替换，而是深入 Antigravity 的 Electron 底层与 React 组件状态机制，实现真正**持久、稳定、零卡死**的原生级中文体验。

你可以把它当作 **Python 独立脚本** 一键安装/卸载，也可以作为 **Antigravity 智能体技能** (`Chinesizing`) 让 AI 自动帮你搞定。

## 为什么选择这个项目？

- 🌐 **全界面深度汉化（2075+ 词条 + 55 条动态规则）**  
  覆盖通用设置、外观主题、模型状态标签、用量配额、MCP 插件管理、项目列表以及 Windows 顶部原生系统菜单。所有词汇均依照国内开发者习惯人工校对，拒绝生硬机翻。
- 🔄 **退出重开不掉汉化（全生命周期拦截）**  
  直接挂载 Electron 的 `web-contents-created` 事件，无论是新建窗口、快捷键刷新（F5）、路由切换，还是从任务栏托盘休眠唤醒，客户端都会自动保持中文状态，再也不用每次开机重新跑脚本。
- 🛡️ **彻底告别下拉菜单卡死（受控组件反向映射）**  
  Antigravity 的前端采用 Base UI / React 受控组件，很多下拉菜单依赖原生英文标签作为状态 Key。如果强行把文本改成中文，组件就会因找不到 Key 而陷入事件死循环。我们在底层拦截代理了 `Map.prototype`，界面显示中文的同时，后台依然能秒级反查对应的英文 Key，完美解决点击假死与选项选不中的问题。
- ⚡ **无死循环、超低资源占用**  
  坚决不开启容易引发微任务死循环的 `characterData` 深度监听，配合原子级防重入锁，页面扫描耗时通常小于 1 毫秒，操作毫无迟滞感。
- ⏱️ **动态倒计时智能中文化**  
  模型额度刷新倒计时（例如 `it will fully refresh in 6 days, 17 hours`）由专属语义模块动态接管，自然转换为“将在 6 天 17 小时后完全重置”，既读得顺畅，又不会干扰前端原本的高频时钟渲染。
- 🔒 **自动化语法门禁与一键无损还原**  
  在打包写入前，会在临时沙箱中自动执行 `node --check` 语法静态检查和模拟打包解包测试，校验 100% 通过后才会安全替换文件，绝不会破坏你的客户端。自带 `--restore` 还原指令，随时一键退回官方原版。

## 环境要求

- **Google Antigravity 客户端**（支持 Windows / macOS / Linux）
- **Node.js**：v22.12.0 或以上（用于打包与语法校验，终端需能运行 `npx`）
- **Python**：3.8 或以上（仅调用标准库，不需要 `pip` 安装任何第三方依赖）

## 快速上手

### 方式一：独立 Python 脚本一键安装（推荐）

打开终端，拉取代码直接运行即可：

```bash
git clone https://github.com/Drippinblood333/antigravity-chinese-locale.git
cd antigravity-chinese-locale

# 运行汉化部署
python scripts/deploy_chinese.py
```

脚本会自动识别你的 Antigravity 安装目录、生成官方原版备份（`app.asar.bak`）、注入代码、完成语法自检并实时热刷新当前窗口。

> **💡 温馨提示（关于后台托盘占用）**：  
> Antigravity 默认在后台托盘常驻。如果脚本执行时提示文件被占用（Permission Denied），只需在电脑右下角托盘图标上**右键选择退出**（或在任务管理器中结束 `Antigravity.exe`），重新执行一次命令即可。

#### 随时一键还原官方原版

如果你需要恢复到未修改的纯净官方版，随时执行：

```bash
python scripts/deploy_chinese.py --restore
```

### 方式二：作为 Antigravity Skill 技能使用

1. 将仓库中的 [`skills/Chinesizing`](skills/Chinesizing) 文件夹复制到你的 Antigravity 技能目录：
   - **Windows**: `%USERPROFILE%\.gemini\config\skills\Chinesizing\`
   - **macOS / Linux**: `~/.gemini/config/skills/Chinesizing/`
2. 在 Antigravity 对话框中直接对 AI 发送：
   > “请根据 Chinesizing 技能对当前客户端进行汉化部署”
3. AI 将全自动按照工程规范帮你完成检测与安全写入。

## 常见问题解答 (FAQ)

- **Q：官方客户端自动更新了，汉化掉了怎么办？**  
  **A**：官方更新会覆盖核心文件，只需重新在终端运行一次 `python scripts/deploy_chinese.py` 即可几秒内重新打上补丁。
- **Q：用这个会有账号风险吗？**  
  **A**：完全不会。本项目仅在本地 Electron 渲染层与主进程做界面中文化呈现，不修改任何网络通信包，不拦截任何 API 请求，不包含任何外部网络上传代码，纯本地安全运行。
- **Q：遇到界面个别生僻单词还没汉化？**  
  **A**：欢迎提交 Issue 或 PR！字典文件存放在 `scripts/i18n_data.json` 中，结构清晰，欢迎随时补充。

## 开源许可

本项目基于 [renkeshui 的 antigravity-chinese-locale](https://github.com/renkeshui/antigravity-chinese-locale) 开发，由 Drippinblood333 维护本仓库的 v3.0 更新。版权声明和许可条款见 [MIT 许可证](LICENSE)。

## 免责声明

本项目仅供个人开发学习与本地效率优化使用，属于第三方开源社区项目，与 Google 官方无关。
