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
- **Node.js**: v18.0.0 or later (with `npx` available in PATH)
- **Python**: 3.8 or later (Standard library only, no external pip dependencies needed)

## Quick Start

### Method 1: Use as an Antigravity Skill (Recommended)

1. Copy the [`skills/Chinesizing`](skills/Chinesizing) folder directly into your Antigravity global skills directory:
   - **Windows**: `%USERPROFILE%\.gemini\config\skills\Chinesizing\`
   - **macOS / Linux**: `~/.gemini/config/skills/Chinesizing/`
2. In your Antigravity chat, prompt:
   > "请根据 Chinesizing 技能对当前客户端进行汉化部署"
3. The agent will automatically run the safe deployment pipeline.

### Method 2: Standalone One-Click Installer

If you prefer running a direct script without an AI agent:

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

## How It Works

```mermaid
flowchart TD
    A["Pristine Backup (app.asar.bak)"] --> B["Decoupled Storage (i18n_data.json)"]
    B --> C["Safe Injection Engine (i18n_runner.js + Map Hook)"]
    C --> D["Full Lifecycle Guard (web-contents-created)"]
    D --> E["Syntax Gatekeeper (node --check)"]
    E -->|Passed| F["Sandbox Pack & Unpack Validation"]
    F -->|Verified| G["Atomic ASAR & Unpacked Sync"]
    G --> H["Live CDP Hot Reload"]
```

## License

[MIT](LICENSE) © 2026 Drippinblood333

## Disclaimer

This project is an independent open-source localization enhancement tool and is not officially affiliated with or endorsed by Google. Use responsibly for personal productivity.

---

<a name="chinese"></a>

## 中文说明

**Antigravity Chinese Locale (Chinesizing)** 是一套专为 Google Antigravity 桌面客户端打造的企业级全界面深度汉化方案与自主 AI 技能。彻底解决了传统外挂脚本导致的启动语法崩溃（`SyntaxError`）、下拉选项点击假死（`characterData` 微任务死循环）、受控组件键值脱节以及**退出重开变回英文**等顽疾，提供媲美官方原生的持久流畅体验。

支持作为 **Antigravity 智能体技能** (`Chinesizing`) 自动执行，亦可作为 **独立 Python 脚本** 一键安装与还原。

## 核心特性 (v3.0 重大里程碑)

- 🌐 **全界面深度覆盖（2,075+ 精准词条与 55 条正则规则）**：覆盖通用设置、外观主题、模型选择器与状态标签、用量配额刷新、MCP 协议管理、知识库卡片、项目与会话列表以及原生顶部窗口菜单（`menu.js`）。
- ⏱️ **智能相对时间与倒计时解析器**：动态抓取并流畅汉化用量配额刷新倒计时（如 `it will fully refresh in 6 days, 17 hours` ➔ `将在 6 天 17 小时后完全重置`），既保证语义通顺（信达雅），又规避高频时钟占位冲突。
- 🖥️ **完美适配 Antigravity 2.32+ 新版架构**：深度支持 Electron 2.32+ 换代的 `hubContents` 窗口生命周期及多行格式化 `app.whenReady()` 挂载点。
- 🔄 **全生命周期守卫（彻底攻克“重启/刷新失效”难题）**：
  - 在主进程注册 `app.on('web-contents-created')` 全局生命周期拦截网，全面监听 `dom-ready`、`did-finish-load` 与 `did-navigate-in-page`；
  - 在 `showOrCreateWindow` 唤醒链路中加入补救执行，保证从系统托盘唤醒时即刻保持汉化。
- ⚡ **纯值比对自愈引擎（弃用有害 WeakSet）**：
  - 弃用节点引用级的 `WeakSet` 永久黑名单，改用“纯值比对自愈”机制；SPA 路由跳转和异步组件重新渲染时自动毫秒级响应并汉化，绝不发生中途变回英文。
- 🧩 **内联切片文本（TextNode Fragmentation）精准缝合**：
  - 针对句子中间嵌套超链接（`<a>`）或 Badge 的复杂 DOM，细粒度切片匹配，杜绝半中半英。
- 🛡️ **彻底杜绝卡死与无限递归**：
  - 彻底剔除 `MutationObserver` 中的 `characterData` 监听，物理切断微任务事件风暴；
  - 引入 `isTranslating` 防重入原子锁，结合 3 秒级低频自愈巡检，DOM 扫描耗时低于 0.001 秒。
- 🔄 **底层双向映射桥（Bidirectional Map Bridge）**：
  - 全局代理 `Map.prototype.has` 与 `get` 方法，使 Base UI / Radix UI 等受控组件在收到汉化中文时，能够无缝反查底层原生英文键名，彻底解决选项拒收与焦点挂死（Focus Trap）。
- 🔒 **严格语法门禁**：
  - 在沙箱临时目录中执行“提取 ➔ 注入 ➔ `node --check` 静态语法分析 ➔ 试打包 ➔ 沙箱解包验证”完整闭环，验证通过才执行原子替换。
- ⚡ **零感知极速热重载与一键还原**：
  - 支持通过 Chrome DevTools 协议（CDP）对运行中的窗口进行热更新，无需立即重启客户端；
  - 附带 `--restore` 还原指令，随时一键无损退回官方原版。

## 环境要求

- **Google Antigravity 客户端**（支持 Windows / macOS / Linux）
- **Node.js**：v18.0.0 或更高版本（需在终端中可执行 `npx`）
- **Python**：3.8 或更高版本（仅使用标准库，无需额外 pip 安装）

## 快速开始

### 方式一：作为 Antigravity 技能使用（推荐）

1. 将本仓库中的 [`skills/Chinesizing`](skills/Chinesizing) 文件夹直接复制到 Antigravity 全局技能目录：
   - **Windows**: `%USERPROFILE%\.gemini\config\skills\Chinesizing\`
   - **macOS / Linux**: `~/.gemini/config/skills/Chinesizing/`
2. 在 Antigravity 对话框中发送：
   > “请根据 Chinesizing 技能对当前客户端进行汉化部署”
3. 智能体将自动依照标准工程规范执行全流程安装。

### 方式二：独立 Python 一键汉化脚本

如果你想脱离 Agent 直接在终端快速汉化：

```bash
git clone https://github.com/Drippinblood333/antigravity-chinese-locale.git
cd antigravity-chinese-locale

