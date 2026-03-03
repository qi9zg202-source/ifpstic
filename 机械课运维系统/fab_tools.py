# fab_tools.py

# 模拟的数据库数据
MOCK_DB = {
    "EQP-01": {"status": "RUNNING", "temp": 23.5, "alarm": None},
    "EQP-02": {"status": "DOWN", "temp": 45.1, "alarm": "Pump Failure"},
    "EQP-03": {"status": "IDLE", "temp": 20.0, "alarm": None}
}

def check_machine_status(machine_id: str) -> str:
    """
    查询 Fab 内特定机台的实时运行状态、温度及报警信息。
    当用户问“现在的状态”、“温度多少”、“有没有报警”时使用。
    
    Args:
        machine_id: 机台的唯一编号 (例如: "EQP-01", "EQP-02")
        
    Returns:
        返回一段包含机台状态、温度和报警详情的文本描述。
    """
    # 模拟查询逻辑
    data = MOCK_DB.get(machine_id)
    
    if not data:
        return f"系统提示：找不到机台 {machine_id} 的信息，请检查编号。"
    
    return f"机台 {machine_id} 当前状态: {data['status']}, 温度: {data['temp']}°C, 报警: {data['alarm'] or '无'}"

def search_maintenance_logs(machine_id: str) -> str:
    """
    查询机台的历史维修记录和保养日志。
    当用户问“以前修过什么”、“历史记录”、“什么时候保养的”时使用。
    
    Args:
        machine_id: 机台编号
    """
    # 这里模拟返回一些假数据
    return f"[{machine_id} 维修记录] 1. 2023-12-01 更换过滤网; 2. 2023-11-15 加注冷却液。"

def send_maintenance_alert(machine_id: str, issue_description: str) -> str:
    """
    给维修部门发送报警邮件通知。
    当检测到机台有故障，或者用户明确要求“通知维修”、“发邮件”时使用。
    
    Args:
        machine_id: 故障的机台编号
        issue_description: 故障的简要描述
    """
    print(f"\n[系统后台] 正在连接邮件服务器...")
    print(f"[邮件发送] To: maintenance@fab-corp.com | Subject: {machine_id} Alert")
    print(f"[邮件内容] 机台 {machine_id} 发生异常: {issue_description}")
    print(f"[系统后台] 发送成功！\n")
    return "邮件已成功发送给维修部。"
