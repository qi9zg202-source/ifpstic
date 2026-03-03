# 总节省费用计算逻辑（计入节费按钮）

## 适用场景
当用户在页面中勾选/切换“计入节费”按钮时，本逻辑用于计算并展示“总节省费用”。

## 计算口径
- **不计算水费**
- **仅计算电费相关节省**
- **默认按高效制冷机房成本逻辑计算**
  - `EER = 5.0` 时为 **基准成本**
  - `EER = 实际EER` 时为 **客观成本**

## 名词与字段
- `eer_baseline`：基准 EER，固定为 5.0
- `eer_actual`：实际 EER（来自当期数据）
- `cost(eer)`：高效制冷机房成本计算函数（输入 EER，输出电费成本）
- `baseline_cost`：`cost(eer_baseline)`
- `actual_cost`：`cost(eer_actual)`
- `period`：统计周期（如月/年/自定义区间）

## 计算逻辑
1. **基准成本（EER=5.0）**
   - `baseline_cost = cost(5.0)`

2. **客观成本（EER=实际值）**
   - `actual_cost = cost(eer_actual)`

3. **节省费用**
   - `total_saving = baseline_cost - actual_cost`
   - 若 `total_saving < 0`，按 0 计（不展示为负节省）

3. **展示规则**
   - 货币单位与页面一致（如：万元/元）
   - 与统计周期一致（如：月/年/区间）
   - 若 `total_saving` 为空或无数据，展示为 `--`

## 边界与异常
- 缺失字段时：
  - 若 `eer_actual` 缺失，则 `actual_cost` 和 `total_saving` 置为 `--`
  - 若成本模型不可用，则 `baseline_cost`、`actual_cost`、`total_saving` 置为 `--`
- 负节省处理：不显示为负值（按 0）

## 示例
- `eer_actual = 5.8`
- `baseline_cost = cost(5.0) = 240 万元`
- `actual_cost = cost(5.8) = 200 万元`
- `total_saving = 40 万元`
