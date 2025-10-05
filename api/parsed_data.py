import json
from pprint import pprint

article_content = []

with open("papers.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        # Each line is a JSON object, so we parse it separately
        article_content.append(json.loads(line))

# Now `article_content` is a list of dictionaries
# pprint(article_content[1])

#title
#keywords
#abstract

weights = [1, 1, .2]
fields = ['title', 'Keywords', 'abstract']