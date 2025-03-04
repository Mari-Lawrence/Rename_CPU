import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import winreg
import ctypes
import re
import logging
import json
import os
from datetime import datetime

# 配置日志记录
logging.basicConfig(filename="cpu_name_editor.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 定义注册表路径和键值
CPU_REGISTRY_PATH = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
VALUE_NAME = "ProcessorNameString"
BACKUP_FILE = "cpu_name_backup.json"
HISTORY_FILE = "cpu_name_history.json"

# 语言字典
LANGUAGES = {
    "zh": {
        "title": "修改 CPU 名称工具",
        "input_label": "输入新的 CPU 名称:",
        "modify_button": "修改名称",
        "restore_button": "恢复原始名称",
        "switch_button": "切换语言 / Switch Language",
        "theme_button": "切换主题",
        "success": "成功",
        "modify_success": "CPU 名称已修改为: {}",
        "restore_success": "CPU 名称已恢复为: {}",
        "error": "错误",
        "modify_error": "修改注册表时出错: {}",
        "restore_error": "恢复注册表时出错: {}",
        "admin_error": "请以管理员身份运行此程序。",
        "invalid_input": "无效输入，请输入有效的 CPU 名称（仅限字母、数字、空格、括号、短横线）。",
        "restart_hint": "可能需要重新启动计算机以使更改生效。",
        "dont_show_again": "不再提示",
        "current_cpu_label": "当前 CPU 名称:",
        "undo_button": "撤销",
        "history_button": "查看历史记录",
        "system_info_label": "系统信息",
        "backup_created": "已创建备份: {}",
        "backup_restored": "已从备份恢复: {}",
        "history_cleared": "历史记录已清除",
        "no_history": "没有历史记录",
        "history_title": "修改历史记录"
    },
    "en": {
        "title": "Modify CPU Name Tool",
        "input_label": "Enter new CPU name:",
        "modify_button": "Modify Name",
        "restore_button": "Restore Original Name",
        "switch_button": "Switch Language / 切换语言",
        "theme_button": "Switch Theme",
        "success": "Success",
        "modify_success": "CPU name changed to: {}",
        "restore_success": "CPU name restored to: {}",
        "error": "Error",
        "modify_error": "Error modifying registry: {}",
        "restore_error": "Error restoring registry: {}",
        "admin_error": "Please run this program as administrator.",
        "invalid_input": "Invalid input, please enter a valid CPU name (letters, numbers, spaces, brackets, dashes only).",
        "restart_hint": "A system restart may be required for changes to take effect.",
        "dont_show_again": "Do not show again",
        "current_cpu_label": "Current CPU Name:",
        "undo_button": "Undo",
        "history_button": "View History",
        "system_info_label": "System Info",
        "backup_created": "Backup created: {}",
        "backup_restored": "Backup restored: {}",
        "history_cleared": "History cleared",
        "no_history": "No history available",
        "history_title": "Modification History"
    }
}

current_lang = "zh"
original_cpu_name = ""
dont_show_restart_hint = False
history = []
backup = {}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_original_cpu_name():
    global original_cpu_name
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_READ)
        original_cpu_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.CloseKey(reg_key)
        if 'current_cpu_label' in globals():  # 检查 current_cpu_label 是否已定义
            current_cpu_label.configure(text=f"{LANGUAGES[current_lang]['current_cpu_label']} {original_cpu_name}")
    except Exception as e:
        messagebox.showerror(LANGUAGES[current_lang]["error"], f"无法获取原始 CPU 名称: {e}")

def validate_input(name):
    return bool(re.match(r"^[ A-Za-z0-9()-]+$", name))

def modify_cpu_name(new_name):
    global dont_show_restart_hint, history
    if not validate_input(new_name):
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["invalid_input"])
        return
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
        current_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, new_name)
        winreg.CloseKey(reg_key)
        logging.info(f"CPU 名称修改为: {new_name}")
        messagebox.showinfo(LANGUAGES[current_lang]["success"],
                            LANGUAGES[current_lang]["modify_success"].format(new_name))
        history.append({"action": "modify", "from": current_name, "to": new_name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_history()
        update_current_cpu_name(new_name)
        create_backup(current_name)

        if not dont_show_restart_hint:
            restart_hint_window()
    except Exception as e:
        logging.error(f"修改注册表时出错: {e}")
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["modify_error"].format(e))

def restore_cpu_name():
    try:
        if not original_cpu_name:
            messagebox.showerror(LANGUAGES[current_lang]["error"], "未找到原始 CPU 名称，可能需要重新启动应用。")
            return
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
        current_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, original_cpu_name)
        winreg.CloseKey(reg_key)
        logging.info("CPU 名称已恢复")
        messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["restore_success"].format(original_cpu_name))
        history.append({"action": "restore", "from": current_name, "to": original_cpu_name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_history()
        update_current_cpu_name(original_cpu_name)
    except Exception as e:
        logging.error(f"恢复注册表时出错: {e}")
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["restore_error"].format(e))

def restart_hint_window():
    global dont_show_restart_hint
    hint_window = ctk.CTk()
    hint_window.title("提示")
    hint_window.geometry("300x150")

    label = ctk.CTkLabel(hint_window, text=LANGUAGES[current_lang]["restart_hint"])
    label.pack(pady=10)

    def set_dont_show():
        global dont_show_restart_hint
        dont_show_restart_hint = dont_show_var.get()

    dont_show_var = tk.BooleanVar(value=True)
    dont_show_checkbox = ctk.CTkCheckBox(hint_window, text=LANGUAGES[current_lang]["dont_show_again"],
                                         variable=dont_show_var, command=set_dont_show)
    dont_show_checkbox.pack(pady=5)

    close_button = ctk.CTkButton(hint_window, text="OK", command=hint_window.destroy)
    close_button.pack(pady=10)

    hint_window.mainloop()

def switch_language():
    global current_lang
    current_lang = "en" if current_lang == "zh" else "zh"
    update_ui()

def switch_theme():
    current_theme = ctk.get_appearance_mode()
    new_theme = "Dark" if current_theme == "Light" else "Light"
    ctk.set_appearance_mode(new_theme)

def update_ui():
    root.title(LANGUAGES[current_lang]["title"])
    title_label.configure(text=LANGUAGES[current_lang]["title"])
    label.configure(text=LANGUAGES[current_lang]["input_label"])
    modify_button.configure(text=LANGUAGES[current_lang]["modify_button"])
    restore_button.configure(text=LANGUAGES[current_lang]["restore_button"])
    switch_button.configure(text=LANGUAGES[current_lang]["switch_button"])
    theme_button.configure(text=LANGUAGES[current_lang]["theme_button"])
    current_cpu_label.configure(text=f"{LANGUAGES[current_lang]['current_cpu_label']} {get_current_cpu_name()}")
    undo_button.configure(text=LANGUAGES[current_lang]["undo_button"])
    history_button.configure(text=LANGUAGES[current_lang]["history_button"])
    system_info_label.configure(text=LANGUAGES[current_lang]["system_info_label"])

def get_current_cpu_name():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_READ)
        current_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.CloseKey(reg_key)
        return current_name
    except Exception as e:
        messagebox.showerror(LANGUAGES[current_lang]["error"], f"无法获取当前 CPU 名称: {e}")
        return "未知"

