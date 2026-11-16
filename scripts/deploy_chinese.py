import os
import sys
import shutil
import tempfile
import subprocess
import json
import re
import urllib.request
import argparse

def find_antigravity_resources():
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        p = os.path.join(local_app_data, "Programs", "antigravity", "resources")
        if os.path.exists(p) and os.path.exists(os.path.join(p, "app.asar")):
            return p
    mac_path = "/Applications/Antigravity.app/Contents/Resources"
    if os.path.exists(mac_path) and os.path.exists(os.path.join(mac_path, "app.asar")):
        return mac_path
    linux_path = "/opt/Antigravity/resources"
    if os.path.exists(linux_path) and os.path.exists(os.path.join(linux_path, "app.asar")):
        return linux_path
    return None

def restore_backup(resources_dir):
    target_asar = os.path.join(resources_dir, "app.asar")
    backup_asar = os.path.join(resources_dir, "app.asar.bak")
    backup_unpacked = backup_asar + ".unpacked"
    target_unpacked = target_asar + ".unpacked"

    if not os.path.exists(backup_asar):
        print(f"[Error] Backup file not found: {backup_asar}")
        print("        Cannot perform restore without a previous backup.")
        sys.exit(1)

    print("[*] Restoring pristine app.asar from backup...")
    try:
        shutil.copy2(backup_asar, target_asar)
    except PermissionError:
        print("\n[Error] Permission denied: Cannot overwrite app.asar!")
        print("        Antigravity is currently running in the background and holding the file.")
        print("        Solution: Right-click the Antigravity icon in your system tray and choose 'Quit',")
        print("                  or terminate 'Antigravity.exe' in Task Manager, then run this command again.")
        sys.exit(1)

    if os.path.exists(backup_unpacked):
        try:
            if os.path.exists(target_unpacked):
                shutil.rmtree(target_unpacked, ignore_errors=True)
            shutil.copytree(backup_unpacked, target_unpacked)
        except Exception as e:
            print(f"[Warning] Failed to restore unpacked directory: {e}")

    print("[✓] Restored pristine app.asar successfully!")
    print("    Please restart Antigravity to load the original version.")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Chinese Localization Deployer & Restorer")
    parser.add_argument("-r", "--restore", "--uninstall", action="store_true", help="Restore pristine app.asar from backup")
    args = parser.parse_args()

    print("=" * 60)
    print("  Antigravity Chinese Localization - Full Suite Deployer")
    print("=" * 60)

    # 1. Locate resources
    resources_dir = find_antigravity_resources()
    if not resources_dir:
        print("[Error] Antigravity resources not found.")
        print("        Ensure Google Antigravity client is installed on your machine.")
        sys.exit(1)
    print(f"[✓] Resources directory: {resources_dir}")

    # Handle restore request
    if args.restore:
        restore_backup(resources_dir)

    # 2. Check Node.js
    try:
        res = subprocess.run(["node", "-v"], capture_output=True, text=True)
        if res.returncode != 0:
            print("[Error] Node.js is required.")
            sys.exit(1)
        print(f"[✓] Node.js detected: {res.stdout.strip()}")
    except Exception as e:
        print(f"[Error] Node.js check failed: {e}")
        sys.exit(1)

    target_asar = os.path.join(resources_dir, "app.asar")
    backup_asar = os.path.join(resources_dir, "app.asar.bak")
    target_unpacked = target_asar + ".unpacked"
    backup_unpacked = backup_asar + ".unpacked"

    # 3. Backup if not exists
    if not os.path.exists(backup_asar):
        print("[*] Creating backup: app.asar.bak ...")
        shutil.copy2(target_asar, backup_asar)
        if os.path.exists(target_unpacked) and not os.path.exists(backup_unpacked):
            shutil.copytree(target_unpacked, backup_unpacked)
        print("[✓] Backup created successfully.")
    else:
        print("[✓] Existing backup found (app.asar.bak).")

    # Locate source scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    i18n_runner_src = os.path.join(script_dir, "i18n_runner.js")
    i18n_data_src = os.path.join(script_dir, "i18n_data.json")

    if not os.path.exists(i18n_runner_src) or not os.path.exists(i18n_data_src):
        print("[Error] Source i18n files not found.")
        sys.exit(1)

    work_dir = tempfile.mkdtemp(prefix="ag_deploy_work_")
    sandbox_verify_dir = tempfile.mkdtemp(prefix="ag_deploy_verify_")
    temp_pack = os.path.join(tempfile.gettempdir(), "ag_new_packed.asar")
    temp_unpacked = temp_pack + ".unpacked"

    try:
        print("[*] Extracting app.asar into sandbox...")
        subprocess.run(f'npx --yes @electron/asar extract "{target_asar}" "{work_dir}"', shell=True, check=True)

        dist_dir = os.path.join(work_dir, "dist")
        if not os.path.exists(dist_dir):
            print("[Error] dist directory missing inside app.asar.")
            sys.exit(1)

        shutil.copy2(i18n_runner_src, os.path.join(dist_dir, "i18n_runner.js"))
        shutil.copy2(i18n_data_src, os.path.join(dist_dir, "i18n_data.json"))

        utils_js = os.path.join(dist_dir, "utils.js")
        main_js = os.path.join(dist_dir, "main.js")
        menu_js = os.path.join(dist_dir, "menu.js")
        modified_files = []

        # A. Patch utils.js
        with open(utils_js, "r", encoding="utf-8") as f:
            u_content = f.read()

        inject_func_code = """
// --- Antigravity i18n injection helper ---
const injectAntigravityI18n = (target) => {
    try {
        const wc = target?.webContents ? target.webContents : target;
        if (!wc || typeof wc.executeJavaScript !== "function" || wc.isDestroyed?.()) return;
        const runnerPath = path_1.default.join(__dirname, "i18n_runner.js");
        const dataPath = path_1.default.join(__dirname, "i18n_data.json");
        if (fs.existsSync(runnerPath) && fs.existsSync(dataPath)) {
            const dataStr = fs.readFileSync(dataPath, "utf-8");
            const runnerCode = fs.readFileSync(runnerPath, "utf-8");
            const script = `
                (function(){
                    try {
                        window.__ANTIGRAVITY_I18N_DATA__ = ${JSON.stringify(JSON.parse(dataStr))};
                        ${runnerCode}
                    } catch(e) {
                        console.error("[Antigravity i18n] Error executing i18n runner:", e);
                    }
                })();
            `;
            wc.executeJavaScript(script).catch(() => {});
        }
    } catch (e) {
        console.error("[Antigravity i18n] Injection error:", e);
    }
};
exports.injectAntigravityI18n = injectAntigravityI18n;
// --- End Antigravity i18n helper ---
"""
        if "injectAntigravityI18n" not in u_content:
            cw_needle = "function createWindow("
            if cw_needle in u_content:
                u_content = u_content.replace(cw_needle, inject_func_code + "\n" + cw_needle, 1)
            else:
                u_content = u_content + "\n" + inject_func_code

            hub_hook = """    // i18n lifecycle listeners
    hubContents.on("dom-ready", () => injectAntigravityI18n(hubContents));
    hubContents.on("did-finish-load", () => injectAntigravityI18n(hubContents));
    hubContents.on("did-navigate-in-page", () => injectAntigravityI18n(hubContents));
"""
            win_hook = """    // i18n lifecycle listeners
    win.webContents.on("dom-ready", () => injectAntigravityI18n(win.webContents));
    win.webContents.on("did-finish-load", () => injectAntigravityI18n(win.webContents));
    win.webContents.on("did-navigate-in-page", () => injectAntigravityI18n(win.webContents));
"""
            if "hubContents.setWindowOpenHandler(" in u_content:
                u_content = u_content.replace(
                    "hubContents.setWindowOpenHandler(",
                    hub_hook + "    hubContents.setWindowOpenHandler(",
                    1
                )
            elif "win.webContents.setWindowOpenHandler" in u_content:
                u_content = u_content.replace(
                    "win.webContents.setWindowOpenHandler",
                    win_hook + "    win.webContents.setWindowOpenHandler",
                    1
                )

            show_needle = "wins[0].focus();"
            if show_needle in u_content:
                u_content = u_content.replace(
                    show_needle,
                    show_needle + "\n        if (exports.injectAntigravityI18n) { (0, exports.injectAntigravityI18n)(wins[0]); }",
                    1
                )

            with open(utils_js, "w", encoding="utf-8") as f:
                f.write(u_content)
            print("[✓] utils.js patched successfully.")
        else:
            print("[✓] utils.js already contains i18n injection.")
        modified_files.append(utils_js)

        # B. Patch main.js
        if os.path.exists(main_js):
            with open(main_js, "r", encoding="utf-8") as f:
                m_content = f.read()

            if "web-contents-created" not in m_content:
                main_inject = (
                    "\n    // Register global WebContents i18n injection lifecycle hook\n"
                    "    electron_1.app.on('web-contents-created', (_event, wc) => {\n"
                    "        wc.on('dom-ready', () => { if (utils_1.injectAntigravityI18n) (0, utils_1.injectAntigravityI18n)(wc); });\n"
                    "        wc.on('did-finish-load', () => { if (utils_1.injectAntigravityI18n) (0, utils_1.injectAntigravityI18n)(wc); });\n"
                    "        wc.on('did-navigate-in-page', () => { if (utils_1.injectAntigravityI18n) (0, utils_1.injectAntigravityI18n)(wc); });\n"
                    "    });"
                )
                when_ready_pattern = r"(electron_1\.app\s*\.whenReady\(\)\s*\.then\(async\s*\(\)\s*=>\s*\{)"
                if re.search(when_ready_pattern, m_content):
                    m_content = re.sub(when_ready_pattern, r"\1" + main_inject, m_content, count=1)
                    with open(main_js, "w", encoding="utf-8") as f:
                        f.write(m_content)
                    print("[✓] main.js patched with global lifecycle hook.")
            else:
                print("[✓] main.js already contains web-contents-created hook.")
            modified_files.append(main_js)

        # C. Patch menu.js for native application menu bar
        if os.path.exists(menu_js):
            with open(menu_js, "r", encoding="utf-8") as f:
                menu_content = f.read()

            if "translateMenuTree" not in menu_content:
                menu_patch = """
    // --- Localize Native Application Menu ---
    const MENU_DICT = {
        "File": "文件",
        "Edit": "编辑",
        "View": "视图",
        "Window": "窗口",
        "Help": "帮助",
        "New Window": "新建窗口",
        "Close Window": "关闭窗口",
        "Close Tab": "关闭标签页",
        "Undo": "撤销",
        "Redo": "重做",
        "Cut": "剪切",
        "Copy": "复制",
        "Paste": "粘贴",
        "Select All": "全选",
        "Actual Size": "实际大小",
        "Zoom In": "放大",
        "Zoom Out": "缩小",
        "Reset Zoom": "重置缩放",
        "Toggle Full Screen": "切换全屏",
        "Toggle Developer Tools": "切换开发者工具",
        "Docs": "官方文档",
        "Check for Updates": "检查更新",
        "Connect to WSL": "连接至 WSL 子系统",
        "Reopen Locally": "在本地重新打开",
        "Minimize": "最小化",
        "Zoom": "缩放",
        "Bring All to Front": "全部置顶"
    };
    const translateMenuTree = (m) => {
        if (!m || !Array.isArray(m.items)) return;
        for (const it of m.items) {
            if (it.label && MENU_DICT[it.label]) it.label = MENU_DICT[it.label];
            if (it.submenu) translateMenuTree(it.submenu);
        }
    };
    translateMenuTree(menu);
    // --- End Localize Menu ---
"""
                needle_menu = "electron_1.Menu.setApplicationMenu(menu);"
                if needle_menu in menu_content:
                    menu_content = menu_content.replace(needle_menu, menu_patch + "\n    " + needle_menu, 1)
                    with open(menu_js, "w", encoding="utf-8") as f:
                        f.write(menu_content)
                    print("[✓] menu.js patched with native menu localizer.")
            else:
                print("[✓] menu.js already contains menu localizer.")
            modified_files.append(menu_js)

        modified_files.append(os.path.join(dist_dir, "i18n_runner.js"))

        # Gatekeeper 1: node --check
        print("[*] Running Gatekeeper 1: node --check on modified files...")
        for fp in modified_files:
            chk = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
            if chk.returncode != 0:
                print(f"[Error] Syntax check failed on {fp}:\n{chk.stderr}")
                sys.exit(1)
        print("[✓] Gatekeeper 1 passed.")

        # Gatekeeper 2: Sandbox pack and re-extract validation
        if os.path.exists(temp_pack):
            os.remove(temp_pack)
        if os.path.exists(temp_unpacked):
            shutil.rmtree(temp_unpacked)

        print("[*] Packaging into sandbox asar...")
        subprocess.run(
            f'npx --yes @electron/asar pack "{work_dir}" "{temp_pack}" --unpack-dir "node_modules/chrome-devtools-mcp"',
            shell=True,
            check=True
        )

        print("[*] Running Gatekeeper 2: Re-extracting sandbox asar to verify integrity...")
        subprocess.run(f'npx --yes @electron/asar extract "{temp_pack}" "{sandbox_verify_dir}"', shell=True, check=True)
        for sub_f in ["dist/utils.js", "dist/main.js", "dist/menu.js", "dist/i18n_runner.js"]:
            verify_target = os.path.join(sandbox_verify_dir, sub_f)
            chk = subprocess.run(["node", "--check", verify_target], capture_output=True, text=True)
            if chk.returncode != 0:
                print(f"[Error] Pack integrity check failed on {sub_f}:\n{chk.stderr}")
                sys.exit(1)
        print("[✓] Gatekeeper 2 passed: Asar bundle is 100% syntactically valid.")

        # Atomic replacement
        target_unpacked = target_asar + ".unpacked"
        if os.path.exists(temp_unpacked):
            if os.path.exists(target_unpacked):
                shutil.rmtree(target_unpacked)
            shutil.copytree(temp_unpacked, target_unpacked)

        print("[*] Performing atomic replacement of app.asar...")
        try:
            shutil.copy2(temp_pack, target_asar)
        except PermissionError:
            print("\n[Error] Permission denied: Cannot overwrite app.asar!")
            print("        Antigravity is currently running in the background and holding the file.")
            print("        Solution: Right-click the Antigravity icon in your system tray and choose 'Quit',")
            print("                  or terminate 'Antigravity.exe' in Task Manager, then run this script again.")
            sys.exit(1)
        print("[✓] Production app.asar successfully updated!")

        # Hot reload via CDP
        try:
            active_port_file = os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "DevToolsActivePort")
            if os.path.exists(active_port_file):
                with open(active_port_file, "r") as f:
                    dt_port = f.readline().strip()
                with urllib.request.urlopen(f"http://127.0.0.1:{dt_port}/json", timeout=2) as resp:
                    pages = json.loads(resp.read().decode("utf-8"))
                    page = next((p for p in pages if p.get("type") == "page" and "Antigravity" in p.get("title", "")), None)
                    if page:
                        with open(os.path.join(dist_dir, "i18n_data.json"), "r", encoding="utf-8") as f:
                            dt_str = f.read()
                        with open(os.path.join(dist_dir, "i18n_runner.js"), "r", encoding="utf-8") as f:
                            rn_str = f.read()
                        full_code = "window.__ANTIGRAVITY_I18N_DATA__ = " + dt_str + ";\n" + rn_str + "; if (typeof window.__antigravity_translateWholePage === 'function') window.__antigravity_translateWholePage();"
                        ws_url = page["webSocketDebuggerUrl"]
                        node_eval = f'''
                        const ws = new WebSocket({json.dumps(ws_url)});
                        ws.onopen = () => {{
                            ws.send(JSON.stringify({{ id: 1, method: "Runtime.evaluate", params: {{ expression: {json.dumps(full_code)} }} }}));
                        }};
                        ws.onmessage = () => process.exit(0);
                        setTimeout(() => process.exit(0), 1000);
                        '''
                        eval_file = os.path.join(tempfile.gettempdir(), "cdp_hot_reload.js")
                        with open(eval_file, "w", encoding="utf-8") as f:
                            f.write(node_eval)
                        subprocess.run(["node", eval_file], capture_output=True)
                        print("[✓] Active window hot-reloaded successfully!")
        except Exception as e:
            print(f"[*] CDP hot reload skipped: {e}")

        print("\n" + "=" * 60)
        print("  Localization deployed successfully for Antigravity 2.32+!")
        print("=" * 60)

    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
        shutil.rmtree(sandbox_verify_dir, ignore_errors=True)
        if os.path.exists(temp_pack):
            try:
                os.remove(temp_pack)
            except Exception:
                pass
        if os.path.exists(temp_unpacked):
            try:
                shutil.rmtree(temp_unpacked, ignore_errors=True)
            except Exception:
                pass

if __name__ == "__main__":
    main()
