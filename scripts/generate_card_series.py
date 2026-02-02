
import json
import os
import random
import string

# ================= Configuration =================
OUTPUT_DIR = "article/小红书/pencil"
PROJECT_NAME = "inverted_vision"
BG_COLOR = "#7B7291" # Morandi Purple-Grey (Introspection/Mystery)

# ================= Card Data (Content + Metaphor) =================
# This data drives both the JSON structure and the Image Prompts
CARDS_DATA = [
    {
        "id": "P1",
        "type": "cover",
        "title": "倒着看世界",
        "subtitle": "真正的视觉不需要翻译",
        "content": "一个关于视觉觉醒的测试",
        "annotation": "Aesthetic Awakening",
        "metaphor": {
            "subject": "A solitary wooden park bench floating upside down",
            "action": "dissolving into abstract geometric lines",
            "symbol": "Inverted gravity field",
            "composition": "Center aligned, minimalist photography, surreal atmosphere, high negative space",
            "accent_color": "Warm Sunlight"
        }
    },
    {
        "id": "P2",
        "type": "content",
        "title": "💭 视觉困惑",
        "content": "为什么照片总觉得差点意思？\n\n脑补了一万字故事，\n去掉故事就索然无味。",
        "annotation": "Concept vs Form",
        "metaphor": {
            "subject": "A blurry figure grasping at fog",
            "action": "struggling to see clearly",
            "symbol": "Mist and shadows",
            "composition": "Asymmetrical",
            "accent_color": "Pale Yellow"
        }
    },
    {
        "id": "P3",
        "type": "content",
        "title": "🧠 视觉翻译",
        "content": "我们在看世界时，\n大脑自动挂载字幕。\n\n你以为看的是照片，\n其实看的是联想。",
        "annotation": "Mental Subtitles",
        "metaphor": {
            "subject": "Glasses with text overlay",
            "action": "filtering reality",
            "symbol": "Letters floating in air",
            "composition": "Layered depth",
            "accent_color": "Cyan Grey"
        }
    },
    {
        "id": "P4",
        "type": "content",
        "title": "🛡️ 生存本能",
        "content": "大脑只关心“是什么”\n（老人=安全/危险？）\n\n为了读懂意义，\n我们牺牲了感知。",
        "annotation": "Evolutionary Filter",
        "metaphor": {
            "subject": "Wireframe of a predator",
            "action": "fading into abstraction",
            "symbol": "Geometric simplification",
            "composition": "High contrast",
            "accent_color": "Brick Red"
        }
    },
    {
        "id": "P5",
        "type": "content",
        "title": "🌱 倒转实验",
        "content": "试着把手机倒过来。\n如果情绪还在，\n那是视觉的力量。\n\n一场反抗大脑惯性的起义。",
        "annotation": "Rebellion against Inertia",
        "metaphor": {
            "subject": "An upside down world",
            "action": "revealing hidden structure",
            "symbol": "Light beams",
            "composition": "Balanced reversal",
            "accent_color": "Emerald Green"
        }
    }
]

