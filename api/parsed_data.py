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
    if match:
        raw = match.group(1).strip()
        keywords = [kw.strip() for kw in raw.split(",") if kw.strip()]
    else:
        # no keywords found in the combined text; continue with empty list
        keywords = []

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

    # Extract paragraph-sized text pieces into a simple list of strings.
    # Collect from abstract_paragraphs (if present) and from sections.
    paragraphs = []
    # abstract_paragraphs: list of dicts with 'text'
    if "abstract_paragraphs" in entry and isinstance(entry["abstract_paragraphs"], list):
        for p in entry["abstract_paragraphs"]:
            if isinstance(p, dict) and "text" in p and p["text"]:
                txt = p["text"].strip()
                if txt:
                    paragraphs.append(txt)

    # sections may contain 'paragraphs' (list of dicts with 'text') or a 'text' field
    if "sections" in entry and isinstance(entry["sections"], list):
        for sec in entry["sections"]:
            if not isinstance(sec, dict):
                continue
            # section-level textual blob
            if "text" in sec and isinstance(sec["text"], str):
                txt = sec["text"].strip()
                if txt:
                    paragraphs.append(txt)

            # section paragraphs (preferred if present)
            if "paragraphs" in sec and isinstance(sec["paragraphs"], list):
                for p in sec["paragraphs"]:
                    if isinstance(p, dict) and "text" in p and p["text"]:
                        txt = p["text"].strip()
                        if txt:
                            paragraphs.append(txt)

    # set the extracted paragraphs on the entry (list of strings)
    entry["paragraphs"] = paragraphs

#title
#keywords
#abstract

counts = [len(e["keywords"]) for e in article_content]
print(f"Min keywords: {min(counts)}, Max keywords: {max(counts)}, Avg: {sum(counts)/len(counts):.2f}")

# Preview a few
for entry in article_content[11:15]:
    print(f"\nTitle: {entry.get('title')}")
    print("Keywords:", entry["keywords"])
    print("Paragraph count:", len(entry["paragraphs"]))

# num_paragraphs = 0
# paragarphs_below_x = 0
# for entry in article_content:
#     num_par = len(entry['paragraphs'])
#     num_paragraphs += num_par
#     if num_par < 10:
#         paragarphs_below_x += 1

# num_paragraphs /= len(article_content)
# print(f'average number of paragraphs: {num_paragraphs}')
# print(f'paragraphs below x is: {paragarphs_below_x}')