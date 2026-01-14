---
description: 商业记者访谈工作流：深度挖掘用户隐性知识并生成文章
---

# 商业记者访谈工作流 (/interview)

本工作流调用 **商业记者 (Commercial Journalist)** 技能，对用户进行深度访谈，并基于访谈内容和提供的素材生成风格化的文章。

## 执行步骤

1. **环境准备**：
   - 加载核心技能：
     - 技能定义：`[SKILL.md](file:///Users/bing/project/me/writer/.agent/skills/commercial-journalist/SKILL.md)`
   - 加载默认风格：
     - `[我的写作风格.md](file:///Users/bing/project/me/writer/.gemini/个人经历/我的写作风格.md)`
   - **读取输入**：如果用户提供了文件路径（如详情页、笔记），请先仔细阅读该文件作为访谈背景。

2. **执行访谈 (Phase 1)**：
   - 激活 `commercial-journalist` 角色。
   - 如果有输入文件，基于文件内容设计第一个问题。
   - 如果没有输入文件，基于用户提供的简单话题开启访谈。
   - 执行标准 5 轮访谈循环（参考 SKILL.md 定义）。

3. **生成文章 (Phase 2)**：
   - 访谈结束后，利用 SKILL.md 中的逻辑，结合 `我的写作风格.md` 生成 5 个标题和正文。

## 如何触发

在聊天框中输入：
- `/interview` (无参数，纯即兴访谈)
- `/interview [文件路径]` (基于文档的深度访谈)
