---
description: Pencil JSON 设计工具标准操作流程 - 从需求到交付的完整指南
---

# Pencil 设计工作流 SOP

> **文件 Input**: 设计需求、参考样式、内容文案  
> **文件 Output**: 可渲染的 `.pen` JSON 文件、工作流程文档  
> **文件 Pos**: 设计工具使用规范，指导 Pencil JSON 格式的卡片设计

---

## 一、项目背景

**原始需求**: 为小红书创建 5 张审美知识卡片  
**技术选型**: Pencil JSON 设计工具（声明式 UI 描述语言）  
**目标交付**: 视觉统一、排版精良、可复用的卡片模板系统

---

## 二、核心设计原则 (First Principles)

**1. Physical Layer First (物理层优先)**
- **定义**: 在构建视觉效果时，不要先思考"UI组件"（容器、边框、控件），而是先思考"物理构成"（材质、光线、墨水、缺陷）。
- **实践**: 
  - 不要画一个"白色背景的 Container"，而是画一张"纸"。
  - 纸有纹理 (Texture)，有厚度 (Shadow)，有吸墨性 (Ink Bleed)。
  - **警惕**: 避免用构建软件界面的逻辑去构建物理世界的投影。

**2. Correctness by Construction (构造即正确)**
- **定义**: 优先使用脚本/代码生成复杂结构文件，而非手动或文本替换。
- **实践**: 脚本是"动态文档"，参数化设计提供了更高的维护性和回溯能力。

---

## 三、完整工作流程

### 阶段 1: 需求分析与样式确定

#### 步骤 1.1 明确设计要求
- [ ] 确定卡片数量和主题
- [ ] 收集参考样式（如 `xiaohongshu_vibe.md`）
- [ ] 定义核心视觉元素（色彩、字体、效果）

#### 步骤 1.2 建立视觉规范
**本项目采用的核心样式**:
```json
{
  "毛玻璃容器": {
    "fill": "#FFFFFF1A",
    "effect": {
      "type": "background_blur",
      "radius": 40
    }
  },
  "双层文字阴影": {
    "effect": {
      "type": "shadow",
      "shadowType": "outer",
      "color": "#00000066",
      "offset": {"x": 2, "y": 2},
      "blur": 0
    }
  }
}
```

