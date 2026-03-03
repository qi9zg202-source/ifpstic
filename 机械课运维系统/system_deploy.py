#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QTextEdit,
                             QLabel, QFrame, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import subprocess
import datetime

class DeployThread(QThread):
    """部署执行线程"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        
    def run(self):
        try:
            self.output_signal.emit("=== 命令执行开始 ===")
            self.output_signal.emit(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.output_signal.emit(f"执行命令: {self.command}")
            self.output_signal.emit("")
            
            if not self.command.strip():
                self.output_signal.emit("❌ 命令不能为空")
                self.finished_signal.emit(False)
                return
            
            # 执行命令
            process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # 实时输出命令结果
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip())
            
            # 获取返回码
            return_code = process.poll()
            
            self.output_signal.emit("")
            if return_code == 0:
                self.output_signal.emit("=== 命令执行完成 ===")
                self.finished_signal.emit(True)
            else:
                self.output_signal.emit(f"❌ 命令执行失败 (返回码: {return_code})")
                self.finished_signal.emit(False)
            
        except Exception as e:
            self.output_signal.emit(f"❌ 执行失败: {str(e)}")
            self.finished_signal.emit(False)

class SystemDeployWindow(QMainWindow):
    """系统发布主窗口"""
    
    def __init__(self):
        super().__init__()
        self.deploy_thread = None
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("系统发布工具")
        self.setGeometry(300, 300, 800, 600)
        
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel("系统发布管理")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("QLabel { color: #2c3e50; margin: 10px; }")
        main_layout.addWidget(title_label)
        
        # 分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 密码输入框
        pwd_label = QLabel("pwd:")
        pwd_label.setFont(QFont("Arial", 10, QFont.Bold))
        main_layout.addWidget(pwd_label)
        
        self.pwd_input = QLineEdit()
        self.pwd_input.setFont(QFont("Consolas", 10))
        self.pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.pwd_input.setText("Sesa627852")
        self.pwd_input.setPlaceholderText("请输入SSH密码")
        self.pwd_input.mousePressEvent = self.copy_pwd_to_clipboard
        main_layout.addWidget(self.pwd_input)
        
        # 命令输入框
        command_label = QLabel("命令:")
        command_label.setFont(QFont("Arial", 10, QFont.Bold))
        main_layout.addWidget(command_label)
        
        self.command_input = QLineEdit()
        self.command_input.setFont(QFont("Consolas", 10))
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.command_input.setText("scp -r /Users/beckliu/Documents/IFPALLINONE/* root@112.74.32.33:/usr/share/nginx/html/pxifpstic/")
        self.command_input.setPlaceholderText("scp -r /Users/beckliu/Documents/IFPALLINONE/* root@112.74.32.33:/usr/share/nginx/html/pxifpstic/")
        self.command_input.mousePressEvent = self.copy_command_to_clipboard
        main_layout.addWidget(self.command_input)
        
        # 命令输出框
        output_label = QLabel("命令输出:")
        output_label.setFont(QFont("Arial", 10, QFont.Bold))
        main_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.output_text.setPlaceholderText("命令执行输出将显示在这里...")
        self.output_text.mousePressEvent = self.copy_output_to_clipboard
        main_layout.addWidget(self.output_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 清空输出按钮
        self.clear_button = QPushButton("清空输出")
        self.clear_button.setFont(QFont("Arial", 10))
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_button)
        
        # 弹簧，推按钮到右边
        button_layout.addStretch()
        
        # 执行按钮
        self.deploy_button = QPushButton("开始发布")
        self.deploy_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.deploy_button.setFixedHeight(45)
        self.deploy_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.deploy_button.clicked.connect(self.start_deploy)
        button_layout.addWidget(self.deploy_button)
        
        main_layout.addLayout(button_layout)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
    def clear_output(self):
        """清空输出框"""
        self.output_text.clear()
        self.statusBar().showMessage("输出已清空")
        
    def start_deploy(self):
        """开始发布"""
        if self.deploy_thread and self.deploy_thread.isRunning():
            return
        
        # 获取命令输入框中的命令
        command = self.command_input.text().strip()
        if not command:
            self.statusBar().showMessage("请输入要执行的命令")
            return
            
        self.deploy_button.setEnabled(False)
        self.deploy_button.setText("执行中...")
        self.clear_button.setEnabled(False)
        self.command_input.setEnabled(False)
        self.statusBar().showMessage("正在执行命令...")
        
        # 创建并启动执行线程
        self.deploy_thread = DeployThread(command)
        self.deploy_thread.output_signal.connect(self.append_output)
        self.deploy_thread.finished_signal.connect(self.deploy_finished)
        self.deploy_thread.start()
        
    def append_output(self, text):
        """追加输出文本"""
        self.output_text.append(text)
        # 自动滚动到底部
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)
        
    def deploy_finished(self, success):
        """命令执行完成"""
        self.deploy_button.setEnabled(True)
        self.deploy_button.setText("开始发布")
        self.clear_button.setEnabled(True)
        self.command_input.setEnabled(True)
        
        if success:
            self.statusBar().showMessage("命令执行完成")
        else:
            self.statusBar().showMessage("命令执行失败")
            
    def copy_output_to_clipboard(self, event):
        """点击输出框时复制所有输出内容到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        self.statusBar().showMessage("输出内容已复制到剪贴板")
        
    def copy_command_to_clipboard(self, event):
        """点击命令输入框时复制命令内容到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.command_input.text())
        self.statusBar().showMessage("命令已复制到剪贴板")
        
    def copy_pwd_to_clipboard(self, event):
        """点击密码输入框时复制密码内容到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.pwd_input.text())
        self.statusBar().showMessage("密码已复制到剪贴板")
            
def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建主窗口
    window = SystemDeployWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()