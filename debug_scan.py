import re

with open("node.bin", "rb") as f:
    data = f.read()

print(f"File size: {len(data)}")

utf8_pattern = re.compile(rb'(?:[\x20-\x7E]|[\xC2-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF4][\x80-\xBF]{3}){3,}')

for match in utf8_pattern.finditer(data):
    try:
        t = match.group().decode('utf-8')
        print(f"FOUND: {t}")
    except: pass