def generate_id(length=5):
    """Generates a random ID for Pencil objects."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# ================= Templates =================
def build_pencil_json(cards):
    """Constructs the .pen JSON structure."""
    
    # Root children are the logical "Pages", laid out side-by-side
    root_children = []
    
    start_x = 0
    CARD_WIDTH = 1080
    CARD_HEIGHT = 1440
    GAP = 200
    
    for i, card in enumerate(cards):
        # Calculate position
        pos_x = start_x + (i * (CARD_WIDTH + GAP))
        
        # 1. Background Layer
        bg = {
            "type": "rectangle",
            "id": generate_id(),
            "name": "Background",
            "x": 0, "y": 0,
            "width": CARD_WIDTH,
            "height": CARD_HEIGHT,
            "fill": BG_COLOR,
            "layout": "none"
        }
        
        # Texture Layer
        texture_layer = {
            "type": "rectangle",
            "id": generate_id(),
            "name": "Texture",
            "x": 0, "y": 0,
            "width": CARD_WIDTH,
            "height": CARD_HEIGHT,
            "fill": {
                "type": "image",
                "opacity": 0.5,
                "enabled": True,
                "url": "gray_texture.png",
                "mode": "fill",
                "blendMode": "multiply"
            },
            "layout": "none"
        }
        
        # Custom Layout for Cover (P1)
        if card['type'] == 'cover':
            # 1. Top Fixed Title
            root_children.append({
                "type": "frame", "id": generate_id(),
                "name": f"{card['id']}: {card['title']}",
                "x": pos_x, "y": 0, "width": CARD_WIDTH, "height": CARD_HEIGHT,
                "fill": BG_COLOR, "layout": "none",
                "children": [
                    bg,
                    texture_layer,
                    # Top Label
                    {"type": "text", "id": generate_id(), "x": 0, "y": 71, "width": 1080, "height": 91, 
                     "content": "每天一个审美知识", "fill": "#FFFFFFFF", "textAlign": "center", "textGrowth": "fixed-width-height",
                     "fontFamily": "Inter", "fontSize": 64, "fontWeight": "bold", "letterSpacing": 10},
                    # English Subtitle
                    {"type": "text", "id": generate_id(), "x": 0, "y": 162, "width": 1080, "height": 51,
                     "content": "A little Aesthetic every day", "fill": "#FFFFFFCC", "textAlign": "center", "textGrowth": "fixed-width-height",
                     "fontFamily": "Georgia", "fontSize": 36, "fontStyle": "italic", "letterSpacing": 2},
                     # Main Title (Huge)
                    {"type": "text", "id": generate_id(), "x": 0, "y": 280, "width": 1080, "height": 200,
                     "content": card['title'], "fill": "#FCE492", "textAlign": "center", "textGrowth": "fixed-width-height",
                     "fontFamily": "Inter", "fontSize": 140, "fontWeight": "900",
                     "effect": {"type": "shadow", "shadowType": "outer", "color": "#FCE49226", "offset": {"x": 0, "y": 2}, "blur": 8}},
                     # Central Image Placeholder
                    {"type": "frame", "id": generate_id(), "name": "p1img", "x": 340, "y": 520, "width": 400, "height": 600,
                     "fill": {"type": "image", "enabled": True, "url": "inverted_vision.png", "mode": "fill"},
                     "effect": {"type": "background_blur", "radius": 20}},
                     # Bottom Content
                    {"type": "text", "id": generate_id(), "x": 0, "y": 1207, "width": 1080, "height": 120,
                     "content": f"{card['subtitle']}\n{card['content']}", "fill": "#FFFFFFFF", "textAlign": "center", "textGrowth": "fixed-width-height",
                     "fontFamily": "Inter", "fontSize": 48, "lineHeight": 1.5, "letterSpacing": 2}
                ]
            })
            continue

        # Standard Layout for Content Cards (P2-P5)
        
        # 2. Card Content Components
        card_content = []
        
        # Title
        card_content.append({
            "type": "text", "id": generate_id(), 
            "fontSize": 70, "fontWeight": "bold", 
            "fontFamily": "Inter",
            "content": card['title'], 
            "fill": "#FDED9EFF",
            "effect": {"type": "shadow", "shadowType": "outer", "color": "#00000066", "offset": {"x": 2, "y": 2}}
        })
        
        # Main Content
        card_content.append({
            "type": "text", "id": generate_id(),
            "fontSize": 54, "fontWeight": "bold", 
            "fontFamily": "Inter",
            "lineHeight": 1.5,
            "content": card['content'], 
            "fill": "#FFFFFFFF",
            "effect": {"type": "shadow", "shadowType": "outer", "color": "#00000066", "offset": {"x": 2, "y": 2}}
        })
        
        # Subtitle/Annotation
        if 'subtitle' in card:
             card_content.append({
                 "type": "text", "id": generate_id(),
                 "fontSize": 42, "fontFamily": "Inter",
                 "content": card['subtitle'], 
                 "fill": "#FDED9ECC"
             })
        if 'annotation' in card:
             card_content.append({
                 "type": "text", "id": generate_id(),
                 "fontSize": 36, "fontStyle": "italic", "fontFamily": "Inter",
                 "content": card['annotation'], 
                 "fill": "#FFFFFF99"
             })

        # Content Frame
        container = {
            "type": "frame",
            "id": generate_id(),
            "name": "ContentContainer",
            "x": 80, # Margin
            "y": 300, # Top Offset
            "width": 920, # 1080 - 80*2
            "height": 840, # Arbitrary based on reference
            "fill": "#FFFFFF1A", # Glassmorphism
            "cornerRadius": 40,
            "effect": {"type": "background_blur", "radius": 40},
            "layout": "vertical",
            "gap": 40,
            "padding": 60,
            "justifyContent": "center" if card['type'] == 'cover' else "flex-start",
            "children": card_content
        }
        
        # Top Level Frame for the Card
        card_frame = {
            "type": "frame",
            "id": generate_id(),
            "name": f"{card['id']}: {card['title']}",
            "x": pos_x,
            "y": 0,
            "width": CARD_WIDTH,
            "height": CARD_HEIGHT,
            "fill": BG_COLOR,
            "layout": "none", # Absolute positioning for background and container
            "children": [bg, texture_layer, container]
        }
        
        root_children.append(card_frame)

    return {
        "version": "2.6",
        "children": root_children
    }

def build_image_prompt(card, bg_color):
    """Generates the prompt string."""
    m = card['metaphor']
    return f"""
[Card {card['id']}]
Prompt: Flat design, Minimalist illustration, Hand-drawn texture, {bg_color} background (Morandi), {m['subject']}, {m['action']}, {m['symbol']}, {m['accent_color']} accent, clean lines, {m['composition']} --no text, realistic, 3d, high resolution
"""

# ================= Main Execution =================
if __name__ == "__main__":
    # 1. Generate JSON content
    pen_data = build_pencil_json(CARDS_DATA)
    
    # 2. Generate Prompts content
    prompts_content = f"# Image Prompts for {PROJECT_NAME}\n# Style: Flat/Minimalist | Color: {BG_COLOR}\n"
    for card in CARDS_DATA:
        prompts_content += build_image_prompt(card, BG_COLOR)
        
    # 3. Write Files
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    json_path = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.pen")
    prompts_path = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}_prompts.txt")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(pen_data, f, ensure_ascii=False, indent=2)
        
    with open(prompts_path, 'w', encoding='utf-8') as f:
        f.write(prompts_content)
        
    print(f"✅ Generated Pencil File: {json_path}")
    print(f"✅ Generated Prompts File: {prompts_path}")
