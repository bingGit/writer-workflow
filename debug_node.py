from moxingshu_parser import MoxingshuParser
p = MoxingshuParser()
data = p.fetch_by_article_id("694bb6d34b73450dc046d4fa")
if data and not data.startswith("Error"):
    texts = p.parse(data)
    print(f"Parsed: {len(texts)}")
    for t in texts: print(t)
