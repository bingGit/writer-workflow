{
  "visual_system_config": {
    "style_name": "叙事插画风 (Narrative Line & Gradient)",
    "brand_archetype": "Notion 风格线稿 x Stripe 风格色彩",
    "design_principles": {
      "clarity": "直白的叙事 (直接画出动作，不要让读者猜)",
      "humanity": "角色驱动概念 (用小人儿把抽象概念演出来)",
      "focus": "色彩即功能 (只给最关键的'道具'上渐变色，以此作为视觉焦点)"
    },
    "visual_rules": {
      "text_language": {
        "rule": "图中所有文字必须使用中文 (Simplified Chinese)",
        "reason": "确保插图与中文文章风格一致"
      },
      "background": {
        "type": "干净平面",
        "color": "纯白 (#FFFFFF) 或 极浅灰",
        "elements": "为了平衡画面，可点缀极少量的几何形状或圆点"
      },
      "style": {
        "line_art": "清晰的黑色墨水矢量线稿 (Notion 风格插画)，线条粗细变化自然",
        "characters": "风格化人物，极简五官，肢体语言丰富，专注于动作本身",
        "color_accent": "Stripe 风格的高亮渐变色 (蓝紫、青绿、暖橙)，仅用于代表解决方案或核心概念的物体上"
      }
    },
    "generation_workflow": [
      {
        "step": 1,
        "action": "视觉化具体动作：谁在做什么？ (例如：一个人正在费力地推石头)"
      },
      {
        "step": 2,
        "action": "定义'魔法道具'：什么工具代表了解决办法？ (例如：一个发光的杠杆)"
      },
      {
        "step": 3,
        "action": "应用风格：黑白的世界 + 渐变的道具"
      },
      {
        "step": 4,
        "action": "输出 Notion x Stripe 风格的 Prompt"
      }
    ],
    "prompt_template": {
      "structure": "Notion 和 Stripe 风格的扁平矢量插画。[带有角色的场景描述]。画面使用清晰的黑色墨水线稿在白色背景上绘制。[核心物体] 被涂上了鲜艳的 [颜色渐变]。干净、现代的企业插画风格，极简，清晰的叙事性。 --v 6.0"
    }
  }
}