# 执行安装脚本
python scripts/deploy_chinese.py
```

脚本将自动寻找客户端路径、备份原版文件（`app.asar.bak`）、建立全生命周期守卫、执行沙箱门禁校验并安全写入，最后实时刷新窗口。

#### 一键还原 / 卸载

若需随时恢复为官方未修改的纯净版本，运行：

```bash
python scripts/deploy_chinese.py --restore
```

> **关于文件占用与重启提示**：Antigravity 默认在系统托盘后台运行。如果在部署或还原时提示文件权限受阻（Permission Denied），只需在任务栏右下角托盘图标右键选择 **退出**（或在任务管理器结束残留的 `Antigravity.exe` 进程）后重新运行脚本即可。

## 常见问题

- **问：官方版本自动更新后汉化失效了怎么办？**
  - **答**：重新运行一次 `python scripts/deploy_chinese.py` 即可。若需恢复官方纯净状态，执行 `python scripts/deploy_chinese.py --restore`。
- **问：动态倒计时和用量刷新时间是如何汉化的？**
  - **答**：在 v3.0 中，我们引入了专门的动态时间语义解析器，可在微秒级将 `it will fully refresh in X days, Y hours` 转化为 `将在 X 天 Y 小时后完全重置`，既避免了破坏时钟定时器，又实现了自然流畅的中文表达。

## 开源协议

本项目采用 [MIT 许可证](LICENSE) © 2026 Drippinblood333

## 免责声明

本项目仅供个人学习与效率优化研究使用，非 Google 官方产品，亦未获得官方背书。
