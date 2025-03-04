import tkinter as tk
from tkinter import ttk, messagebox
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
    root.geometry("400x200")
    root.resizable(False, False)  # 禁止调整窗口大小

    # 设置主题样式
    style = ttk.Style()
    style.theme_use("clam")  # 使用现代化的主题

    # 设置字体
    font_title = ("Arial", 14, "bold")
    font_label = ("Arial", 12)
    font_button = ("Arial", 10, "bold")

    # 添加标题
    title_label = ttk.Label(root, text="修改 CPU 名称工具", font=font_title, foreground="#333")
    title_label.pack(pady=10)

    # 添加输入框和标签
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10)

    label = ttk.Label(input_frame, text="输入新的 CPU 名称:", font=font_label)
    label.grid(row=0, column=0, padx=5, pady=5)

    entry = ttk.Entry(input_frame, width=30, font=font_label)
    entry.grid(row=0, column=1, padx=5, pady=5)

    # 添加按钮
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    modify_button = ttk.Button(
        button_frame,
        text="修改名称",
        command=lambda: modify_cpu_name(entry.get()),
        style="Accent.TButton"
    )
    modify_button.grid(row=0, column=0, padx=10)

    restore_button = ttk.Button(
        button_frame,
        text="恢复原始名称",
        command=restore_cpu_name,
        style="Accent.TButton"
    )
    restore_button.grid(row=0, column=1, padx=10)

    # 自定义按钮样式
    style.configure("Accent.TButton", font=font_button, foreground="white", background="#0078D7", padding=10)
    style.map("Accent.TButton", background=[("active", "#005BB5")])

    # 运行主循环
    root.mainloop()


# 启动 GUI
if __name__ == "__main__":
    create_gui()