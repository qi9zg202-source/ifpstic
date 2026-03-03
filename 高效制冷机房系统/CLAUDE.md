# 晶圆厂高效制冷机房设计项目

## 项目概述
本项目是一个晶圆厂（FAB）高效制冷机房的设计和优化系统，包含运行策略分析、成本分析、热回收指标等功能模块。

## 技术栈
- **前端**: HTML + JavaScript（原生）
- **后端**: Node.js (env_manager_server.js)
- **数据库**: SQLite (env_manager.sqlite, test.db)
- **脚本**: Python 3.10 (word_mapper.py)
- **文档**: Markdown (PRD 文档)

## 项目结构
```
.
├── index.html                          # 主页面
├── env_manager.html                    # 环境管理界面
├── fab_cooling_cost_analysis.html      # 制冷成本分析
├── fab_ai_strategy_package_detail.html # AI策略包详情
├── 高效制冷机房-A运行优化策略功能.html  # 运行优化策略
├── env_manager_server.js               # Node.js 服务器
├── word_mapper.py                      # Python 工具脚本
├── env_manager.sqlite                  # 主数据库
├── test.db                             # 测试数据库
└── *_prd.md                            # 产品需求文档
```

## 开发规范

### HTML 文件
- 使用语义化标签
- 保持代码缩进一致（2空格）
- JavaScript 代码尽量模块化
- 注释使用中文

### 数据库操作
- 使用 SQLite3
- 数据库文件：env_manager.sqlite（生产）、test.db（测试）
- 操作前先备份数据库

### PRD 文档
- 使用 Markdown 格式
- 包含功能描述、交互逻辑、数据结构
- 文件命名：`{feature_name}_prd.md`

### Python 脚本
- Python 3.10+
- 使用 type hints
- 遵循 PEP 8 规范

## 常见任务

### 启动开发服务器
```bash
node env_manager_server.js
```

### 数据库操作
```bash
sqlite3 env_manager.sqlite
```

### 运行 Python 脚本
```bash
python word_mapper.py
```

## 注意事项
1. 修改数据库前务必备份
2. HTML 文件中的硬编码数据应逐步迁移到数据库
3. 新功能开发前先编写 PRD 文档
4. 代码注释和文档使用中文
5. 测试使用 test.db，不要直接操作 env_manager.sqlite

## 项目目标
- 优化晶圆厂制冷系统运行效率
- 降低能耗成本
- 提供数据驱动的决策支持
- 实现热回收效益分析
