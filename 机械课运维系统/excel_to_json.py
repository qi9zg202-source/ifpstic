import pandas as pd
import json
from datetime import datetime

def excel_to_json(excel_file):
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 打印列名
        print("Excel文件的列名:")
        print(df.columns.tolist())
        print("\n")

        # 处理日期时间格式
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')

        # 将DataFrame转换为字典列表
        records = df.to_dict('records')
        
        # 创建JSON结构
        json_data = {
            "status": "success",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data": {
                "total": len(records),
                "items": records
            }
        }
        
        # 打印格式化的JSON
        print("JSON数据:")
        print(json.dumps(json_data, ensure_ascii=False, indent=2))
        
        # 可选：保存到文件
        output_file = excel_file.replace('.xlsx', '_output.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"\nJSON已保存到文件: {output_file}")
        
        return json_data
        
    except Exception as e:
        print(f"处理Excel文件时出错: {str(e)}")
        return None

def main():
    # Excel文件路径
    excel_file = "34IFP问题记录20250224.xlsx"  # 替换为你的Excel文件名
    
    # 转换Excel到JSON
    excel_to_json(excel_file)

if __name__ == "__main__":
    main() 