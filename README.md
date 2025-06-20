# ScriptRepacker GUI

一个为 `ScriptRepacker.exe` 命令行工具提供图形化操作界面的高效前端应用。本程序通过现代化的GUI，简化了对 `.ss` 及 `.ss.txt` 文件对的批量处理流程。

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ 功能特性 (Features)

* **直观的用户界面**: 提供简洁明了的图形界面，所有操作一目了然。
* **灵活的输入方式**: 支持通过文件对话框选择源文件夹，或直接从文件管理器拖拽文件夹以设定路径。
* **批处理核心**: 自动检索并处理指定文件夹内所有匹配的 `*.ss` 及 `*.ss.txt` 文件对。
* **自动化工作流**: 自动创建独立的输出目录 (`_output`) 并归类处理结果，保持项目结构清晰。
* **幂等性操作**: 支持对同一批文件重复运行。程序会自动覆盖已存在的旧输出文件，确保结果始终为最新。
* **实时处理日志**: 在界面内提供详细的处理日志，方便追踪当前进度、确认操作结果或排查潜在问题。
* **多线程处理**: GUI主线程与文件处理工作线程分离，确保在处理大量文件时界面依然流畅响应，不会卡死。
* **错误重试机制**: 内置简单的失败重试逻辑，以应对因文件占用等原因导致的瞬时处理失败。

## 📖 使用说明 (for End-Users)

如果您下载的是已经打包好的 `ScriptRepackerGUI.exe` 程序，请按以下步骤使用：

1.  下载最新的 Release 版本（通常是一个 `.zip` 压缩包）。
2.  解压 `.zip` 文件。
3.  **【重要】** 将 `ScriptRepacker.exe` 程序复制到与 `ScriptRepackerGUI.exe` **相同的文件夹**中。
4.  在同一目录下，创建一个名为 `input` 的文件夹，并将所有待处理的 `.ss` 和 `.ss.txt` 文件放入其中。
5.  双击运行 `ScriptRepackerGUI.exe`。
6.  在程序界面中，通过点击按钮或拖拽的方式，选择您刚刚创建的 `input` 文件夹。
7.  点击“开始处理”按钮。
8.  处理完成后，程序会在 `input` 文件夹旁边自动创建一个 `..._output` 文件夹，所有处理好的文件都存放在里面。

## 🛠️ 从源码构建 (Building from Source)

如果您希望从源代码自行运行或打包本程序，请遵循以下步骤。

### 环境要求
* Python 3.9 或更高版本
* `ScriptRepacker.exe` (本仓库不包含此文件，需由用户自行准备)

### 操作步骤

1.  **克隆或下载仓库**
    ```bash
    git clone [https://github.com/Ywocp/ScriptRepackerGUI.git](https://github.com/Ywocp/ScriptRepackerGUI.git)
    cd ScriptRepacker-GUI
    ```

2.  **准备核心程序**
    将您自己的 `ScriptRepacker.exe` 程序文件复制到项目根目录下。

3.  **安装依赖库**
    本程序依赖 PySide6。在终端中运行以下命令进行安装：
    ```bash
    pip install pyside6
    ```

4.  **直接运行**
    通过以下命令直接从源码启动程序：
    ```bash
    python gui_app.py
    ```

### 📦 打包为独立的 .exe 文件

本项目使用 PyInstaller 进行打包。

1.  **安装 PyInstaller**:
    ```bash
    pip install pyinstaller
    ```

2.  **执行打包命令**:
    为了在不使用 UPX 的前提下优化体积，我们推荐使用以下包含模块排除的命令：
    ```bash
    pyinstaller --onefile --windowed --add-data "ScriptRepacker.exe;." -n "ScriptRepackerGUI" --exclude-module "PySide6.QtNetwork" --exclude-module "PySide6.QtWebEngineCore" --exclude-module "PySide6.QtMultimedia" --exclude-module "PySide6.QtSql" --exclude-module "PySide6.QtTest" gui_app.py
    ```

    **打包命令参数解析**:
| 参数 | 说明 |
| :--- | :--- |
| `--onefile` | 将所有依赖打包成一个独立的 `.exe` 文件。 |
| `--windowed` | 用于GUI程序，运行时不显示黑色的命令行控制台窗口。 |
| `--add-data "A;B"`| 将外部文件或文件夹打包进来。此处 `A` 是源文件(`ScriptRepacker.exe`)，`B` 是打包后在程序内的相对路径 (`.` 代表根目录)。 |
| `-n "AppName"` | 指定生成的 `.exe` 文件的名称。 |
| `--exclude-module`| 排除不需要的模块，以减小最终体积。 |


3.  **获取成果**:
    打包成功后，您最终的 `ScriptRepackerGUI.exe` 文件会出现在新生成的 `dist` 文件夹中。

## 🤝 贡献

欢迎通过提交 Issues 或 Pull Requests 来为此项目做出贡献。

## 📄 许可证

本项目采用 [MIT](https://opensource.org/licenses/MIT) 许可证。
