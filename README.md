# CPU 名称修改工具

这是一个基于 Python 和 CustomTkinter 的桌面应用程序，允许用户修改 Windows 系统注册表中的 CPU 名称，并提供备份、恢复、历史记录等功能。该工具支持中英文界面，适用于需要自定义 CPU 显示名称的用户。

## 功能

- **修改 CPU 名称**：通过输入新的 CPU 名称修改注册表中的 `ProcessorNameString`。
- **恢复原始名称**：将 CPU 名称恢复为原始值。
- **备份与恢复**：每次修改时自动创建备份，并支持从备份文件恢复。
- **历史记录**：记录每次修改或恢复的操作，支持查看和撤销。
- **多语言支持**：支持中文和英文界面切换。
- **主题切换**：支持浅色和深色主题切换。
- **日志记录**：所有操作都会记录到日志文件 `cpu_name_editor.log`。

## 使用说明

1. 以管理员身份运行程序。
2. 在输入框中输入新的 CPU 名称。
3. 点击“修改名称”按钮更改 CPU 名称，或点击“恢复原始名称”恢复默认值。
4. 使用“撤销”按钮撤销上一次操作。
5. 点击“查看历史记录”查看所有操作记录。
6. 通过“切换语言”和“切换主题”按钮调整界面。

**注意**：修改完成后可能需要重启系统以应用更改。

## 安装步骤

1. **环境要求**：
   - Windows操作系统
   - Python 3.7 或更高版本

2. **安装依赖**：
   在项目根目录下运行以下命令：
   ```bash
   pip install customtkinter

运行程序：
将代码保存为 .py 文件（例如 cpu_name_editor.py）。

以管理员权限运行：
bash

python cpu_name_editor.py

注意事项
权限要求：必须以管理员身份运行，否则无法修改注册表。

输入限制：新 CPU 名称仅支持字母、数字、空格、括号和短横线。

备份文件：备份数据存储在 cpu_name_backup.json，历史记录存储在 cpu_name_history.json。

日志文件：操作日志保存在 cpu_name_editor.log 中，便于调试和记录。

许可证
此项目采用 MIT 许可证，详情请见 LICENSE 文件。
贡献
欢迎提交问题和拉取请求！如果您有改进建议，请通过 GitHub Issues 联系我。

# CPU Name Modifier Tool

This is a desktop application built with Python and CustomTkinter that allows users to modify the CPU name in the Windows registry. It provides features like backup, restore, and history tracking. The tool supports both Chinese and English interfaces, making it ideal for users who want to customize their CPU display name.

## Features

- **Modify CPU Name**: Change the `ProcessorNameString` in the registry by entering a new CPU name.
- **Restore Original Name**: Revert the CPU name to its original value.
- **Backup and Restore**: Automatically create backups with each modification and restore from backup files.
- **History Tracking**: Record all modification and restoration actions with the ability to view and undo them.
- **Multi-Language Support**: Switch between Chinese and English interfaces.
- **Theme Switching**: Toggle between light and dark themes.
- **Logging**: All operations are logged to the `cpu_name_editor.log` file.

## Usage

1. Run the program with administrator privileges.
2. Enter a new CPU name in the input field.
3. Click the "Modify Name" button to change the CPU name, or "Restore Original Name" to revert to the default.
4. Use the "Undo" button to revert the last action.
5. Click "View History" to see all recorded operations.
6. Adjust the interface with the "Switch Language" and "Switch Theme" buttons.

**Note**: A system restart may be required for changes to take effect.

## Installation

1. **Requirements**:
   - Windows operating system
   - Python 3.7 or higher

2. **Install Dependencies**:
   Run the following command in the project directory:
   ```bash
   pip install customtkinter

Run the Program:
Save the code as a .py file (e.g., cpu_name_editor.py).

Run with administrator privileges:
bash

python cpu_name_editor.py

Notes
Permission: Must be run as an administrator to modify the registry.

Input Restrictions: The new CPU name can only contain letters, numbers, spaces, brackets, and dashes.

Backup Files: Backup data is stored in cpu_name_backup.json, and history is saved in cpu_name_history.json.

Log File: Operation logs are saved in cpu_name_editor.log for debugging and tracking.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Feel free to submit issues or pull requests! If you have suggestions for improvement, please reach out via GitHub Issues.

# CPU 名変更ツール

これは Python と CustomTkinter を使用して構築されたデスクトップアプリケーションで、Windows レジストリ内の CPU 名を変更することができます。バックアップ、復元、履歴追跡などの機能を提供し、中国語と英語のインターフェースをサポートしています。CPU の表示名をカスタマイズしたいユーザー向けに設計されています。

## 機能

- **CPU 名の変更**：新しい CPU 名を入力して、レジストリの `ProcessorNameString` を変更します。
- **元の名前の復元**：CPU 名を元の値に戻します。
- **バックアップと復元**：変更ごとに自動的にバックアップを作成し、バックアップファイルから復元できます。
- **履歴追跡**：すべての変更および復元操作を記録し、閲覧および取り消しが可能です。
- **多言語サポート**：中国語と英語のインターフェースを切り替えられます。
- **テーマ切り替え**：ライトテーマとダークテーマを切り替えられます。
- **ログ記録**：すべての操作が `cpu_name_editor.log` ファイルに記録されます。

## 使用方法

1. 管理者権限でプログラムを実行します。
2. 入力欄に新しい CPU 名を入力します。
3. 「名前を変更」ボタンをクリックして CPU 名を変更するか、「元の名前を復元」をクリックしてデフォルトに戻します。
4. 「取り消し」ボタンを使用して最後の操作を取り消します。
5. 「履歴を表示」をクリックしてすべての操作記録を確認します。
6. 「言語切り替え」と「テーマ切り替え」ボタンでインターフェースを調整します。

**注意**：変更を適用するにはシステムの再起動が必要な場合があります。

## インストール手順

1. **要件**：
   - Windows オペレーティングシステム
   - Python 3.7 以上

2. **依存関係のインストール**：
   プロジェクトディレクトリで以下のコマンドを実行します：
   ```bash
   pip install customtkinter

プログラムの実行：
コードを .py ファイルとして保存します（例：cpu_name_editor.py）。

管理者権限で実行します：
bash

python cpu_name_editor.py

注意事項
権限：レジストリを変更するには管理者として実行する必要があります。

入力制限：新しい CPU 名には文字、数字、スペース、括弧、ダッシュのみ使用可能です。

バックアップファイル：バックアップデータは cpu_name_backup.json に、履歴は cpu_name_history.json に保存されます。

ログファイル：操作ログは cpu_name_editor.log に保存され、デバッグや追跡に役立ちます。

ライセンス
このプロジェクトは MIT ライセンスの下で公開されています。詳細は LICENSE ファイルを参照してください。
貢献
問題の提出やプルリクエストを歓迎します！改善提案がある場合は、GitHub Issues を通じてご連絡ください。

