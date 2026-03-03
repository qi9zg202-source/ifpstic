import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFileDialog, QTextEdit, QFrame,
                           QTableWidget, QTableWidgetItem, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ExcelAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Excel数据分析器')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置边距
        
        # 创建标题标签
        title_label = QLabel('Excel数据分析结果')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # 添加分割线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        # 创建垂直分割器
        splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(splitter)
        
        # 创建上部分容器（统计信息区域）
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建统计信息显示区域
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('Courier New', 12))
        top_layout.addWidget(self.result_text)
        
        # 创建下部分容器（表格区域）
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建表格标题
        table_title = QLabel('Excel数据表格')
        table_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        bottom_layout.addWidget(table_title)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setFont(QFont('Arial', 10))
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        bottom_layout.addWidget(self.table)
        
        # 将上下部分添加到分割器
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        
        # 设置分割器的初始比例
        splitter.setSizes([300, 500])  # 设置初始高度比例
        splitter.setHandleWidth(8)  # 设置分隔条的宽度
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #ccc;
                border: 1px solid #999;
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background-color: #999;
            }
        """)  # 设置分隔条的样式
        
        # 创建按钮面板
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        # 创建选择文件按钮
        select_button = QPushButton('选择Excel文件')
        select_button.setMinimumWidth(120)
        select_button.setFont(QFont('Arial', 11))
        select_button.clicked.connect(self.analyze_excel)
        button_layout.addWidget(select_button)
        
        main_layout.addWidget(button_panel)
        
    def update_table(self, df):
        # 设置表格的行数和列数
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        
        # 设置表头
        self.table.setHorizontalHeaderLabels(df.columns)
        
        # 设置表头样式
        header = self.table.horizontalHeader()
        header.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        
        # 填充数据
        for i in range(len(df)):
            for j in range(len(df.columns)):
                value = str(df.iloc[i, j])
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 设置单元格为只读
                self.table.setItem(i, j, item)
        
        # 调整列宽以适应内容
        self.table.resizeColumnsToContents()
        
        # 设置表格样式
        self.table.setAlternatingRowColors(True)  # 设置交替行颜色
        self.table.setShowGrid(True)  # 显示网格线
        
    def analyze_excel(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(self, '选择Excel文件', '', 'Excel files (*.xlsx *.xls)')
        
        if file_path:
            try:
                # 读取Excel文件
                df = pd.read_excel(file_path)
                
                # 更新表格显示
                self.update_table(df)
                
                # 获取基本信息
                total_rows = len(df)
                total_cols = len(df.columns)
                first_column = df.columns[0]
                
                # 区分一期和二期指标
                p2_records = df[df[first_column].str.contains('_P2', na=False)]
                p1_records = df[~df[first_column].str.contains('_P2', na=False)]
                
                # 检查一期指标重复数据
                p1_duplicates = p1_records[p1_records[first_column].duplicated(keep=False)]
                
                # 检查二期指标重复数据
                p2_duplicates = p2_records[p2_records[first_column].duplicated(keep=False)]
                
                # 检查包含&的记录
                ampersand_records = df[df[first_column].str.contains('&', na=False)]
                
                # 生成报告
                report = f"""
数据基本信息
{'='*50}
• 总行数: {total_rows}
• 总列数: {total_cols}

一期指标统计 (不含_P2)
{'='*50}
• 一期指标总行数: {len(p1_records)}
• 一期指标重复记录数: {len(p1_duplicates)}

二期指标统计 (包含_P2)
{'='*50}
• 二期指标总行数: {len(p2_records)}
• 二期指标重复记录数: {len(p2_duplicates)}

特殊字符统计
{'='*50}
• 包含'&'的记录数: {len(ampersand_records)}

详细信息
{'='*50}"""

                # 如果有一期指标重复记录，显示详细信息
                if len(p1_duplicates) > 0:
                    report += "\n\n一期指标重复记录详情:"
                    duplicate_groups = p1_duplicates.groupby(first_column)
                    for value, group in duplicate_groups:
                        report += f"\n\n值: '{value}'"
                        report += f"\n出现次数: {len(group)}"
                        report += "\n出现在以下行:"
                        for index in group.index:
                            report += f"\n- 第 {index + 1} 行"
                    report += "\n" + "-"*30

                # 如果有二期指标重复记录，显示详细信息
                if len(p2_duplicates) > 0:
                    report += "\n\n二期指标重复记录详情:"
                    duplicate_groups = p2_duplicates.groupby(first_column)
                    for value, group in duplicate_groups:
                        report += f"\n\n值: '{value}'"
                        report += f"\n出现次数: {len(group)}"
                        report += "\n出现在以下行:"
                        for index in group.index:
                            report += f"\n- 第 {index + 1} 行"
                    report += "\n" + "-"*30

                # 如果有包含&的记录，显示详细信息
                if len(ampersand_records) > 0:
                    report += "\n\n包含'&'的记录详情:"
                    for index, row in ampersand_records.iterrows():
                        report += f"\n- 第 {index + 1} 行: {row[first_column]}"
                
                # 更新显示
                self.result_text.setText(report)
                
            except Exception as e:
                self.result_text.setText(f"错误: {str(e)}")

def main():
    app = QApplication(sys.argv)
    ex = ExcelAnalyzer()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 