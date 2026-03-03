#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel数据筛选脚本
功能：根据diclist.xlsx的A列匹配point__202506271617.xlsx的L列进行数据筛选
作者：Claude
日期：2024-07-12
"""

import pandas as pd
import os
import sys
from datetime import datetime
from pathlib import Path

def filter_excel_data():
    """
    主要功能：根据字典文件筛选数据文件
    
    流程：
    1. 读取 diclist.xlsx 的 A 列作为筛选条件
    2. 读取 point__202506271617.xlsx 数据文件
    3. 匹配 L 列与字典 A 列的数据
    4. 导出筛选结果到新的Excel文件
    """
    
    # 定义文件路径
    dict_file = "diclist.xlsx"
    data_file = "point__202506271617.xlsx"
    
    print("=" * 60)
    print("📊 Excel数据筛选工具")
    print("=" * 60)
    print(f"字典文件: {dict_file}")
    print(f"数据文件: {data_file}")
    print(f"工作目录: {os.getcwd()}")
    print("-" * 60)
    
    try:
        # 1. 检查文件是否存在
        if not os.path.exists(dict_file):
            print(f"❌ 错误：字典文件 '{dict_file}' 不存在")
            return False
            
        if not os.path.exists(data_file):
            print(f"❌ 错误：数据文件 '{data_file}' 不存在")
            return False
        
        print("✅ 文件检查通过")
        
        # 2. 读取字典文件的A列
        print(f"\n📖 读取字典文件: {dict_file}")
        try:
            dict_df = pd.read_excel(dict_file)
            print(f"字典文件形状: {dict_df.shape}")
            print(f"字典文件列名: {list(dict_df.columns)}")
            
            # 获取A列数据（第一列）
            dict_column_a = dict_df.iloc[:, 0].dropna().astype(str).unique()
            print(f"A列唯一值数量: {len(dict_column_a)}")
            print(f"A列前5个值: {dict_column_a[:5].tolist()}")
            
        except Exception as e:
            print(f"❌ 读取字典文件失败: {str(e)}")
            return False
        
        # 3. 读取数据文件
        print(f"\n📖 读取数据文件: {data_file}")
        try:
            data_df = pd.read_excel(data_file)
            print(f"数据文件形状: {data_df.shape}")
            print(f"数据文件列名: {list(data_df.columns)}")
            
            # 检查是否有L列（第12列，索引为11）
            if data_df.shape[1] < 12:
                print(f"❌ 错误：数据文件列数不足，当前只有 {data_df.shape[1]} 列，需要至少12列才能访问L列")
                return False
            
            # 获取L列数据（第12列）
            l_column_name = data_df.columns[11]  # L列是第12列，索引为11
            print(f"L列列名: '{l_column_name}'")
            
            # 显示L列的一些统计信息
            l_column_data = data_df.iloc[:, 11].astype(str)
            l_unique_count = l_column_data.nunique()
            l_null_count = data_df.iloc[:, 11].isnull().sum()
            
            print(f"L列唯一值数量: {l_unique_count}")
            print(f"L列空值数量: {l_null_count}")
            print(f"L列前5个值: {l_column_data.head().tolist()}")
            
        except Exception as e:
            print(f"❌ 读取数据文件失败: {str(e)}")
            return False
        
        # 4. 进行数据匹配筛选
        print(f"\n🔍 开始数据匹配...")
        try:
            # 将L列数据转换为字符串进行匹配
            data_df_copy = data_df.copy()
            data_df_copy['L_column_str'] = data_df_copy.iloc[:, 11].astype(str)
            
            # 筛选：L列的值在字典A列中存在的记录
            filtered_df = data_df_copy[data_df_copy['L_column_str'].isin(dict_column_a)]
            
            # 删除临时列
            filtered_df = filtered_df.drop('L_column_str', axis=1)
            
            print(f"原始数据行数: {len(data_df)}")
            print(f"筛选后行数: {len(filtered_df)}")
            print(f"筛选率: {len(filtered_df)/len(data_df)*100:.2f}%")
            
            # 显示匹配统计
            matched_values = set(data_df.iloc[:, 11].astype(str)) & set(dict_column_a)
            print(f"匹配到的唯一值数量: {len(matched_values)}")
            
        except Exception as e:
            print(f"❌ 数据匹配失败: {str(e)}")
            return False
        
        # 5. 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"filtered_data_{timestamp}.xlsx"
        
        # 6. 导出筛选结果
        print(f"\n💾 导出筛选结果...")
        try:
            filtered_df.to_excel(output_file, index=False)
            print(f"✅ 导出成功！")
            print(f"📁 输出文件: {output_file}")
            print(f"📊 输出数据行数: {len(filtered_df)}")
            print(f"📊 输出数据列数: {len(filtered_df.columns)}")
            
        except Exception as e:
            print(f"❌ 导出文件失败: {str(e)}")
            return False
        
        # 7. 生成详细报告
        print(f"\n📋 筛选报告:")
        print(f"├─ 字典文件: {dict_file} ({len(dict_column_a)} 个筛选条件)")
        print(f"├─ 数据文件: {data_file} ({len(data_df)} 行原始数据)")
        print(f"├─ 匹配列: {l_column_name} (第L列)")
        print(f"├─ 筛选结果: {len(filtered_df)} 行匹配数据")
        print(f"├─ 筛选率: {len(filtered_df)/len(data_df)*100:.2f}%")
        print(f"└─ 输出文件: {output_file}")
        
        # 8. 显示一些匹配的示例
        if len(filtered_df) > 0:
            print(f"\n🔍 筛选结果预览 (前5行):")
            print(filtered_df.head().to_string(max_cols=10))
        
        return True
        
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        return False

def check_files_info():
    """
    检查文件信息的辅助函数
    """
    dict_file = "diclist.xlsx"
    data_file = "point__202506271617.xlsx"
    
    print("📁 文件信息检查:")
    
    # 检查字典文件
    if os.path.exists(dict_file):
        try:
            dict_df = pd.read_excel(dict_file)
            print(f"✅ {dict_file}:")
            print(f"   形状: {dict_df.shape}")
            print(f"   A列数据类型: {dict_df.iloc[:, 0].dtype}")
            print(f"   A列示例: {dict_df.iloc[:5, 0].tolist()}")
        except Exception as e:
            print(f"❌ {dict_file}: 读取失败 - {str(e)}")
    else:
        print(f"❌ {dict_file}: 文件不存在")
    
    # 检查数据文件
    if os.path.exists(data_file):
        try:
            data_df = pd.read_excel(data_file, nrows=5)  # 只读前5行检查结构
            print(f"✅ {data_file}:")
            print(f"   预计形状: {data_df.shape} (仅前5行)")
            print(f"   总列数: {len(data_df.columns)}")
            if len(data_df.columns) >= 12:
                l_col_name = data_df.columns[11]
                print(f"   L列名称: '{l_col_name}'")
                print(f"   L列数据类型: {data_df.iloc[:, 11].dtype}")
                print(f"   L列示例: {data_df.iloc[:, 11].tolist()}")
            else:
                print(f"   ⚠️  列数不足，无法访问L列")
        except Exception as e:
            print(f"❌ {data_file}: 读取失败 - {str(e)}")
    else:
        print(f"❌ {data_file}: 文件不存在")

def main():
    """
    主函数
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check_files_info()
        return
    
    # 执行数据筛选
    success = filter_excel_data()
    
    if success:
        print("\n🎉 数据筛选完成！")
    else:
        print("\n💥 数据筛选失败！")
        print("\n💡 提示：可以使用 'python filter_excel_data.py --check' 检查文件信息")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {str(e)}")
        print("\n💡 请检查文件路径和格式是否正确")