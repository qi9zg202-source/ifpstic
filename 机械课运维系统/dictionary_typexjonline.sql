/*
 Navicat Premium Dump SQL

 Source Server         : 10.110.210.160-uat-mysql
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44-log)
 Source Host           : 10.110.210.160:3306
 Source Schema         : ifp_account

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44-log)
 File Encoding         : 65001

 Date: 24/03/2025 09:51:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dictionary_type
-- ----------------------------
DROP TABLE IF EXISTS `dictionary_type`;
CREATE TABLE `dictionary_type`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '类别名称',
  `type_code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '类别编码',
  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'VALID' COMMENT '状态：VALID - 有效；INVALID - 无效',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注',
  `is_delete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除 0-未删除,1-已删除',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `fac_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '厂区',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_type_code`(`type_code`) USING BTREE COMMENT 'typeCode索引',
  INDEX `idx_type_name`(`type_name`) USING BTREE COMMENT 'typeName索引'
) ENGINE = InnoDB AUTO_INCREMENT = 237 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '字典类型' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of dictionary_type
-- ----------------------------
INSERT INTO `dictionary_type` VALUES (1, '科室', 'className', 'VALID', '科室', 0, '2024-04-09 18:39:57', '2024-09-10 10:30:19', NULL);
INSERT INTO `dictionary_type` VALUES (2, '备件分类', 'sparePartCategory', 'VALID', '备件分类', 0, '2024-04-09 19:42:07', '2024-04-09 19:54:41', NULL);
INSERT INTO `dictionary_type` VALUES (4, '品牌', 'brandName', 'VALID', '品牌', 0, '2024-04-10 15:31:21', '2024-04-10 16:04:04', NULL);
INSERT INTO `dictionary_type` VALUES (5, '备件等级', 'sparePartLevel', 'VALID', '', 0, '2024-04-10 15:59:59', '2024-04-10 16:04:11', NULL);
INSERT INTO `dictionary_type` VALUES (6, '库位', 'warehouse', 'VALID', '', 0, '2024-04-10 16:00:36', '2024-05-06 11:11:59', NULL);
INSERT INTO `dictionary_type` VALUES (7, '单位', 'unit', 'VALID', '', 0, '2024-04-10 16:00:52', '2024-04-10 16:00:52', NULL);
INSERT INTO `dictionary_type` VALUES (8, '来源', 'source', 'VALID', '', 0, '2024-04-10 16:45:58', '2024-04-10 16:45:58', NULL);
INSERT INTO `dictionary_type` VALUES (10, '计量单位', 'measureUnit', 'VALID', '', 0, '2024-04-18 10:24:57', '2024-04-18 10:24:57', NULL);
INSERT INTO `dictionary_type` VALUES (11, '值类型', 'valueType', 'VALID', '', 0, '2024-04-18 14:41:14', '2024-04-18 14:41:14', NULL);
INSERT INTO `dictionary_type` VALUES (29, '业务类型', 'business_type', 'VALID', '操作日志业务处理类型', 0, '2024-03-15 14:25:54', '2024-03-13 16:02:25', NULL);
INSERT INTO `dictionary_type` VALUES (30, '操作类别', 'operator_type', 'VALID', '使用者类型', 0, '2024-03-15 15:37:31', '2024-03-27 10:57:31', NULL);
INSERT INTO `dictionary_type` VALUES (32, '设备巡检任务状态', 'check_task_status', 'VALID', '设备巡检任务状态', 0, '2024-04-17 14:50:52', '2024-04-17 14:50:52', NULL);
INSERT INTO `dictionary_type` VALUES (33, '设备巡检任务审批状态', 'check_task_approve_status', 'VALID', '', 0, '2024-04-17 14:54:10', '2024-04-17 14:54:10', NULL);
INSERT INTO `dictionary_type` VALUES (37, '数字孪生平台-物模型-属性值类型', 'ATTRIBUTE_VALUE_TYPE', 'VALID', '物模型-属性值类型', 0, '2024-04-22 17:56:54', '2024-04-30 15:36:13', NULL);
INSERT INTO `dictionary_type` VALUES (38, '数字孪生平台-物模型-属性值单位', 'ATTRIBUTE_VALUE_UNIT', 'VALID', '属性值单位', 0, '2024-04-22 17:57:28', '2024-04-30 15:36:10', NULL);
INSERT INTO `dictionary_type` VALUES (44, '报警推送渠道', 'ALARM_PUSH_CHANNEL', 'VALID', '报警推送渠道', 0, '2024-04-29 16:55:24', '2024-04-29 16:55:24', NULL);
INSERT INTO `dictionary_type` VALUES (45, '报警处置状态', 'ALARM_DISPOSE_STATUS', 'VALID', '报警处置状态', 0, '2024-04-29 16:55:51', '2024-04-29 16:55:51', NULL);
INSERT INTO `dictionary_type` VALUES (46, '消息类型', 'MESSAGE_TYPE', 'VALID', '消息类型', 0, '2024-04-29 16:56:08', '2024-04-29 16:56:08', NULL);
INSERT INTO `dictionary_type` VALUES (48, '水科运维', 'WTTS', 'VALID', '', 0, '2024-04-30 17:35:21', '2024-09-06 13:31:02', NULL);
INSERT INTO `dictionary_type` VALUES (50, '工具分类', 'toolCategory', 'VALID', '', 0, '2024-05-06 17:28:21', '2024-05-06 17:28:21', NULL);
INSERT INTO `dictionary_type` VALUES (56, '报废原因', 'scrapReason', 'VALID', '', 0, '2024-05-09 11:30:31', '2024-05-09 11:30:31', NULL);
INSERT INTO `dictionary_type` VALUES (57, '工具品牌', 'toolBrand', 'VALID', '', 0, '2024-05-11 13:33:53', '2024-05-11 13:33:53', NULL);
INSERT INTO `dictionary_type` VALUES (58, '缺失隐患', 'LOSSES', 'VALID', '', 0, '2024-05-11 16:10:13', '2024-05-11 16:13:14', NULL);
INSERT INTO `dictionary_type` VALUES (59, 'SPC指标级别', 'SPCL', 'VALID', '', 0, '2024-05-16 13:38:51', '2024-05-16 13:38:51', NULL);
INSERT INTO `dictionary_type` VALUES (60, '厂区', 'factoryArea', 'VALID', '', 0, '2024-05-17 13:08:20', '2024-05-17 13:08:20', NULL);
INSERT INTO `dictionary_type` VALUES (62, 'FAB报警级别', 'FAB_ALARM_LEVEL', 'VALID', '', 0, '2024-05-17 16:22:03', '2024-05-17 16:22:03', NULL);
INSERT INTO `dictionary_type` VALUES (63, '可视化配置中心', 'visualConfigCenter', 'VALID', '', 0, '2024-05-20 08:27:41', '2024-05-20 08:27:41', NULL);
INSERT INTO `dictionary_type` VALUES (64, '气化科任务状态', 'gas_task_status', 'VALID', '', 0, '2024-05-20 11:09:54', '2024-09-10 13:06:52', NULL);
INSERT INTO `dictionary_type` VALUES (65, '设备巡检计划状态', 'check_plan_status', 'VALID', '', 0, '2024-05-23 08:42:01', '2024-05-23 08:42:01', NULL);
INSERT INTO `dictionary_type` VALUES (66, '设备巡检计划周期', 'check_cycle_unit', 'VALID', '', 0, '2024-05-23 08:48:25', '2024-05-27 09:14:05', NULL);
INSERT INTO `dictionary_type` VALUES (68, '位置类型', 'fac_position_type', 'VALID', '', 0, '2024-06-11 17:43:02', '2024-06-11 17:43:02', NULL);
INSERT INTO `dictionary_type` VALUES (69, '设备状态', 'EQP_STATUS', 'VALID', '', 0, '2024-06-11 17:43:26', '2024-06-19 16:20:29', NULL);
INSERT INTO `dictionary_type` VALUES (70, '报警级别', 'ALARM_LEVEL', 'VALID', '报警级别', 0, '2024-06-19 14:57:03', '2024-06-19 14:57:03', NULL);
INSERT INTO `dictionary_type` VALUES (71, '设备运行状态', 'EQP_RUN_STATUS', 'VALID', '', 0, '2024-06-19 15:24:01', '2024-06-19 15:24:01', NULL);
INSERT INTO `dictionary_type` VALUES (72, '设备停机分类', 'EQP_DOWN_TYPE', 'VALID', '', 0, '2024-06-19 15:25:33', '2024-06-19 15:25:33', NULL);
INSERT INTO `dictionary_type` VALUES (73, '机台保养类型', 'FAB_PM_CATEGORY', 'VALID', '', 0, '2024-06-19 19:04:47', '2024-06-19 19:04:47', NULL);
INSERT INTO `dictionary_type` VALUES (74, '机台区域', 'FAB_AREA', 'VALID', '', 0, '2024-06-19 19:05:10', '2024-06-19 19:05:10', NULL);
INSERT INTO `dictionary_type` VALUES (75, '机台保养计划状态', 'FAB_PM_PLAN_STATUS', 'VALID', '', 0, '2024-06-19 19:05:32', '2024-06-19 19:05:32', NULL);
INSERT INTO `dictionary_type` VALUES (76, '抄表项周期类型', 'METER_READING_ITEM_TYPE', 'VALID', '', 0, '2024-06-24 16:53:22', '2024-06-24 16:53:22', NULL);
INSERT INTO `dictionary_type` VALUES (77, '双碳', 'BICARBON', 'VALID', '', 0, '2024-07-05 14:05:29', '2024-07-05 14:05:29', NULL);
INSERT INTO `dictionary_type` VALUES (78, '巡检目标', 'check_target', 'VALID', '', 0, '2024-07-09 13:58:07', '2024-07-09 13:58:07', NULL);
INSERT INTO `dictionary_type` VALUES (79, '巡检内容类型', 'check_result_type', 'VALID', '', 0, '2024-07-09 13:58:58', '2024-07-09 13:58:58', NULL);
INSERT INTO `dictionary_type` VALUES (80, '交接班状态机', 'HANDOVER_STATUS', 'VALID', '', 0, '2024-07-11 13:56:13', '2024-07-11 13:56:13', NULL);
INSERT INTO `dictionary_type` VALUES (81, 'UT', 'UTILITY', 'VALID', '', 0, '2024-07-12 11:26:00', '2024-07-12 11:26:00', NULL);
INSERT INTO `dictionary_type` VALUES (82, 'PMS单位', 'PMS_Unit', 'VALID', '', 0, '2024-07-15 14:49:15', '2024-07-15 14:49:15', NULL);
INSERT INTO `dictionary_type` VALUES (83, '气化科供应提醒点位列表', 'GAS_SUPPLY_REMINDER_POINTS', 'VALID', '', 0, '2024-07-15 16:25:06', '2024-09-10 13:06:52', NULL);
INSERT INTO `dictionary_type` VALUES (84, '用途', 'used', 'VALID', '', 0, '2024-07-16 13:23:10', '2024-07-16 13:23:10', NULL);
INSERT INTO `dictionary_type` VALUES (85, '机械科运维', 'MCTS', 'VALID', '', 0, '2024-07-23 09:47:01', '2024-09-06 17:06:12', NULL);
INSERT INTO `dictionary_type` VALUES (86, '气化科值班工程师', 'GAS_DUTY_ENGINEER', 'VALID', '', 0, '2024-07-23 15:55:35', '2024-09-10 13:06:52', NULL);
INSERT INTO `dictionary_type` VALUES (97, '故障等级', 'FAULT_LEVEL', 'VALID', '', 0, '2024-08-07 09:51:46', '2024-08-07 09:51:46', NULL);
INSERT INTO `dictionary_type` VALUES (98, '维修需求来源', 'MAINTENANCE_SOURCE', 'VALID', '', 0, '2024-08-07 09:53:38', '2024-08-07 09:53:38', NULL);
INSERT INTO `dictionary_type` VALUES (99, '侦测器工单状态', 'GAS_DETECTOR_TASK_STATUS', 'VALID', '', 0, '2024-08-07 10:20:03', '2024-08-07 10:20:03', NULL);
INSERT INTO `dictionary_type` VALUES (100, '气化科ERC工程师', 'GAS_ERC_ENGINEER', 'VALID', '', 0, '2024-08-07 10:20:29', '2024-09-10 13:06:52', NULL);
INSERT INTO `dictionary_type` VALUES (101, '消防系统厂区地块区域', 'ERC_FACTORY_AREA', 'VALID', '', 0, '2024-08-20 14:08:25', '2024-08-20 14:08:25', NULL);
INSERT INTO `dictionary_type` VALUES (102, '消防系统设备状态', 'ERC_EQP_STATUS', 'VALID', '', 0, '2024-08-20 14:09:32', '2024-08-20 14:09:32', NULL);
INSERT INTO `dictionary_type` VALUES (103, '消防系统物资预警状态', 'ERC_MATERIAL_WARNING_STATUS', 'VALID', '', 0, '2024-08-20 14:11:24', '2024-08-20 14:11:24', NULL);
INSERT INTO `dictionary_type` VALUES (104, '消防系统物资入库类型', 'ERC_MATERIAL_IN_TYPE', 'VALID', '', 0, '2024-08-20 14:12:06', '2024-08-20 14:12:06', NULL);
INSERT INTO `dictionary_type` VALUES (105, '消防系统物资出库原因', 'ERC_MATERIAL_OUT_REASON', 'VALID', '', 0, '2024-08-23 13:12:14', '2024-08-23 13:12:14', NULL);
INSERT INTO `dictionary_type` VALUES (106, 'ERC设备巡检计划状态', 'ERC_CHECK_PLAN_STATUS', 'VALID', '', 0, '2024-08-12 13:14:45', '2024-08-12 13:14:45', NULL);
INSERT INTO `dictionary_type` VALUES (107, 'ERC设备巡检计划周期', 'ERC_CHECK_PLAN_CYCLE', 'VALID', '', 0, '2024-08-12 14:30:38', '2024-08-12 14:34:24', NULL);
INSERT INTO `dictionary_type` VALUES (108, 'ERC设备巡检任务状态', 'ERC_CHECK_TASK_STATUS', 'VALID', '', 0, '2024-08-12 14:34:09', '2024-08-12 14:34:09', NULL);
INSERT INTO `dictionary_type` VALUES (109, 'ERC设备巡检任务类型', 'ERC_CHECK_TASK_TYPE', 'VALID', '', 0, '2024-08-12 14:36:08', '2024-08-12 14:36:08', NULL);
INSERT INTO `dictionary_type` VALUES (110, 'ERC设备巡检任务审核状态', 'ERC_CHECK_TASK_APPROVE_STATUS', 'INVALID', '', 0, '2024-08-12 14:37:10', '2024-08-13 14:23:57', NULL);
INSERT INTO `dictionary_type` VALUES (111, 'ERC设备巡检规则类型', 'ERC_CHECK_RULE_TYPE', 'VALID', '', 0, '2024-08-12 15:13:05', '2024-08-12 15:13:05', NULL);
INSERT INTO `dictionary_type` VALUES (112, 'ERC设备巡检内容范围', 'ERC_CHECK_CONTENT_RANG', 'VALID', '', 0, '2024-08-12 15:39:46', '2024-08-12 15:39:46', NULL);
INSERT INTO `dictionary_type` VALUES (113, 'ERC设备巡检计划生成任务时间', 'ERC_CHECK_PLAN_TASK_CREATE_TIME', 'VALID', '', 0, '2024-08-15 20:14:22', '2024-08-15 20:14:22', NULL);
INSERT INTO `dictionary_type` VALUES (114, 'ERC设备巡检周期', 'ERC_EQP_CHECK', 'VALID', '设备巡检周期', 0, '2024-08-09 13:17:00', '2024-08-09 13:17:00', NULL);
INSERT INTO `dictionary_type` VALUES (115, 'ERC设备巡检任务是否超期', 'ERC_CHECK_TASK_TIME_OUT', 'VALID', '', 0, '2024-08-24 12:13:55', '2024-08-24 12:13:55', NULL);
INSERT INTO `dictionary_type` VALUES (116, '消防系统物资出入库转审专员岗位ID', 'ERC_MATERIAL_TRANSFER_POSITION', 'VALID', '', 0, '2024-08-24 15:47:48', '2024-08-24 15:47:48', NULL);
INSERT INTO `dictionary_type` VALUES (117, '核算管理', 'ACCOUNTING_MGT', 'VALID', '', 0, '2024-08-26 13:10:27', '2024-08-26 13:10:27', NULL);
INSERT INTO `dictionary_type` VALUES (118, '消防系统设备保养项目确认方式', 'ERC_MAINTAIN_PROJECT_CONFIRM_WAY', 'VALID', '', 0, '2024-08-27 14:42:05', '2024-08-27 14:42:05', NULL);
INSERT INTO `dictionary_type` VALUES (119, '消防系统设备保养工单状态', 'ERC_MAINTAIN_TASK_STATUS', 'VALID', '', 0, '2024-08-28 14:23:10', '2024-08-28 14:23:10', NULL);
INSERT INTO `dictionary_type` VALUES (120, '消防系统维修', 'ERC_MAINTENANCE_SOURCE', 'VALID', '', 0, '2024-08-28 17:23:32', '2024-08-28 17:23:32', NULL);
INSERT INTO `dictionary_type` VALUES (121, '消防系统维修优先级', 'ERC_MAINTENANCE_WEIGHT', 'VALID', '', 0, '2024-08-29 16:37:57', '2024-08-29 16:37:57', NULL);
INSERT INTO `dictionary_type` VALUES (122, 'e5092f63e642407b97199563708d5e5c', 'test呃呃呃', 'VALID', '', 0, '2024-08-29 16:44:59', '2024-08-29 16:45:03', NULL);
INSERT INTO `dictionary_type` VALUES (123, '2ce548e8b24f4b8394a6ecffa8aa56ab', 'cf3eb73c060f45eba4a343b158678aad', 'VALID', 'test', 0, '2024-08-29 16:46:56', '2024-08-29 16:48:49', NULL);
INSERT INTO `dictionary_type` VALUES (125, '异常点检执行方式', 'POINT_CHECK_EXECUTE', 'VALID', '', 0, '2024-09-06 16:58:18', '2024-09-06 16:58:18', NULL);
INSERT INTO `dictionary_type` VALUES (126, '异常点检来源', 'POINT_CHECK_SOURCE', 'VALID', '', 0, '2024-09-06 17:00:19', '2024-09-06 17:00:19', NULL);
INSERT INTO `dictionary_type` VALUES (127, '异常点检计划状态', 'POINT_CHECK_PLAN_STATUS', 'VALID', '', 0, '2024-09-06 17:02:35', '2024-09-06 17:02:35', NULL);
INSERT INTO `dictionary_type` VALUES (128, '异常点检任务状态', 'POINT_CHECK_TASK_STATUS', 'VALID', '', 0, '2024-09-06 17:03:09', '2024-09-06 17:03:09', NULL);
INSERT INTO `dictionary_type` VALUES (129, '室外天气读数', 'OUTDOOR_WEATHER', 'VALID', '', 0, '2024-09-06 17:09:15', '2024-09-06 17:09:15', NULL);
INSERT INTO `dictionary_type` VALUES (130, 'IFP巡检内容范围', 'INSPECT_CONTENT_RANGE', 'VALID', '', 0, '2024-09-14 10:50:37', '2024-09-14 10:50:37', NULL);
INSERT INTO `dictionary_type` VALUES (131, '能源指标类型', 'ENERGY_CATEGORY_TYPE', 'VALID', '', 0, '2024-09-14 14:21:10', '2024-09-14 14:21:10', NULL);
INSERT INTO `dictionary_type` VALUES (132, '能源指标单位', 'ENERGY_INDICATOR_UNIT', 'VALID', '', 0, '2024-09-14 14:21:38', '2024-09-14 14:21:38', NULL);
INSERT INTO `dictionary_type` VALUES (133, '能源指标', 'ENERGY_INDICATOR', 'VALID', '', 0, '2024-09-14 14:22:06', '2024-09-14 14:22:06', NULL);
INSERT INTO `dictionary_type` VALUES (134, '培训类型', 'TRAIN_TYPE', 'VALID', '', 0, '2024-09-20 10:49:04', '2024-09-20 10:49:04', NULL);
INSERT INTO `dictionary_type` VALUES (135, '培训状态', 'TRAIN_STATUS', 'VALID', '', 0, '2024-09-20 10:49:21', '2024-09-20 10:49:21', NULL);
INSERT INTO `dictionary_type` VALUES (137, '耗材全生命周期管理', 'CONSUMABLE_LIFE_CYCLE', 'VALID', '', 0, '2024-09-29 10:23:52', '2024-09-29 10:23:52', NULL);
INSERT INTO `dictionary_type` VALUES (139, '双碳指标', 'BICARBON_INDEX', 'VALID', '双碳指标', 0, '2024-09-29 13:38:28', '2024-09-29 13:38:28', NULL);
INSERT INTO `dictionary_type` VALUES (141, '能源', 'ENERGY', 'VALID', '', 0, '2024-09-29 17:11:58', '2024-09-29 17:11:58', NULL);
INSERT INTO `dictionary_type` VALUES (143, '部门ID', 'DEPT_ID', 'VALID', '', 0, '2024-10-24 13:30:35', '2024-10-24 13:30:35', NULL);
INSERT INTO `dictionary_type` VALUES (149, '物资出入库审核状态', 'MATERIAL_APPROVE_STATUS', 'VALID', '', 0, '2024-11-23 09:48:14', '2024-11-23 09:48:14', NULL);
INSERT INTO `dictionary_type` VALUES (151, '气化课供应提醒 气瓶 点位列表', 'GAS_SUPPLY_CYLINDER_POINTS', 'VALID', '', 0, '2024-11-06 14:27:34', '2024-07-14 14:27:34', NULL);
INSERT INTO `dictionary_type` VALUES (153, '气化课供应提醒 酸桶 点位列表', 'GAS_SUPPLY_BUCKET_POINTS', 'VALID', '', 0, '2024-11-06 14:27:34', '2024-07-14 14:27:34', NULL);
INSERT INTO `dictionary_type` VALUES (155, '气化课供应提醒 槽车 点位列表', 'GAS_SUPPLY_TANK_POINTS', 'VALID', '', 0, '2024-11-06 14:27:34', '2024-07-14 14:27:34', NULL);
INSERT INTO `dictionary_type` VALUES (157, '气化课-特气单位', 'SPECIALTY_GAS_UNIT', 'VALID', '', 0, '2024-08-06 17:14:06', '2024-08-06 17:14:06', NULL);
INSERT INTO `dictionary_type` VALUES (159, '看板组件类型', 'COMPONENT_TYPE', 'VALID', '', 0, '2024-11-26 19:05:40', '2024-11-26 19:05:40', NULL);
INSERT INTO `dictionary_type` VALUES (161, '数据类型', 'DATA_TYPE', 'VALID', '', 0, '2024-11-26 20:12:11', '2024-11-26 20:12:11', NULL);
INSERT INTO `dictionary_type` VALUES (163, '衍生指标类型', 'DERIVED_MEASURE_TYPE', 'VALID', '', 0, '2024-11-26 20:11:02', '2024-11-26 20:11:02', NULL);
INSERT INTO `dictionary_type` VALUES (165, '子包', 'INTOUCH_PACKAGE_NAME', 'VALID', '', 0, '2024-11-26 20:13:03', '2024-11-26 20:13:03', NULL);
INSERT INTO `dictionary_type` VALUES (167, '指标来源', 'MEASURE_SOURCE', 'VALID', '', 0, '2024-11-26 20:11:53', '2024-11-26 20:11:53', NULL);
INSERT INTO `dictionary_type` VALUES (169, '指标类型', 'MEASURE_TYPE', 'VALID', '', 0, '2024-11-26 20:11:35', '2024-11-26 20:11:35', NULL);
INSERT INTO `dictionary_type` VALUES (171, '指标点位单位', 'MEASURE_UNIT', 'VALID', '', 0, '2024-11-26 20:13:22', '2024-11-26 20:13:22', NULL);
INSERT INTO `dictionary_type` VALUES (173, '监控实体类型', 'MONITOR_ENTITY_TYPE', 'VALID', '', 0, '2024-11-26 20:10:29', '2024-11-26 20:10:29', NULL);
INSERT INTO `dictionary_type` VALUES (175, '监控物料', 'MONITOR_MATERIAL', 'VALID', '', 0, '2024-11-26 20:12:39', '2024-11-26 20:12:39', NULL);
INSERT INTO `dictionary_type` VALUES (177, '监控物料-废弃', 'MONITOR_MATERIAL_WASTE', 'VALID', '', 0, '2024-11-26 20:13:39', '2024-11-26 20:13:39', NULL);
INSERT INTO `dictionary_type` VALUES (179, '衍生指标统计周期', 'statistics_cycle', 'VALID', '', 0, '2024-11-26 20:11:22', '2024-11-26 20:11:22', NULL);
INSERT INTO `dictionary_type` VALUES (181, '电科运维', 'ELTS', 'VALID', '', 0, '2024-06-13 16:04:52', '2025-01-02 09:27:36', NULL);
INSERT INTO `dictionary_type` VALUES (183, '气化科运维', 'GAS_TS', 'VALID', '', 0, '2024-11-26 10:11:30', '2024-11-26 10:11:30', NULL);
INSERT INTO `dictionary_type` VALUES (185, '考试类型', 'EXAM_TYPE', 'VALID', '考试类型', 0, '2024-12-01 19:44:07', '2024-12-01 19:44:07', NULL);
INSERT INTO `dictionary_type` VALUES (187, '水科运维-验证线配置', 'WATER_VERIFICATION', 'VALID', '', 0, '2024-10-27 10:10:31', '2024-10-27 10:12:23', NULL);
INSERT INTO `dictionary_type` VALUES (189, 'PID及拓扑图', 'PID_AND_TOPO', 'VALID', 'PID及拓扑图', 0, '2024-12-05 18:34:35', '2024-12-05 18:34:35', NULL);
INSERT INTO `dictionary_type` VALUES (191, 'FFU风机过滤单元', 'EQP_CONSUMABLE', 'VALID', '', 0, '2024-12-12 17:16:04', '2024-12-12 17:26:14', NULL);
INSERT INTO `dictionary_type` VALUES (193, '设备使用耗材', '设备使用耗材', 'VALID', '设备使用耗材', 0, '2024-12-12 17:17:28', '2024-12-12 17:17:28', NULL);
INSERT INTO `dictionary_type` VALUES (195, '备件寿命单位', 'sparePartLifeUnit', 'VALID', '', 0, '2024-12-30 11:45:11', '2024-12-30 11:45:11', NULL);
INSERT INTO `dictionary_type` VALUES (197, '气化-TANK容量', 'GAS_TANK_CAPACITY', 'VALID', '', 0, '2024-12-21 14:44:57', '2024-12-21 14:44:57', NULL);
INSERT INTO `dictionary_type` VALUES (203, '算法', 'ALGORITHM', 'VALID', '算法数仓字典', 0, '2024-12-23 13:25:38', '2024-12-23 13:27:03', NULL);
INSERT INTO `dictionary_type` VALUES (205, '可视化设备类型', 'VISUAL_EQP_TYPE', 'VALID', '', 0, '2024-12-30 09:35:44', '2024-12-30 09:35:44', NULL);
INSERT INTO `dictionary_type` VALUES (207, '可视化属性值类型', 'VISUAL_VALUE_TYPE', 'VALID', '', 0, '2025-01-03 11:05:24', '2025-01-03 11:05:24', NULL);
INSERT INTO `dictionary_type` VALUES (209, '点位采集类型', 'POINT_COLLECT_TYPE', 'VALID', '', 0, '2025-01-15 14:45:47', '2025-01-15 14:45:47', NULL);
INSERT INTO `dictionary_type` VALUES (211, '点位对应设备状态', 'POINT_EQP_STATUS', 'VALID', '', 0, '2025-01-15 14:45:47', '2025-01-15 14:45:47', NULL);
INSERT INTO `dictionary_type` VALUES (213, '一期值班电话', 'CLASS_NAME_PHONE', 'VALID', '', 0, '2025-01-20 16:38:58', '2025-02-25 13:59:01', NULL);
INSERT INTO `dictionary_type` VALUES (219, '种类', 'typeCategory', 'VALID', '', 0, '2025-02-19 14:45:07', '2025-02-19 14:45:07', NULL);
INSERT INTO `dictionary_type` VALUES (221, '能源种类物料编码', 'ENERGY_MATERIAL_CODE', 'VALID', '能源模型-能源种类名称-数仓物料编码', 0, '2025-02-19 14:48:07', '2025-02-19 14:48:07', NULL);
INSERT INTO `dictionary_type` VALUES (223, '二期值班电话', 'CLASS_NAME_PHONE_TWO', 'VALID', '', 0, '2025-02-25 13:59:23', '2025-02-25 13:59:23', NULL);
INSERT INTO `dictionary_type` VALUES (225, 'ERC消防系统值班电话', 'ERC_FAC_PHONE', 'VALID', '', 0, '2025-02-25 13:59:42', '2025-02-25 13:59:42', NULL);
INSERT INTO `dictionary_type` VALUES (227, '设备保养过滤节假日', 'EQP_PMS_FILTER_DATE', 'VALID', '', 0, '2025-02-26 15:25:13', '2025-02-26 15:25:13', NULL);
INSERT INTO `dictionary_type` VALUES (229, '指标标签', 'measure_tag', 'VALID', '', 0, '2025-03-18 17:47:13', '2025-03-18 17:47:13', NULL);
INSERT INTO `dictionary_type` VALUES (231, '可视化组件属性值类型', 'VISUAL_COM_VALUE_TYPE', 'VALID', '', 0, '2025-03-19 14:54:55', '2025-03-19 14:54:55', NULL);
INSERT INTO `dictionary_type` VALUES (233, '报警文档事件类型-侦测器', 'event_type_detector', 'VALID', '', 0, '2025-03-20 13:39:07', '2025-03-20 13:39:07', NULL);
INSERT INTO `dictionary_type` VALUES (235, '报警文档事件类型-手动录入', 'event_type_manual', 'VALID', '', 0, '2025-03-20 13:39:07', '2025-03-20 13:39:07', NULL);

SET FOREIGN_KEY_CHECKS = 1;
