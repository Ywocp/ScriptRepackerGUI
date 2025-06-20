# ScriptRepacker GUI

一个为  [xmoezzz/ScriptRepacker](https://github.com/xmoeproject/SiglusExtract/blob/master/tools/ScriptRepacker.exe)  提供图形化操作界面的前端。本程序通过现代化的GUI，简化了对 `.ss` 及 `.ss.txt` 文件对的批量处理流程。

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ 功能特性 (Features)

* **直观的用户界面**: 提供简洁明了的图形界面，所有操作一目了然。
* **灵活的输入方式**: 支持通过文件对话框选择源文件夹，或直接从文件管理器拖拽文件夹以设定路径。
* **批处理核心**: 自动检索并处理指定文件夹内所有匹配的 `*.ss` 及 `*.ss.txt` 文件对。
* **自动化工作流**: 自动创建独立的输出目录 (`_output`) 并归类处理结果，保持项目结构清晰。
* **覆盖操作**: 支持对同一批文件重复运行，可自动覆盖已存在的输出文件，确保结果始终为最新。
* **实时处理日志**: 在界面内提供详细的处理日志，方便追踪进度和排查问题。
* **多线程处理**: GUI主线程与文件处理工作线程分离，确保在处理大量文件时界面依然流畅响应，不会卡死。
* **错误重试机制**: 内置简单的失败重试逻辑，以应对因文件占用等原因导致的瞬时处理失败。

## 📖 使用说明 (for End-Users)

1.  从本项目的 [Releases 页面](https://github.com/Ywocp/ScriptRepackerGUI/releases)下载最新的 `ScriptRepackerGUI.exe` 程序文件。

2.  将所有需要处理的 `.ss` 和 `.ss.txt` 文件整理到一个文件夹中（此文件夹可任意命名，例如 `MySourceFiles`）。

3.  为方便管理，建议将下载的 `ScriptRepackerGUI.exe` 和第2步中准备的源文件夹（例如 `MySourceFiles`）放在同一个目录下，比如都放在桌面上（随便放也行，不影响文件处理）。

4.  双击运行 `ScriptRepackerGUI.exe`。

5.  在程序主窗口，通过以下任一方式指定源文件夹：
    * **点击按钮**：点击“点击选择文件夹”按钮，在弹出的窗口中选择在第2步中准备的文件夹。
    * **拖拽操作**：直接将第2步中准备的文件夹从文件管理器中拖拽到程序窗口的任意位置。

6.  确认路径无误后，点击“开始处理”按钮。

7.  处理完成后，在源文件夹旁边会自动生成一个带有 `_output` 后缀的新文件夹（例如，如果源文件夹是 `MySourceFiles`，则输出文件夹为 `MySourceFiles_output`），所有处理好的最终文件都存放在里面。

## 🛠️ 从源码构建 (Building from Source)

本章节面向希望自行修改代码、运行或打包程序的用户。

### 环境要求

* Python 3.9 或更高版本。
* 本项目的核心依赖工具 `ScriptRepacker.exe` 已包含在仓库中，克隆或下载源码后即可使用。

### 操作步骤

1.  **克隆或下载仓库**
    ```bash
    git clone [https://github.com/Ywocp/ScriptRepackerGUI.git](https://github.com/Ywocp/ScriptRepackerGUI.git)
    cd ScriptRepacker-GUI
    ```

2.  **安装依赖库**
    本程序依赖 PySide6。在终端中运行以下命令进行安装：
    ```bash
    pip install pyside6
    ```

3.  **直接运行**
    通过以下命令直接从源码启动程序：
    ```bash
    python gui_app.py
    ```

### 📦 打包为独立的 .exe 文件

1.  **安装 PyInstaller**:
    ```bash
    pip install pyinstaller
    ```

2.  **执行打包命令** :
    由于 `ScriptRepacker.exe` 已在项目文件夹中，`--add-data` 参数会自动找到它。
    ```bash
    pyinstaller --onefile --windowed --add-data "ScriptRepacker.exe;." -n "ScriptRepackerGUI" --exclude-module "PySide6.QtNetwork" --exclude-module "PySide6.QtWebEngineCore" --exclude-module "PySide6.QtMultimedia" --exclude-module "PySide6.QtSql" --exclude-module "PySide6.QtTest" gui_app.py
    ```

3.  **获取成果**:
    打包成功后，最终的 `ScriptRepackerGUI.exe` 文件会出现在新生成的 `dist` 文件夹中。

## 🙏 致谢 (Acknowledgements)

本项目的核心处理功能由 [xmoeproject/SiglusExtract](https://github.com/xmoeproject/SiglusExtract) 项目提供的 `ScriptRepacker.exe` 工具实现。在此向原作者表示诚挚的感谢。

## 📄 许可证

本项目采用 [MIT](https://opensource.org/licenses/MIT) 许可证。
