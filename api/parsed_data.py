import json
import re

article_content = []

with open("papers.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        # Each line is a JSON object, so we parse it separately
        article_content.append(json.loads(line))

# Now `article_content` is a list of dictionaries
keywords_data = {}

for entry in article_content:
    text = ""
    # combine text sources
    if "abstract" in entry:
        text += entry["abstract"]
    if "sections" in entry:
        for section in entry["sections"]:
            text += " " + section.get("text", "")

    match = re.search(r"[Kk]eywords?:\s*(.*)", text)
    if not match:
        entry["keywords"] = []
        continue
    raw = match.group(1).strip()
    keywords = [kw.strip() for kw in raw.split(",") if kw.strip()]

    cleaned_keywords = []

    CUTOFF_WORDS = ["introduction", "background", "methods", "©", "license", "open access","edited"]

    for kw in keywords:
        lower_kw = kw.lower()
        # Stop if it looks like the start of a normal sentence (not a keyword)
        if re.match(r"^(This|The|We|In|A|An|Our|For|To)\b", kw):
            break
        if any(cutoff in lower_kw for cutoff in CUTOFF_WORDS):
            break
        # Stop if the fragment clearly continues into a sentence
        if re.search(r"[.!?]", kw):
            break
        cleaned_keywords.append(kw)

    entry["keywords"] = cleaned_keywords

#title
#keywords
#abstract

weights = [1, 1, .2]
fields = ['title', 'Keywords', 'abstract']

counts = [len(e["keywords"]) for e in article_content]
print(f"Min keywords: {min(counts)}, Max keywords: {max(counts)}, Avg: {sum(counts)/len(counts):.2f}")

# Preview a few
for entry in article_content[11:20]:
    print(f"\nTitle: {entry.get('title')}")
    print("Keywords:", entry["keywords"])