**呼吸感排版层级**:
- 标题: 70px, Bold, 黄色 (#FDED9EFF)
- 主文本: 54px, Bold, 白色 (#FFFFFFFF)
- 辅助文本: 42px, Normal, 黄色-80% (#FDED9ECC)
- 注释/隐喻文本: 36px, Italic, 白色-60% (#FFFFFF99)

**🎨 主题-背景色匹配表 (莫兰迪色系)**:

| 主题类型 | 推荐色值 | 心理暗示 |
|---------|---------|---------|
| 通用/封面 | `#5B8BA3` 蓝灰 | 专业、沉稳、信任 |
| 定义/解释 | `#4A7A8F` 深蓝灰 | 深入、权威、层次递进 |
| 疗愈/修复 | `#6B8E7D` 雾霾绿 | 自然、镇静、生命力 |
| 情绪/内省 | `#7B7291` 紫灰 | 神秘、内省、共情 |
| 温暖/接纳 | `#8B7D6B` 暖灰 | 包容、安全、大地感 |
| 警示/重点 | `#A68B7C` 砖红灰 | 注意、重要、行动 |

---

### 阶段 2: JSON 结构搭建

#### 步骤 2.1 创建基础文件结构
```json
{
  "name": "项目名称",
  "pages": [
    {
      "name": "P1: 封面",
      "width": 1080,
      "height": 1440,
      "fill": "渐变背景",
      "children": [
        // 背景层
        // 内容层
      ]
    }
  ]
}
```

#### 步骤 2.2 分层设计原则
1. **背景层**: 图片 + overlay 蒙版（opacity: 0.4）
2. **内容层**: Frame 容器 + 垂直布局
3. **文本层**: 分层文本组件（标题/正文/注释）

**⚠️ 关键约定：绝对定位 vs 自动布局**
- 若需要使用 `x`, `y` 坐标精确控制位置，父级 Frame **必须** 设置 `"layout": "none"`。
- 若使用 `gap`, `padding` 进行自动排列，父级 Frame 应设置 `"layout": "vertical"`。

#### 步骤 2.3 全自动生成 (Integrated Generation)
**执行逻辑**: 使用 Python 脚本将数据源转化为 JSON 卡片和配图提示词。

**操作命令**:
```bash
# 编辑 scripts/generate_card_series.py 填入卡片数据 (Content + Metaphor)
# 然后运行:
python3 scripts/generate_card_series.py
```

**Output**:
1. `article/../pencil/project.pen`: 可直接渲染的卡片文件
2. `article/../pencil/project_prompts.txt`: 配套的 Midjourney/SD 提示词列表（已自动同步背景色和隐喻）

#### 步骤 3.1 样式统一化（P2-P5）
**从 P2 确定的毛玻璃+双层文字模板**:
```json
{
  "type": "frame",
  "fill": "#FFFFFF1A",
  "effect": {"type": "background_blur", "radius": 40},
  "layout": "vertical",
  "gap": 40,
  "padding": 60,
  "children": [
    // 文本内容
  ]
}
```

**⚠️ 关键错误 #2: 直接替换大块 JSON 导致结构损坏**
- **问题**: 使用 `replace_file_content` 替换 P2-P5 时，由于目标内容不唯一导致 JSON 格式错误
- **表现**: `Expecting ',' delimiter: line 808 column 11`
- **解决**: 改用 Python 脚本全量重建文件

---

### 阶段 4: 呼吸感排版优化

#### 步骤 4.1 文本层级拆解
**从单文本块到多层组件**:

❌ **Before (扁平结构)**:
```json
{
  "type": "text",
  "content": "标题\n\n正文内容\n\n注释",
  "fontSize": 42
}
```

✅ **After (层级结构)**:
```json
{
  "type": "frame",
  "layout": "vertical",
  "gap": 12,
  "children": [
    {"type": "text", "fontSize": 54, "fontWeight": "bold", "fill": "#FFF"},
    {"type": "text", "fontSize": 42, "fill": "#FDED9ECC"},
    {"type": "text", "fontSize": 36, "fontStyle": "italic", "fill": "#FFFFFF99"}
  ]
}
```

#### 步骤 4.2 间距与对齐微调
- **垂直间距**: 使用 `gap` 控制（12px / 40px / 50px）
- **内边距**: 容器统一 `padding: 60`
- **对齐方式**: P1 使用 `center`，P2-P5 使用默认 `flex-start`

**🎯 水平居中“三位一体”法则**
若要在绝对定位（`layout: "none"`）下实现文本水平居中，必须同时满足：
1. `x": 0`（起始位置）
2. `width": 1080`（容器宽度撑满画布）
3. `textAlign": "center"`（文本在容器内对齐）

**🚧 高风险资产“降级占位”策略**
当插画、照片等复杂资产尚未就绪时，先构建一个 **Placeholder Frame**：
- 显式标注 `width` 和 `height`
- 并在内部放置 `text` 标注文件名和建议比例
- **目的**: 确保在不依赖最终素材的情况下，完成 90% 的版式和重心调试。

---

### 阶段 5: 内容优化（基于 xiaohongshu_vibe.md）

#### 步骤 5.1 文案风格调整
**遵循原则**:
- 短句优先，善用换行
- 减少说教感，增加诗意表达
- 添加场景化隐喻（"像清晨的艺术馆"）

**具体改动示例（P2）**:
- Before: "情绪感是设计通过视觉传递的情感氛围"
- After: "它藏在页面打开的第一秒。\n\n是大脑在读懂文字之前，\n就已经做出的直觉判断。"

#### 步骤 5.2 结构化内容呈现（P3）
**分类清晰展示**:
- 颜色 Color → 莫兰迪色 = 宁静 高级
- 形状 Shape → 圆角 = 安全 柔软
- 留白 Space → 负空间 = 秩序 冷静

---

## 四、技术难点与解决方案

### 问题 1: 中文引号导致 JSON 渲染失败
**原因**: 使用了中文全角引号 `“”`。  
**解决**: 强制使用英文半角引号 `""`。  

### 问题 2: 大规模 JSON 编辑导致结构损坏
**症状**: JSON 解析错误。  
**解决**: 大规模重构优先使用 Python 脚本全量重建，避免局部文本替换。

### 问题 3: 视觉对齐精度问题
**解决**: 
1. 居中对齐严格遵守“三位一体”法则（见上文）。
2. 双层效果优先使用单层文本 + `shadow` effect。

### 问题 4: 物理材质感（纹理）实现公式
**解决**: 
- **结构**: `rectangle` + `image fill`。
- **混合公式**: `blendMode: "multiply"` + `opacity: 0.1~0.3`。
- **素材要求**: 必须使用高分辨率（2000px+）摄影级素材。

---

## 五、工作流程最佳实践

### 4.1 增量开发策略
1. ✅ **先完成 P1 封面验证渲染**
2. ✅ **在 P2 建立样式模板（毛玻璃+文字效果）**
3. ✅ **复制 P2 结构到 P3-P5，仅修改内容**
4. ✅ **最后统一优化呼吸感排版**

### 4.2 文件编辑策略选择表

| 操作类型 | 推荐工具 | 原因 |
|---------|---------|------|
| 单字段修改（如颜色值） | `replace_file_content` | 快速精准 |
| 单卡片内容更新 | `replace_file_content` | 目标唯一易定位 |
| 多卡片样式统一 | Python 脚本 | 避免重复操作 |
| 全量结构重构 | Python 脚本 | 保证 JSON 完整性 |
| 新增卡片 | 复制现有卡片 + 修改内容 | 保持样式一致 |

### 4.3 调试与验证流程
```bash
// turbo
# 1. 验证 JSON 格式
python3 -c "import json; json.load(open('file.pen'))"

# 2. 检查文件内容
cat file.pen | head -n 50

# 3. 使用 Pencil 渲染工具测试（如果有）
pencil render file.pen -o output.png
```

---

### 4.4 交互协议：先确认后执行
- **原则**: 涉及视觉风格调整、结构重构等主观或高风险任务时，必须先复述对需求的理解，获得确认后再执行。
- **流程**: 
  1. 用户下达模糊指令（如“更有质感一点”）
  2. Agent 分析并回复：“我的理解是增加纸张纹理的不透明度，并加深阴影以体现厚度，是否准确？”
  3. 用户确认：“是”
  4. Agent 执行代码修改

---

## 六、需求演进记录

### 版本 1: 初始需求
- 创建 5 张卡片
- 主题：情绪感
- 风格：现代、简洁

### 版本 2: 样式细化
- 引入毛玻璃效果 (glassmorphism)
- 添加双层文字阴影
- 确定黄白配色方案

### 版本 3: 排版优化
- 引入"呼吸感"概念
- 实现文本层级（70/54/42/36px）
- 使用 `gap` 控制垂直间距

### 版本 4: 内容调性
- 基于 `xiaohongshu_vibe.md` 优化文案
- 减少说教，增加诗意
- 添加场景化隐喻

### 版本 5: 细节打磨
- 解决 P1 对齐问题（双层 → shadow）
- 统一所有卡片的视觉规范
- 完成最终交付

---

## 七、可复用模板

### 卡片模板 1: 封面卡（垂直居中）
```json
{
  "layout": "vertical",
  "gap": 60,
  "padding": 80,
  "justifyContent": "center",
  "alignItems": "center",
  "children": [
    {"type": "text", "fontSize": 64, "fontWeight": "bold", "content": "主标题"},
    {"type": "frame", "children": [/* 核心内容 */]},
    {"type": "text", "fontSize": 48, "content": "底部标语"}
  ]
}
```

### 卡片模板 2: 内容卡（毛玻璃容器）
```json
{
  "type": "frame",
  "fill": "#FFFFFF1A",
  "effect": {"type": "background_blur", "radius": 40},
  "layout": "vertical",
  "gap": 40,
  "padding": 60,
  "children": [
    {"type": "text", "fontSize": 70, "fontWeight": "bold", "fill": "#FDED9EFF"},
    {"type": "text", "fontSize": 54, "fill": "#FFFFFFFF"},
    {"type": "text", "fontSize": 42, "fill": "#FDED9ECC"}
  ]
}
```

### 文字效果模板: 双层阴影
```json
{
  "type": "text",
  "effect": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#00000066",
    "offset": {"x": 2, "y": 2},
    "blur": 0
  }
}
```

---

## 八、快速检查清单

**设计阶段**:
- [ ] 所有文本使用英文半角引号
- [ ] 颜色值格式正确（#RRGGBBAA）
- [ ] 字号符合层级规范（70/54/42/36）
- [ ] 容器使用统一的 gap 和 padding

**编辑阶段**:
- [ ] 大规模修改使用 Python 脚本
- [ ] 每次修改后验证 JSON 格式
- [ ] 保持一致的视觉样式（毛玻璃/阴影）

**内容阶段**:
- [ ] 文案符合 xiaohongshu_vibe 风格
- [ ] 使用短句和换行增强可读性
- [ ] 添加场景化隐喻提升共鸣

**交付阶段**:
- [ ] 所有卡片渲染正常
- [ ] 视觉效果一致
- [ ] JSON 文件格式完整

---

## 九、底层工程原理

本 SOP 的设计逻辑对标现代软件工程的核心原则：

| 工程原则 | SOP 体现 | 设计收益 |
|---------|---------|---------|
| **分层抽象** (Layering) | 背景层 → 内容层 → 文本层 | 关注点分离，改一层不影响其他层 |
| **约定优于配置** (Convention over Config) | `layout: "none"` 才能绝对定位 | 减少隐式规则导致的错误 |
| **可组合性** (Composability) | 主题-背景色表、可复用模板 | 原子化设计 + 组件复用 |
| **防御性编程** (Defensive) | 占位框架、脚本全量重建 | 假设环境不可靠，先保证可运行 |
| **声明式范式** (Declarative) | JSON 描述"想要什么"而非"怎么画" | 可读性高、易于版本控制 |
| **版本控制思维** (VCS Mindset) | 需求演进记录 V1→V5 | 记录决策而非仅保存文件 |
| **测试验证** (Testing) | 快速检查清单、JSON 格式验证 | 每次修改后验证 = 单元测试思想 |

> 💡 **核心洞察**：这份 SOP 本质上是把**软件工程的系统性思维**应用到**设计资产管理**领域。它不仅是操作手册，更是一个**可维护、可扩展、可复用的设计系统架构文档**。

---

## 十、相关文档

- 参考样式: `/Users/bing/project/me/writer/.agent/prompts/xiaohongshu_vibe.md`
- 项目文件: `/Users/bing/project/me/writer/article/小红书/pencil/aesthetic_knowledge_cover.pen`
- 构建脚本: `/tmp/rebuild_all_cards.py`

---

**文档版本**: v1.1  
**最后更新**: 2026-01-29  
**维护说明**: 每次重大工作流程更新后，请同步更新本 SOP 文档