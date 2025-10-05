import json
from pprint import pprint

data = []

with open("papers.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        # Each line is a JSON object, so we parse it separately
        data.append(json.loads(line))

# Now `data` is a list of dictionaries
pprint(data[1])

#title
#keywords 
#abstract

weights = [1, 1, .2]
fields = ['title', 'Keywords', 'abstract']