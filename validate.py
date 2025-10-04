import json

with open('papers.jsonl', 'r', encoding='utf-8') as f:
    total = 0
    valid = 0
    errors = []
    
    for line in f:
        total += 1
        try:
            data = json.loads(line)
            required = ['paper_id', 'source_url', 'metadata', 'sections']
            missing = [k for k in required if k not in data]
            if missing:
                errors.append(f"Line {total}: missing {missing}")
            else:
                valid += 1
        except json.JSONDecodeError as e:
            errors.append(f"Line {total}: invalid JSON - {e}")
    
    print(f"Total: {total} | Valid: {valid} | Invalid: {total - valid}")
    if errors:
        print("\nErrors:")
        for err in errors[:10]:
            print(err)