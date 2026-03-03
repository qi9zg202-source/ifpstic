import pandas as pd
import sys

def check_duplicates_in_column_a(df):
    # 获取第一列的名称
    first_column = df.columns[0]
    
    # 找出重复的值
    duplicates = df[df[first_column].duplicated(keep=False)]
    
    print("\n" + "="*50)
    print(f"重复数据检查结果 (第一列: {first_column})")
    print("="*50)
    
    if not duplicates.empty:
        print(f"\n发现 {len(duplicates)} 行重复数据!")
        # 按第一列分组并显示重复项
        duplicate_groups = duplicates.groupby(first_column)
        for value, group in duplicate_groups:
            print(f"\n重复值: '{value}'")
            print(f"出现次数: {len(group)}")
            print("出现在以下行:")
            for index in group.index:
                print(f"- 第 {index + 1} 行")
            print("-" * 30)
    else:
        print(f"\n第一列中没有发现重复数据")
    
    print("\n数据基本信息:")
    print(f"总行数: {len(df)}")
    print(f"总列数: {len(df.columns)}")
    print("="*50)

def check_ampersand_records(df):
    # 获取第一列的名称
    first_column = df.columns[0]
    
    # 筛选出包含"&"的记录
    ampersand_records = df[df[first_column].str.contains('&', na=False)]
    
    print("\n" + "="*50)
    print(f"包含'&'符号的记录统计")
    print("="*50)
    
    if len(ampersand_records) > 0:
        print(f"\n总共找到 {len(ampersand_records)} 条包含'&'的记录")
        print("\n所有包含'&'的记录:")
        for index, row in ampersand_records.iterrows():
            print(f"- 第 {index + 1} 行: {row[first_column]}")
    else:
        print("\n没有找到包含'&'符号的记录")
    
    print("="*50)

def check_p2_records(df):
    # 获取第一列的名称
    first_column = df.columns[0]
    
    # 筛选出带有"_P2"的记录
    p2_records = df[df[first_column].str.contains('_P2', na=False)]
    
    print("\n" + "="*50)
    print(f"带有'_P2'的记录统计")
    print("="*50)
    
    print(f"\n总共找到 {len(p2_records)} 条带有'_P2'的记录")
    
    # 检查这些记录中是否有重复
    duplicates = p2_records[p2_records[first_column].duplicated(keep=False)]
    
    if not duplicates.empty:
        print(f"\n在带有'_P2'的记录中发现 {len(duplicates)} 行重复数据!")
        # 按第一列分组并显示重复项
        duplicate_groups = duplicates.groupby(first_column)
        for value, group in duplicate_groups:
            print(f"\n重复值: '{value}'")
            print(f"出现次数: {len(group)}")
            print("出现在以下行:")
            for index in group.index:
                print(f"- 第 {index + 1} 行")
            print("-" * 30)
    else:
        print(f"\n在带有'_P2'的记录中没有发现重复数据")
    
    # 显示一些带_P2的记录示例
    print("\n带'_P2'的记录示例（前5条）:")
    for index, row in p2_records.head().iterrows():
        print(f"- {row[first_column]}")
    
    print("="*50)

def read_excel_file(file_path):
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 检查包含&的记录
        check_ampersand_records(df)
        
        # 检查A列重复数据
        check_duplicates_in_column_a(df)
        
        # 检查带P2的记录
        check_p2_records(df)
        
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")

if __name__ == "__main__":
    file_path = "10601sticarea0601.xlsx"
    read_excel_file(file_path) 