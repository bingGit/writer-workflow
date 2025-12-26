from moxingshu_parser import MoxingshuParser
p = MoxingshuParser()
text = "A黑色/深色线条： 就像给内容加了一个“牢笼”，"
cleaned = p._deep_clean(text)
print(f"Original: {text}")
print(f"Cleaned: {cleaned}")
valid = p._is_valid_text(cleaned)
print(f"Valid: {valid}")
