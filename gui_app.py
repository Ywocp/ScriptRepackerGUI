import os
import sys
import shutil
import subprocess
import time
import threading

from PySide6.QtCore import Qt, Signal, QObject, QThread, QUrl
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QLineEdit, QLabel, QTextEdit, QFileDialog, QMessageBox)


# 为了在独立线程中安全地更新GUI，我们需要一个信号收发器
class WorkerSignals(QObject):
    log = Signal(str)
    finished = Signal()
    error = Signal(str)
    info_message = Signal(str, str)


class RepackerWorker(QObject):
    def __init__(self, input_dir, repacker_exe_path):
        super().__init__()
        self.signals = WorkerSignals()
        self.input_dir = input_dir
        self.repacker_exe_path = repacker_exe_path

    def run(self):
        try:
            output_dir = os.path.join(os.path.dirname(self.input_dir), f"{os.path.basename(self.input_dir)}_output")
            if not os.path.exists(output_dir):
                self.signals.log.emit(f"[INFO] 正在创建输出文件夹: {output_dir}")
                os.makedirs(output_dir)

            self.signals.log.emit("=" * 50)
            self.signals.log.emit("开始处理...")

            ss_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.ss')]
            if not ss_files:
                self.signals.log.emit("[INFO] 在源文件夹中未找到 .ss 文件。")

            for ss_filename in ss_files:
                ss_filepath = os.path.join(self.input_dir, ss_filename)
                txt_filename = ss_filename + ".txt"
                txt_filepath = os.path.join(self.input_dir, txt_filename)

                if os.path.exists(txt_filepath):
                    self.signals.log.emit("-" * 50)
                    self.signals.log.emit(f"[找到文件对]\n  - {ss_filename}\n  - {txt_filename}")

                    out_filename = ss_filename + ".out"
                    out_filepath = os.path.join(self.input_dir, out_filename)

                    is_success = False
                    retry_count = 0
                    while not is_success and retry_count < 5:
                        self.signals.log.emit("[*] 正在运行 ScriptRepacker.exe...")

                        subprocess.run([self.repacker_exe_path, ss_filepath, txt_filepath], check=False,
                                       creationflags=0x08000000)

                        # --- 已移除 ---: 不再需要人为等待1秒
                        # time.sleep(1)

                        if os.path.exists(out_filepath):
                            final_filepath = os.path.join(output_dir, ss_filename)
                            self.signals.log.emit(f"[*] 正在移动并重命名文件至: {final_filepath}")
                            shutil.move(out_filepath, final_filepath)
                            self.signals.log.emit(f"[SUCCESS] 最终文件已生成: {final_filepath}")
                            is_success = True
                        else:
                            retry_count += 1
                            self.signals.log.emit(f"[FAILURE] 未找到输出文件，3秒后重试 (第{retry_count}次)...")
                            time.sleep(3)

                    if not is_success:
                        self.signals.log.emit(f"[FATAL ERROR] 重试多次后依然无法处理文件: {ss_filename}")
                else:
                    self.signals.log.emit(f"[WARNING] 文件 {ss_filename} 缺少对应的 .txt 文件，已跳过。")

            self.signals.log.emit("=" * 50)
            self.signals.log.emit("[完成] 所有找到的文件对都已处理完毕。")
            self.signals.info_message.emit("完成", "所有任务已处理完毕！")

        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Script Repacker GUI (v11 - Fast)")
        self.resize(700, 500)
        self.setAcceptDrops(True)

        self.repacker_exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ScriptRepacker.exe")
        self.thread = None
        self.worker = None

        self.layout = QVBoxLayout(self)
        self.label_info = QLabel("请选择或拖拽包含.ss和.txt的源文件夹到此窗口")
        self.input_path_edit = QLineEdit()
        self.select_folder_button = QPushButton("点击选择文件夹")
        self.start_button = QPushButton("开始处理")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        self.layout.addWidget(self.label_info)
        self.layout.addWidget(self.input_path_edit)
        self.layout.addWidget(self.select_folder_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(QLabel("处理日志:"))
        self.layout.addWidget(self.log_area)

        self.select_folder_button.clicked.connect(self.select_folder)
        self.start_button.clicked.connect(self.start_processing)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if folder:
            self.input_path_edit.setText(folder.replace('/', os.sep))
            self.log_message(f"已选择源文件夹: {folder}")

    def log_message(self, message):
        self.log_area.append(message)

    def start_processing(self):
        input_dir = self.input_path_edit.text()
        if not input_dir or not os.path.isdir(input_dir):
            QMessageBox.critical(self, "错误", "请先选择一个有效的源文件夹！")
            return

        if not os.path.exists(self.repacker_exe_path):
            QMessageBox.critical(self, "错误", f"未在程序目录找到 ScriptRepacker.exe！\n请确保它和本程序在同一文件夹。")
            return

        self.start_button.setEnabled(False)
        self.log_area.clear()

        self.thread = QThread()
        self.worker = RepackerWorker(input_dir, self.repacker_exe_path)
        self.worker.moveToThread(self.thread)

        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.finished.connect(self.on_processing_finished)
        self.worker.signals.error.connect(self.on_processing_error)
        self.worker.signals.info_message.connect(lambda title, msg: QMessageBox.information(self, title, msg))

        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_processing_finished(self):
        self.start_button.setEnabled(True)
        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()
            self.worker.deleteLater()
            self.thread.deleteLater()
            self.thread = None
            self.worker = None

    def on_processing_error(self, error_msg):
        QMessageBox.critical(self, "严重错误", f"处理过程中发生错误:\n{error_msg}")
        self.on_processing_finished()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            if hasattr(urls[0], 'toLocalFile'):
                path = urls[0].toLocalFile()
            else:
                path = str(urls[0])

            if os.path.isdir(path):
                self.input_path_edit.setText(path)
                self.log_message(f"已通过拖拽选择源文件夹: {path}")
            else:
                self.log_message(f"[WARNING] 您拖入的不是一个文件夹，请重新拖入。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())