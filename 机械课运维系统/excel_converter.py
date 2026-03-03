import pandas as pd
import os
import sqlite3
import json
from datetime import datetime

class ExcelConverter:
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.df = None

    def read_excel(self, file_path, sheet_name=0):
        """
        读取Excel文件
        :param file_path: Excel文件路径
        :param sheet_name: 工作表名称或索引，默认为第一个工作表
        :return: 成功返回True，失败返回False
        """
        try:
            self.input_path = file_path
            self.df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"成功读取文件: {file_path}")
            print(f"数据形状: {self.df.shape}")
            # 打印列名，用于调试
            print("列名:", self.df.columns.tolist())
            return True
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            return False

    def convert_data(self, columns_map=None, date_columns=None):
        """
        转换数据格式
        :param columns_map: 列名映射字典，例如 {'原列名': '新列名'}
        :param date_columns: 需要转换为日期格式的列名列表
        """
        if self.df is None:
            print("请先读取Excel文件")
            return False

        try:
            # 重命名列
            if columns_map:
                self.df = self.df.rename(columns=columns_map)

            # 转换日期格式
            if date_columns:
                for col in date_columns:
                    if col in self.df.columns:
                        self.df[col] = pd.to_datetime(self.df[col])
                        self.df[col] = self.df[col].dt.strftime('%Y-%m-%d')

            return True
        except Exception as e:
            print(f"数据转换失败: {str(e)}")
            return False

    def save_excel(self, output_path=None, sheet_name='Sheet1'):
        """
        保存转换后的数据到新的Excel文件
        :param output_path: 输出文件路径
        :param sheet_name: 工作表名称
        """
        if self.df is None:
            print("没有数据可保存")
            return False

        try:
            if output_path is None:
                # 生成默认输出文件名
                file_dir = os.path.dirname(self.input_path)
                file_name = os.path.splitext(os.path.basename(self.input_path))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(file_dir, f"{file_name}_converted_{timestamp}.xlsx")

            self.df.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"文件已保存: {output_path}")
            return True
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return False

    def clean_string(self, value):
        """
        清理字符串：去除空格，处理None值
        :param value: 输入值
        :return: 清理后的字符串
        """
        if pd.isna(value) or value is None:
            return ''
        return str(value).strip()

    def generate_formatted_string(self, record):
        """
        生成格式化的字符串
        :param record: 单条记录字典
        :return: 格式化后的字符串
        """
        try:
            # 从记录中提取所需字段并清理
            subsystem = self.clean_string(record.get('子系统', ''))
            first_menu = self.clean_string(record.get('一级菜单', ''))
            menu_path = self.clean_string(record.get('菜单整体路径', ''))
            description = self.clean_string(record.get('问题描述', ''))
            proposer = self.clean_string(record.get('提出人', ''))
            propose_time = self.clean_string(record.get('提出时间', ''))
            remark = self.clean_string(record.get('备注', ''))  # 添加备注字段

            # 生成格式化的字符串
            formatted_string = f"[{subsystem}]-[{first_menu}]-[{menu_path}]-[{description}]-[{proposer}]-[{propose_time}]-[{remark}]"
            return formatted_string
        except Exception as e:
            print(f"生成格式化字符串失败: {str(e)}")
            return None

    def save_to_excel(self, output_path=None):
        """
        保存数据到Excel文件，包括生成的字符串
        :param output_path: 输出文件路径
        :return: 成功返回True，失败返回False
        """
        try:
            if output_path is None:
                # 生成默认输出文件名
                file_dir = os.path.dirname(self.input_path)
                file_name = os.path.splitext(os.path.basename(self.input_path))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(file_dir, f"{file_name}_with_strings_{timestamp}.xlsx")

            # 保存到新的Excel文件
            self.df.to_excel(output_path, index=False)
            print(f"文件已保存: {output_path}")
            return True
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return False

    def convert_to_json(self):
        """
        将DataFrame转换为标准JSON格式并打印
        :return: 成功返回True，失败返回False
        """
        if self.df is None:
            print("没有数据可转换")
            return False

        try:
            # 过滤"机械科运维"的数据
            self.df = self.df[self.df.iloc[:, 0] == "机械科运维"]
            print(f"过滤后数据形状: {self.df.shape}")

            # 处理日期时间列
            for column in self.df.columns:
                if pd.api.types.is_datetime64_any_dtype(self.df[column]):
                    self.df[column] = self.df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif pd.api.types.is_numeric_dtype(self.df[column]):
                    # 处理数值类型，将 NaN 转换为 None
                    self.df[column] = self.df[column].where(pd.notnull(self.df[column]), None)

            # 清理所有字符串列的空格
            for column in self.df.columns:
                if self.df[column].dtype == 'object':
                    self.df[column] = self.df[column].apply(self.clean_string)

            # 将DataFrame转换为字典列表
            records = self.df.to_dict('records')
            
            # 创建标准JSON格式
            json_data = {
                "status": "success",
                "data": {
                    "total": len(records),
                    "items": records
                }
            }
            
            # 打印JSON数据
            print("\nJSON数据:")
            print(json.dumps(json_data, ensure_ascii=False, indent=2))
            
            # 生成格式化字符串并添加到DataFrame
            formatted_strings = []
            print("\n格式化字符串:")
            for i, record in enumerate(records, 1):
                formatted_string = self.generate_formatted_string(record)
                if formatted_string:
                    formatted_strings.append(formatted_string)
                    print(f"{i}. {formatted_string}")

            # 将格式化字符串添加到DataFrame的I列
            self.df['格式化字符串'] = formatted_strings
            
            # 保存到新的Excel文件
            self.save_to_excel()
            
            return True
        except Exception as e:
            print(f"转换为JSON失败: {str(e)}")
            return False

def main():
    # 使用示例
    converter = ExcelConverter()
    
    # 读取Excel文件
    input_file = "34IFP问题记录20250224.xlsx"
    if not converter.read_excel(input_file):
        return

    # 转换为JSON并打印
    converter.convert_to_json()

if __name__ == "__main__":
    main() 