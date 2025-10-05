import json
import re

article_content = []

with open("papers.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        # Each line is a JSON object, so we parse it separately
        article_content.append(json.loads(line))

# Deduplicate by paper_id and sanitize to ensure ChromaDB-compatible unique IDs
seen_ids = set()
deduplicated = []

def sanitize_id(raw_id: str) -> str:
    """Sanitize ID to be ChromaDB-compatible: [a-zA-Z0-9._-], 3-512 chars, start/end with alphanumeric."""
    # Replace invalid chars with underscore
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', raw_id)
    # Remove leading/trailing non-alphanumeric
    safe = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', safe)
    # Limit length to 512
    safe = safe[:512]
    # Ensure minimum 3 chars
    if len(safe) < 3:
        safe = safe + '_id'
    return safe

for entry in article_content:
    # ONLY use paper_id field for deduplication
    entry_id = entry.get("paper_id")
    
    # Skip entries without paper_id
    if entry_id is None or entry_id == "":
        continue
    
    # Convert to string and sanitize
    raw_id = str(entry_id)
    sanitized_id = sanitize_id(raw_id)
    
    # If sanitized ID collides, append counter to make it unique
    if sanitized_id in seen_ids:
        counter = 1
        while f"{sanitized_id}_{counter}" in seen_ids:
            counter += 1
        sanitized_id = f"{sanitized_id}_{counter}"
    
    seen_ids.add(sanitized_id)
    
    # Store the sanitized ID back in the entry
    entry["paper_id"] = sanitized_id
    deduplicated.append(entry)

article_content = deduplicated
print(f"Loaded {len(article_content)} unique articles by paper_id (dropped {len(seen_ids) - len(article_content)} duplicates).")

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

    # store keywords as a single comma-separated string (empty string if none)
    entry["keywords"] = ", ".join(cleaned_keywords)

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

# Verify all paper_ids are unique
all_ids = [e.get("paper_id") for e in article_content]
assert len(all_ids) == len(set(all_ids)), "ERROR: Duplicate paper_ids found after processing!"
print(f"✓ All {len(all_ids)} paper_ids are unique and ChromaDB-compatible")

counts = [len(e.get("keywords", "").split(", ")) if e.get("keywords") else 0 for e in article_content]
print(f"Min keywords: {min(counts)}, Max keywords: {max(counts)}, Avg: {sum(counts)/len(counts):.2f}")

# Preview a few
# for entry in article_content[11:15]:
#     print(f"\nTitle: {entry.get('title')}")
#     print("Keywords:", entry["keywords"])
#     print("Paragraph count:", len(entry["paragraphs"]))

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