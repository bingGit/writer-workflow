import json
import os

def create_note_card(id_prefix, x, y, title, author, likes, image_url):
    """创建单一笔记卡片组件"""
    return {
        "type": "frame",
        "id": f"note-{id_prefix}",
        "x": x,
        "y": y,
        "width": 510, # 1080 / 2 - gap/2
        "fill": "#FFFFFF",
        "cornerRadius": 24,
        "clip": True,
        "layout": "vertical",
        "effect": {
            "type": "shadow",
            "shadowType": "outer",
            "color": "#0000000D",
            "offset": {"x": 0, "y": 4},
            "blur": 12
        },
        "children": [
            # 封面图
            {
                "type": "rectangle",
                "id": f"img-{id_prefix}",
                "width": "fill_container",
                "height": 600,
                "fill": {
                    "type": "image",
                    "enabled": True,
                    "url": image_url,
                    "mode": "fill"
                }
            },
            # 文本内容容器
            {
                "type": "frame",
                "id": f"text-cont-{id_prefix}",
                "width": "fill_container",
                "padding": 24,
                "layout": "vertical",
                "gap": 16,
                "children": [
                    {
                        "type": "text",
                        "id": f"title-{id_prefix}",
                        "content": title,
                        "fontSize": 28,
                        "fontWeight": "semibold",
                        "fill": "#000000",
                        "textGrowth": "fixed-width",
                        "width": "fill_container"
                    },
                    {
                        "type": "frame",
                        "id": f"author-cont-{id_prefix}",
                        "width": "fill_container",
                        "layout": "horizontal",
                        "justifyContent": "space_between",
                        "alignItems": "center",
                        "children": [
                            {
                                "type": "frame",
                                "layout": "horizontal",
                                "gap": 8,
                                "alignItems": "center",
                                "children": [
                                    {"type": "rectangle", "width": 32, "height": 32, "cornerRadius": 16, "fill": "#E0E0E0"}, # Avatar placeholder
                                    {"type": "text", "content": author, "fontSize": 22, "fill": "#666666"}
                                ]
                            },
                            {
                                "type": "frame",
                                "layout": "horizontal",
                                "gap": 4,
                                "alignItems": "center",
                                "children": [
                                    {"type": "text", "content": "❤️", "fontSize": 20},
                                    {"type": "text", "content": str(likes), "fontSize": 22, "fill": "#999999"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

def generate_xiaohongshu_home():
    # 基础配置
    width = 1080
    height = 2400
    gap = 20
    padding = 20

    # 模拟数据
    notes = [
        {"title": "终于找到了！成都最好拍的机位📷", "author": "摄影师阿强", "likes": 1205, "image": "https://images.unsplash.com/photo-1542332213-9b5a5a3fad35?q=80&w=2070&auto=format&fit=crop"},
        {"title": "极简主义者的书房长什么样？🌿", "author": "家居美学", "likes": 583, "image": "https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?q=80&w=2067&auto=format&fit=crop"},
        {"title": "拒绝路人感！这套搭配我能穿一整年", "author": "穿搭博主子", "likes": 2341, "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1920&auto=format&fit=crop"},
        {"title": "深夜食堂 | 这一碗螺蛳粉治愈了所有人", "author": "美食探店王", "likes": 892, "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?q=80&w=1974&auto=format&fit=crop"},
    ]

    # 页面结构
    pen_data = {
        "version": "2.6",
        "children": [
            {
                "type": "frame",
                "id": "xhs-home",
                "name": "Xiaohongshu Home",
                "width": width,
                "height": height,
                "fill": "#F5F5F5",
                "clip": True,
                "layout": "none",
                "children": [
                    # 顶部导航栏 (Glassmorphism)
                    {
                        "type": "frame",
                        "id": "top-nav",
                        "x": 0, "y": 0, "width": width, "height": 180,
                        "fill": "#FFFFFFCC",
                        "effect": {"type": "background_blur", "radius": 40},
                        "layout": "none",
                        "children": [
                            {"type": "text", "x": 80, "y": 100, "content": "关注", "fontSize": 32, "fill": "#999999"},
                            {"type": "text", "x": 200, "y": 95, "content": "发现", "fontSize": 36, "fontWeight": "bold", "fill": "#000000"},
                            {"type": "text", "x": 320, "y": 100, "content": "成都", "fontSize": 32, "fill": "#999999"},
                            {"type": "rectangle", "x": 200, "y": 145, "width": 64, "height": 6, "cornerRadius": 3, "fill": "#FF2442"}, # 下划线
                            {"type": "text", "x": 920, "y": 100, "content": "🔍", "fontSize": 40}
                        ]
                    },
                    # 瀑布流容器
                    {
                        "type": "frame",
                        "id": "content-area",
                        "x": padding, "y": 200,
                        "width": width - padding * 2,
                        "height": height - 380,
                        "layout": "none",
                        "children": []
                    },
                    # 底部标签栏
                    {
                        "type": "frame",
                        "id": "bottom-bar",
                        "x": 0, "y": height - 160, "width": width, "height": 160,
                        "fill": "#FFFFFF",
                        "layout": "horizontal",
                        "justifyContent": "space_around",
                        "alignItems": "center",
                        "padding": 20,
                        "children": [
                            {"type": "text", "content": "首页", "fontSize": 32, "fontWeight": "bold", "fill": "#000000"},
                            {"type": "text", "content": "视频", "fontSize": 32, "fill": "#999999"},
                            {"type": "rectangle", "width": 100, "height": 60, "cornerRadius": 16, "fill": "#FF2442", "layout": "none", "children": [{"type": "text", "x": 38, "y": 5, "content": "+", "fontSize": 40, "fill": "#FFFFFF"}]},
                            {"type": "text", "content": "消息", "fontSize": 32, "fill": "#999999"},
                            {"type": "text", "content": "我", "fontSize": 32, "fill": "#999999"}
                        ]
                    }
                ]
            }
        ]
    }

    # 填充笔记卡片 (简单排列 2 列)
    col_width = (width - padding * 2 - gap) / 2
    for i, note in enumerate(notes):
        col = i % 2
        row = i // 2
        x = col * (col_width + gap)
        y = row * 820 # 卡片预估高度
        card = create_note_card(f"note-{i}", x, y, note['title'], note['author'], note['likes'], note['image'])
        pen_data["children"][0]["children"][1]["children"].append(card)

    # 保存文件
    output_path = "/Users/bing/project/me/writer/article/小红书/pencil/xiaohongshu_home.pen"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pen_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_xiaohongshu_home()