def update_current_cpu_name(name):
    current_cpu_label.configure(text=f"{LANGUAGES[current_lang]['current_cpu_label']} {name}")

def create_backup(name):
    global backup
    backup = {"name": name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open(BACKUP_FILE, "w") as f:
        json.dump(backup, f)
    logging.info(f"备份已创建: {backup}")
    messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["backup_created"].format(backup["timestamp"]))

def restore_backup():
    global backup
    if not os.path.exists(BACKUP_FILE):
        messagebox.showerror(LANGUAGES[current_lang]["error"], "没有可用的备份文件。")
        return
    with open(BACKUP_FILE, "r") as f:
        backup = json.load(f)
    modify_cpu_name(backup["name"])
    messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["backup_restored"].format(backup["timestamp"]))

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

def show_history():
    if not history:
        messagebox.showinfo(LANGUAGES[current_lang]["history_title"], LANGUAGES[current_lang]["no_history"])
        return
    history_window = ctk.CTk()
    history_window.title(LANGUAGES[current_lang]["history_title"])
    history_window.geometry("400x300")

    for entry in history:
        label = ctk.CTkLabel(history_window, text=f"{entry['timestamp']}: {entry['action']} {entry['from']} -> {entry['to']}")
        label.pack(pady=5)

    clear_button = ctk.CTkButton(history_window, text="Clear History", command=clear_history)
    clear_button.pack(pady=10)

    history_window.mainloop()

def clear_history():
    global history
    history = []
    save_history()
    messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["history_cleared"])

def undo_last_action():
    if not history:
        messagebox.showinfo(LANGUAGES[current_lang]["error"], "没有可撤销的操作。")
        return
    last_action = history[-1]
    if last_action["action"] == "modify":
        modify_cpu_name(last_action["from"])
    elif last_action["action"] == "restore":
        modify_cpu_name(last_action["from"])
    history.pop()
    save_history()

if not is_admin():
    messagebox.showerror("权限错误", LANGUAGES[current_lang]["admin_error"])
    exit()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title(LANGUAGES[current_lang]["title"])
root.geometry("500x400")
root.resizable(False, False)

# 初始化 GUI 组件
title_label = ctk.CTkLabel(root, text=LANGUAGES[current_lang]["title"], font=("Arial", 16, "bold"))
title_label.pack(pady=10)

current_cpu_label = ctk.CTkLabel(root, text=f"{LANGUAGES[current_lang]['current_cpu_label']} {get_current_cpu_name()}", font=("Arial", 12))
current_cpu_label.pack(pady=5)

input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=10)
label = ctk.CTkLabel(input_frame, text=LANGUAGES[current_lang]["input_label"], font=("Arial", 12))
label.grid(row=0, column=0, padx=5, pady=5)
entry = ctk.CTkEntry(input_frame, width=200)
entry.grid(row=0, column=1, padx=5, pady=5)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)
modify_button = ctk.CTkButton(button_frame, text=LANGUAGES[current_lang]["modify_button"], command=lambda: modify_cpu_name(entry.get()))
modify_button.grid(row=0, column=0, padx=10)
restore_button = ctk.CTkButton(button_frame, text=LANGUAGES[current_lang]["restore_button"], command=restore_cpu_name)
restore_button.grid(row=0, column=1, padx=10)
undo_button = ctk.CTkButton(button_frame, text=LANGUAGES[current_lang]["undo_button"], command=undo_last_action)
undo_button.grid(row=0, column=2, padx=10)

history_button = ctk.CTkButton(root, text=LANGUAGES[current_lang]["history_button"], command=show_history)
history_button.pack(pady=5)

system_info_label = ctk.CTkLabel(root, text=LANGUAGES[current_lang]["system_info_label"], font=("Arial", 12))
system_info_label.pack(pady=5)

switch_button = ctk.CTkButton(root, text=LANGUAGES[current_lang]["switch_button"], command=switch_language)
switch_button.pack(pady=5)
theme_button = ctk.CTkButton(root, text=LANGUAGES[current_lang]["theme_button"], command=switch_theme)
theme_button.pack(pady=5)

# 在 GUI 初始化后调用 get_original_cpu_name()
get_original_cpu_name()
load_history()

root.mainloop()