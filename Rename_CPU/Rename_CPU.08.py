import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import winreg
import ctypes
import re
import logging

# 配置日志记录
logging.basicConfig(filename="cpu_name_editor.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 定义注册表路径和键值
CPU_REGISTRY_PATH = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
VALUE_NAME = "ProcessorNameString"

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
        "dont_show_again": "不再提示"
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
        "dont_show_again": "Do not show again"
    }
}

current_lang = "zh"
original_cpu_name = ""
dont_show_restart_hint = False

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
    except Exception as e:
        messagebox.showerror(LANGUAGES[current_lang]["error"], f"无法获取原始 CPU 名称: {e}")

def validate_input(name):
    return bool(re.match(r"^[ A-Za-z0-9()-]+$", name))

def modify_cpu_name(new_name):
    global dont_show_restart_hint
    if not validate_input(new_name):
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["invalid_input"])
        return
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, new_name)
        winreg.CloseKey(reg_key)
        logging.info(f"CPU 名称修改为: {new_name}")
        messagebox.showinfo(LANGUAGES[current_lang]["success"],
                            LANGUAGES[current_lang]["modify_success"].format(new_name))

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
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, original_cpu_name)
        winreg.CloseKey(reg_key)
        logging.info("CPU 名称已恢复")
        messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["restore_success"].format(original_cpu_name))
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

if not is_admin():
    messagebox.showerror("权限错误", LANGUAGES[current_lang]["admin_error"])
    exit()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title(LANGUAGES[current_lang]["title"])
root.geometry("400x300")
root.resizable(False, False)

get_original_cpu_name()

title_label = ctk.CTkLabel(root, text=LANGUAGES[current_lang]["title"], font=("Arial", 16, "bold"))
title_label.pack(pady=10)

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

switch_button = ctk.CTkButton(root, text=LANGUAGES[current_lang]["switch_button"], command=switch_language)
switch_button.pack(pady=5)
theme_button = ctk.CTkButton(root, text=LANGUAGES[current_lang]["theme_button"], command=switch_theme)
theme_button.pack(pady=5)

root.mainloop()