# 文件名：main.py (真实 AI 版)

import google.generativeai as genai
import os
import fab_tools 
import getpass

# --- 1. 配置 API Key ---
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("提示：未检测到 GOOGLE_API_KEY 环境变量。")
    # 尝试让用户输入
    try:
        api_key = getpass.getpass("请输入您的 Google API Key (输入后看不见是正常的): ")
    except:
        api_key = input("请输入您的 Google API Key: ")

if not api_key:
    print("错误：必须提供 API Key 才能连接真实 AI。")
    exit(1)

genai.configure(api_key=api_key) 

# --- 2. 准备工具箱 ---
# 在这里告诉 AI 它可以调用哪些函数
# AI 会读取这些函数的文档字符串(Docstring)来区分它们的功能
tools_list = [
    fab_tools.check_machine_status, 
    fab_tools.search_maintenance_logs,
    fab_tools.send_maintenance_alert # <--- 新增的技能：发邮件
]

# --- 3. 初始化模型 ---
print("正在连接 Google AI 服务...")
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro-latest', 
    tools=tools_list 
)

# --- 4. 开启对话 ---
chat = model.start_chat(enable_automatic_function_calling=True)

print("--- Fab 智能助理 (在线版) 已启动 ---")
print("提示：此模式会真正连接 Google 的大脑，虽然它很聪明，但需要 API Key。")

while True:
    try:
        user_input = input("\n刘工请指示: ")
    except EOFError:
        break
        
    if user_input.lower() in ['exit', 'quit', '退出']:
        print("助理下班了。")
        break
        
    try:
        print("AI 思考中...", end="", flush=True)
        # 发送给真实 AI
        response = chat.send_message(user_input)
        
        # 清除“思考中”提示
        print("\r" + " " * 15 + "\r", end="")
        
        # 打印 AI 的回复
        print(f"AI 回复: {response.text}")
        
    except Exception as e:
        print(f"\n出错了: {e}")
        print("提示：如果报 404 或 Key 错误，请检查您的 API Key 是否正确，或网络是否通畅。")
