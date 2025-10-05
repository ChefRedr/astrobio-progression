import json

seen = set()
dupes = set()

with open("llm_data.jsonl", "r") as f:
    for line in f:
        paper_id = json.loads(line)["paper_id"]
        if paper_id in seen:
            dupes.add(paper_id)
        seen.add(paper_id)

print("✅ All unique" if not dupes else f"❌ Duplicates: {dupes}")
