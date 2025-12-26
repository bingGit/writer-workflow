import base64
import sys
import re
import urllib.request
import urllib.error
import json
import os
import time
import random

class MoxingshuParser:
    def __init__(self):
        self.ignored_keywords = {
            "type", "paragraph", "text", "style", "color", "background", 
            "backgroundcolor", "fontcolor", "null", "content", "bold", "italic",
            "underline", "align", "center", "left", "right", "justify",
            "true", "false", "width", "height", "solid", "border", "radius",
            "padding", "margin", "font", "fontsize", "fontweight", "lineheight",
            "opacity", "zindex", "display", "flex", "none", "hidden", "visible",
            "start", "level", "version", "editorversion", "static"
        }
        self.color_pattern = re.compile(r'^#[0-9a-fA-F]{3,8}$')
        # 垃圾字符黑名单 (包含 Protobuf 常见的干扰符)
        self.garbage_chars = {"Ă", "ă", "ƾ", "ƅ", "Ҙ", "%", "$"}

    def fetch_by_article_id(self, article_id):
        url = f"https://next-yjs.moxingshu.cn/v1/file/get?articleId={article_id}"
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://www.moxingshu.cn",
            "referer": "https://www.moxingshu.cn/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        if os.path.exists("token.txt"):
            try:
                with open("token.txt", "r", encoding="utf-8") as f:
                    token = f.read().strip()
                    if token: headers["mindmap_token"] = token
            except Exception: pass
        if os.path.exists("cookie.txt"):
            try:
                with open("cookie.txt", "r", encoding="utf-8") as f:
                    cookie_content = f.read().strip()
                    if cookie_content: headers["Cookie"] = cookie_content
            except Exception: pass
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                raw_response = response.read().decode('utf-8')
                json_data = json.loads(raw_response)
                if json_data.get("code") == 0:
                    return json_data.get("data", {}).get("buffer", "")
                return f"Error: API {json_data.get('code')}"
        except Exception as e: return f"Error: {str(e)}"

    def fetch_article_list(self, output_file="article_list.json"):
        url = "https://api.moxingshu.com.cn/api/Article/ArticleList"
        headers = {"user-agent": "Mozilla/5.0", "referer": "https://www.moxingshu.cn/"}
        if os.path.exists("token.txt"):
            with open("token.txt", "r") as f: headers["mindmap_token"] = f.read().strip()
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return "✅ Saved"
        except Exception as e: return str(e)

    def export_hierarchy(self, query, with_details=False):
        json_file = "article_list.json"
        if not os.path.exists(json_file): self.fetch_article_list(json_file)
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data_list = json.load(f).get("data", [])
        except: return "Error loading json"
        
        id_map = {n["id"]: n for n in data_list}
        children_map = {}
        for n in data_list:
            pid = n.get("parentId")
            if pid not in children_map: children_map[pid] = []
            children_map[pid].append(n)
        for pid in children_map: children_map[pid].sort(key=lambda x: x.get("sort", 0))

        root_node = id_map.get(query) or next((n for n in data_list if n.get("title") == query), None)
        if not root_node: return f"Not found: {query}"

        output_lines = [f"# {root_node['title']} - 导图结构\n"]
        
        output_dir = "parse_result"
        if not os.path.exists(output_dir): os.makedirs(output_dir)

        def traverse(node, level):
            indent = "  " * (level - 1)
            title = node.get("title", "").replace("\n", " ")
            output_lines.append(f"{indent}- {title}")
            
            if with_details:
                time.sleep(random.uniform(0.3, 0.8)) # 稍微加快一点
                raw = self.fetch_by_article_id(node["id"])
                if raw and not raw.startswith("Error"):
                    texts = self.parse(raw)
                    seen_texts = set()
                    for t in texts:
                        # 再次去重与过滤
                        t_clean = t.strip()
                        if not t_clean: continue
                        if t_clean == title.strip(): continue
                        if t_clean in seen_texts: continue
                        
                        output_lines.append(f"{indent}  > {t_clean}")
                        seen_texts.add(t_clean)

            for child in children_map.get(node["id"], []):
                traverse(child, level + 1)

        traverse(root_node, 1)
        
        safe_title = root_node['title'].replace("/", "_").replace("\\", "_")
        suffix = "_details" if with_details else ""
        filename = os.path.join(output_dir, f"{safe_title}{suffix}.md")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        return f"✅ Done: {filename}"

    def _read_varint(self, data, offset):
        value, shift = 0, 0
        while offset < len(data):
            byte = data[offset]
            offset += 1
            value |= (byte & 0x7f) << shift
            if not (byte & 0x80): return value, offset
            shift += 7
        return None, offset

    def parse(self, base64_content):
        try: binary_data = base64.b64decode(base64_content)
        except: return []
        
        extracted_items = []
        
        # 使用正则直接匹配二进制中的 UTF-8 字符串
        # 范围包括：ASCII 可见字符 (0x20-0x7E) 和 常见 UTF-8 多字节序列
        # 排除控制字符，至少连续 3 个字节
        utf8_pattern = re.compile(rb'(?:[\x20-\x7E]|[\xC2-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF4][\x80-\xBF]{3}){3,}')
        
        for match in utf8_pattern.finditer(binary_data):
            try:
                raw_text = match.group().decode('utf-8')
                start_pos = match.start()
                end_pos = match.end()
                
                # 核心清洗步骤
                clean_text = self._deep_clean(raw_text)
                
                if self._is_valid_text(clean_text):
                    extracted_items.append({
                        'text': clean_text,
                        'start': start_pos,
                        'end': end_pos
                    })
            except: pass

        # 依然使用碎片合并逻辑，因为正则可能会把一句话中间的特殊符号断开
        return self._post_process_merge(extracted_items)

    def _post_process_merge(self, items):
        if not items: return []
        items.sort(key=lambda x: x['start'])
        
        merged = []
        current = items[0]
        
        for next_item in items[1:]:
            gap = next_item['start'] - current['end']
            
            # 放宽合并条件：对于正则匹配，gap 可能会稍微大一点（跳过乱码）
            # 或者 gap 为 0 (紧邻)
            if 0 <= gap < 100:
                # 拼接时加一个空格缓冲，或者是直接拼？
                # 对于中文，直接拼。对于英文，可能需要空格。
                # 简单起见，直接拼，依赖后续肉眼或 _deep_clean
                current['text'] += next_item['text']
                current['end'] = next_item['end']
            else:
                merged.append(current)
                current = next_item
        
        merged.append(current)
        
        # 最终去重清洗
        final_texts = []
        seen = set()
        for item in merged:
            t = self._deep_clean(item['text'])
            if self._is_valid_text(t) and t not in seen:
                final_texts.append(t)
                seen.add(t)
        return final_texts

    def _deep_clean(self, text):
        # 1. 保留可见字符
        text = "".join(c for c in text if c.isprintable() or c in "\n\r\t")
        text = text.strip()
        
        # 2. 去除特定的垃圾符号
        for garbage in self.garbage_chars:
            text = text.replace(garbage, "")
        
        # 3. 去除行首奇怪的修饰符 (如 "$", "*", "=", "r" 等如果后面紧跟中文)
        # 例如: "$。这种强对比" -> "。这种强对比"
        # 匹配模式：行首1-2个非中文字符，后面跟着中文
        match = re.match(r'^([^a-zA-Z0-9\u4e00-\u9fff\s]{1,2})([\u4e00-\u9fff].*)', text)
        if match:
            text = match.group(2)
        
        # 4. 去除奇怪的字母前缀 (如 "r使用" -> "使用", "Up淡金色" -> "淡金色")
        # 匹配模式：行首1-3个英文字母，后面跟着中文
        match = re.match(r'^([a-zA-Z]{1,3})([\u4e00-\u9fff].*)', text)
        if match:
             text = match.group(2)
             
        return text.strip()

    def _is_valid_text(self, text):
        if not text or len(text) < 2: return False
        
        lt = text.lower()
        
        # 1. 样式代码强过滤
        # 如果包含 backgroundcolor, rgb, 等
        if "backgroundcolor" in lt or "fontcolor" in lt: return False
        if "rgb(" in lt or "rgba(" in lt: return False
        
        # 2. 关键词黑名单
        if lt in self.ignored_keywords: return False
        
        # 3. 颜色/CSS
        clean = text.replace('"', '').replace("'", "").strip()
        # 只要包含颜色代码开头，就认为是颜色（处理后面跟乱码的情况）
        if re.match(r'^#[0-9a-fA-F]{3,8}', clean) or clean.startswith("rgb"): return False
        
        # 增强：过滤样式堆砌字符串 (如 "#f4e6b9"null"#3C373B")
        if "#" in text and ("null" in lt or text.count("#") > 1):
             return False
        
        # 过滤纯 null 或重复的 null
        if lt.replace("null", "").strip() == "":
             return False

        # 4. 纯英文过滤 (更严格)
        is_ascii = all(ord(c) < 128 for c in text)
        if is_ascii:
            # 必须包含空格才算句子，除非是很长的单词 (如 backdrop-filter)
            if " " not in text and len(text) < 12: return False
            # 必须包含字母或数字
            if not re.search(r'[a-zA-Z0-9]', text): return False
            # 如果全是符号
            if not any(c.isalnum() for c in text): return False
            
        # 5. 垃圾短语过滤
        if text in ["(Ă", "L(Ă", "J(Ă"]:
            return False

        return True

if __name__ == "__main__":
    parser = MoxingshuParser()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'list': print(parser.fetch_article_list())
        elif sys.argv[1] == 'export': print(parser.export_hierarchy(sys.argv[2], "--details" in sys.argv))
        else:
            res = parser.parse(sys.argv[1])
            for r in res: print(f"- {r}")