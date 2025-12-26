# 模型树 (Moxingshu) 解析与导出工具

这是一个专门用于解析“模型树”平台数据的命令行工具。它可以将复杂的 Protobuf 二进制数据转化为结构清晰、纯净的 Markdown 文档，并支持全量层级导出。

## 🚀 核心功能

- **全量列表拉取**：同步云端所有节点信息并缓存到本地。
- **层级导图导出**：根据标题或 ID 递归导出完整的树状结构。
- **详情自动提取**：自动请求各节点详情，并以引用块（`> `）形式插入。
- **智能数据清洗**：自动剔除 Protobuf 干扰字符、样式属性（颜色、字号）、ID 标记等噪声。
- **安全抓取模式**：内置随机延迟，模拟人工点击，保护账号安全。

## 🛠️ 环境准备

- Python 3.x
- 无需安装第三方库（仅使用标准库：`urllib`, `base64`, `json`, `re` 等）

## ⚙️ 配置说明

在运行脚本前，请确保在根目录下创建以下鉴权文件（可通过浏览器开发者工具获取）：

1.  **`token.txt`**: 填入 `mindmap_token` 的值（推荐）。
2.  **`cookie.txt`**: 填入 `Cookie` 字段的值（可选，作为补充）。

## 📖 使用指南

### 1. 同步全量节点列表
在使用导出功能前，建议先同步本地缓存：
```bash
python3 moxingshu_parser.py list
```
成功后会生成 `article_list.json`。

### 2. 导出层级导图
通过节点标题导出：
```bash
python3 moxingshu_parser.py export "我的节点标题"
```

### 3. 导出包含详情的完整文档
开启 `--details` 模式后，脚本会逐个请求子节点的详细文字内容：
```bash
python3 moxingshu_parser.py export "毛玻璃效果" --details
```
*生成的文档将存储在 `parse_result/` 目录下。*

### 4. 直接解析 Base64 字符串
如果你有一段原始的 Base64 编码数据，可以直接解析：
```bash
python3 moxingshu_parser.py "Ax2zr874CQAAA..."
```

## 📂 目录结构

- `moxingshu_parser.py`: 主程序脚本。
- `parse_result/`: 导出的 Markdown 文件存放处。
- `article_list.json`: 节点列表缓存。
- `token.txt`: 存放鉴权 Token。
- `GEMINI.md`: AI 上下文配置文件。

## ⚠️ 注意事项

- 开启 `--details` 导出时，由于包含网络请求和随机延迟，耗时较长属于正常现象。
- 如果遇到 `401 Unauthorized` 错误，请更新 `token.txt` 中的内容。
