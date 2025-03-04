import tkinter as tk
from tkinter import ttk, messagebox
import winreg

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
        "success": "成功",
        "modify_success": "CPU 名称已修改为: {}",
        "restore_success": "CPU 名称已恢复为: {}",
        "error": "错误",
        "modify_error": "修改注册表时出错: {}",
        "restore_error": "恢复注册表时出错: {}"
    },
    "en": {
        "title": "Modify CPU Name Tool",
        "input_label": "Enter new CPU name:",
        "modify_button": "Modify Name",
        "restore_button": "Restore Original Name",
        "switch_button": "Switch Language / 切换语言",
        "success": "Success",
        "modify_success": "CPU name changed to: {}",
        "restore_success": "CPU name restored to: {}",
        "error": "Error",
        "modify_error": "Error modifying registry: {}",
        "restore_error": "Error restoring registry: {}"
    }
}

current_lang = "zh"  # 默认语言为中文

def modify_cpu_name(new_name):
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
        original_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, new_name)
        winreg.CloseKey(reg_key)
        messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["modify_success"].format(new_name))
    except Exception as e:
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["modify_error"].format(e))

def restore_cpu_name():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
        original_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, original_name)
        winreg.CloseKey(reg_key)
        messagebox.showinfo(LANGUAGES[current_lang]["success"], LANGUAGES[current_lang]["restore_success"].format(original_name))
    except Exception as e:
        messagebox.showerror(LANGUAGES[current_lang]["error"], LANGUAGES[current_lang]["restore_error"].format(e))

def switch_language():
    global current_lang
    current_lang = "en" if current_lang == "zh" else "zh"
    update_ui()

def update_ui():
    root.title(LANGUAGES[current_lang]["title"])
    title_label.config(text=LANGUAGES[current_lang]["title"])
    label.config(text=LANGUAGES[current_lang]["input_label"])
    modify_button.config(text=LANGUAGES[current_lang]["modify_button"])
    restore_button.config(text=LANGUAGES[current_lang]["restore_button"])
    switch_button.config(text=LANGUAGES[current_lang]["switch_button"])

# 创建主窗口
root = tk.Tk()
root.title(LANGUAGES[current_lang]["title"])
root.geometry("400x250")
root.resizable(False, False)

# 设置字体
font_title = ("Arial", 14, "bold")
font_label = ("Arial", 12)
font_button = ("Arial", 10, "bold")

# 添加标题
title_label = ttk.Label(root, text=LANGUAGES[current_lang]["title"], font=font_title, foreground="#333")
title_label.pack(pady=10)

# 添加输入框和标签
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)
label = ttk.Label(input_frame, text=LANGUAGES[current_lang]["input_label"], font=font_label)
label.grid(row=0, column=0, padx=5, pady=5)
entry = ttk.Entry(input_frame, width=30, font=font_label)
entry.grid(row=0, column=1, padx=5, pady=5)

# 添加按钮
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)
modify_button = ttk.Button(button_frame, text=LANGUAGES[current_lang]["modify_button"], command=lambda: modify_cpu_name(entry.get()))
modify_button.grid(row=0, column=0, padx=10)
restore_button = ttk.Button(button_frame, text=LANGUAGES[current_lang]["restore_button"], command=restore_cpu_name)
restore_button.grid(row=0, column=1, padx=10)

# 添加语言切换按钮
switch_button = ttk.Button(root, text=LANGUAGES[current_lang]["switch_button"], command=switch_language)
switch_button.pack(pady=10)

# 运行主循环
root.mainloop()
