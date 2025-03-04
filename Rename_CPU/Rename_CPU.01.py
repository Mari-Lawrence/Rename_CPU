import tkinter as tk
from tkinter import messagebox
import winreg

# 定义注册表路径和键值
CPU_REGISTRY_PATH = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
VALUE_NAME = "ProcessorNameString"


# 修改 CPU 名称的函数
def modify_cpu_name(new_name):
    try:
        # 打开注册表项
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)

        # 获取原始名称（用于恢复）
        original_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)

        # 修改键值
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, new_name)

        # 关闭注册表项
        winreg.CloseKey(reg_key)

        # 提示成功
        messagebox.showinfo("成功", f"CPU 名称已修改为: {new_name}")

    except Exception as e:
        messagebox.showerror("错误", f"修改注册表时出错: {e}")


# 恢复原始 CPU 名称的函数
def restore_cpu_name():
    try:
        # 打开注册表项
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)

        # 获取原始名称
        original_name, _ = winreg.QueryValueEx(reg_key, VALUE_NAME)

        # 恢复原始名称
        winreg.SetValueEx(reg_key, VALUE_NAME, 0, winreg.REG_SZ, original_name)

        # 关闭注册表项
        winreg.CloseKey(reg_key)

        # 提示成功
        messagebox.showinfo("成功", f"CPU 名称已恢复为: {original_name}")

    except Exception as e:
        messagebox.showerror("错误", f"恢复注册表时出错: {e}")


# 创建图形化界面
def create_gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("修改 CPU 名称")
    root.geometry("300x150")

    # 添加标签
    label = tk.Label(root, text="输入新的 CPU 名称:")
    label.pack(pady=10)

    # 添加输入框
    entry = tk.Entry(root, width=30)
    entry.pack(pady=10)

    # 添加修改按钮
    modify_button = tk.Button(root, text="修改名称", command=lambda: modify_cpu_name(entry.get()))
    modify_button.pack(pady=5)

    # 添加恢复按钮
    restore_button = tk.Button(root, text="恢复原始名称", command=restore_cpu_name)
    restore_button.pack(pady=5)

    # 运行主循环
    root.mainloop()


# 启动 GUI
if __name__ == "__main__":
    create_gui()