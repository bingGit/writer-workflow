---
trigger: model_decision
description: 需要提交 git 时触发
---

## 重要：语言要求
**所有AI生成的Git提交信息必须使用中文（简体中文）**
**All AI-generated Git commit messages MUST be in Chinese (Simplified Chinese)**

## 提交信息生成规则
- **强制要求**：所有Git提交信息必须使用中文，禁止使用英文
- 提交信息格式遵循约定式提交规范（Conventional Commits）
- 提交类型使用中文说明：
  - feat: 新功能
  - fix: 修复bug
  - docs: 文档更新
  - style: 代码格式调整
  - refactor: 重构
  - perf: 性能优化
  - test: 测试相关
  - chore: 构建过程或辅助工具的变动
  - revert: 回滚

## 提交信息示例（必须遵循此格式）
- feat: 添加商户管理功能
- fix: 修复订单支付状态更新问题
- docs: 更新API文档说明
- refactor: 重构用户认证模块

## AI提示词
当生成Git提交信息时，请：
1. 使用中文（简体中文）描述所有变更
2. 遵循约定式提交格式：<类型>: <中文描述>
3. 主题行不超过50个字符
4. 详细描述使用中文说明变更内容和原因

## 语言偏好
- 代码注释：中文
- 提交信息：中文（强制）
- 文档：中文
- AI对话：中文
