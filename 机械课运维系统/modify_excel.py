import pandas as pd

def modify_excel():
    try:
        # 读取Excel文件
        file_path = "10601sticarea0601.xlsx"
        df = pd.read_excel(file_path)
        
        # 获取第一列的名称
        first_column = df.columns[0]
        
        # 修改第一列的值，添加"MACHINE_"前缀
        df[first_column] = 'MACHINE_' + df[first_column].astype(str)
        
        # 保存修改后的文件
        df.to_excel(file_path, index=False)
        print(f"\n成功修改Excel文件：{file_path}")
        print(f"已在第一列（{first_column}）的每个值前添加'MACHINE_'前缀")
        print("\n修改后的前5行示例：")
        print(df[first_column].head())
        
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")

if __name__ == '__main__':
    modify_excel() 