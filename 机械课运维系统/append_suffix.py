#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理脚本：为第一列所有文本追加 _tt 后缀
作者：Claude
日期：2024-07-12
"""

import pandas as pd
import sys
import os
from pathlib import Path

def append_suffix_to_first_column(input_file, output_file=None, suffix="_tt"):
    """
    为Excel或CSV文件的第一列所有文本追加指定后缀
    
    参数:
    input_file (str): 输入文件路径
    output_file (str): 输出文件路径，如果为None则覆盖原文件
    suffix (str): 要追加的后缀，默认为 "_tt"
    """
    
    try:
        # 检查文件是否存在
        if not os.path.exists(input_file):
            print(f"错误：文件 '{input_file}' 不存在")
            return False
        
        # 获取文件扩展名
        file_ext = Path(input_file).suffix.lower()
        
        # 根据文件类型读取数据
        if file_ext in ['.xlsx', '.xls']:
            print(f"读取Excel文件: {input_file}")
            df = pd.read_excel(input_file)
        elif file_ext == '.csv':
            print(f"读取CSV文件: {input_file}")
            df = pd.read_csv(input_file, encoding='utf-8')
        else:
            print(f"错误：不支持的文件类型 '{file_ext}'")
            print("支持的文件类型：.xlsx, .xls, .csv")
            return False
        
        print(f"原始数据形状: {df.shape}")
        print(f"第一列名称: '{df.columns[0]}'")
        
        # 显示第一列前5个值（处理前）
        print(f"\n处理前第一列前5个值:")
        print(df.iloc[:5, 0].tolist())
        
        # 获取第一列列名
        first_column = df.columns[0]
        
        # 为第一列所有值追加后缀
        # 先转换为字符串，再追加后缀
        df[first_column] = df[first_column].astype(str) + suffix
        
        # 显示第一列前5个值（处理后）
        print(f"\n处理后第一列前5个值:")
        print(df.iloc[:5, 0].tolist())
        
        # 确定输出文件路径
        if output_file is None:
            output_file = input_file
            print(f"\n将覆盖原文件: {output_file}")
        else:
            print(f"\n将保存到新文件: {output_file}")
        
        # 根据文件类型保存数据
        output_ext = Path(output_file).suffix.lower()
        
        if output_ext in ['.xlsx', '.xls']:
            df.to_excel(output_file, index=False)
        elif output_ext == '.csv':
            df.to_csv(output_file, index=False, encoding='utf-8')
        else:
            # 如果输出文件没有扩展名，使用与输入文件相同的格式
            if file_ext in ['.xlsx', '.xls']:
                output_file += '.xlsx'
                df.to_excel(output_file, index=False)
            else:
                output_file += '.csv'
                df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✅ 处理完成！共处理 {len(df)} 行数据")
        print(f"📁 输出文件: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {str(e)}")
        return False

def main():
    """
    主函数：处理命令行参数或交互式输入
    """
    print("=" * 60)
    print("📝 文本处理工具：为第一列追加后缀")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 命令行模式
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        suffix = sys.argv[3] if len(sys.argv) > 3 else "_tt"
        
        print(f"命令行模式:")
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file if output_file else '覆盖原文件'}")
        print(f"后缀: {suffix}")
        
    else:
        # 交互式模式
        print("交互式模式:")
        print("请输入文件信息（支持 .xlsx, .xls, .csv 格式）\n")
        
        # 获取输入文件路径
        input_file = input("请输入文件路径: ").strip().strip('"\'')
        
        if not input_file:
            print("❌ 文件路径不能为空")
            return
        
        # 获取输出文件路径（可选）
        output_file = input("请输入输出文件路径（留空则覆盖原文件）: ").strip().strip('"\'')
        if not output_file:
            output_file = None
        
        # 获取后缀（可选）
        suffix = input("请输入要追加的后缀（默认为 _tt）: ").strip()
        if not suffix:
            suffix = "_tt"
    
    print("\n开始处理...")
    
    # 执行处理
    success = append_suffix_to_first_column(input_file, output_file, suffix)
    
    if success:
        print("\n🎉 处理成功完成！")
    else:
        print("\n💥 处理失败，请检查错误信息")

# 使用示例
def show_examples():
    """显示使用示例"""
    print("\n" + "=" * 60)
    print("📚 使用示例:")
    print("=" * 60)
    
    examples = [
        "# 命令行使用:",
        "python append_suffix.py input.xlsx",
        "python append_suffix.py input.xlsx output.xlsx",
        "python append_suffix.py input.csv output.csv _suffix",
        "",
        "# Python脚本中使用:",
        "from append_suffix import append_suffix_to_first_column",
        "append_suffix_to_first_column('data.xlsx', 'data_modified.xlsx', '_tt')",
        "",
        "# 支持的文件格式:",
        "- Excel文件: .xlsx, .xls",
        "- CSV文件: .csv",
    ]
    
    for example in examples:
        print(example)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {str(e)}")
    
    # 显示使用示例
    if len(sys.argv) == 1:  # 只在交互模式下显示
        show_examples()