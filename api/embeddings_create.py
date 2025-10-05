import numpy as np
import chromadb
from chromadb.api.client import Client
from typing import Optional
import os
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import sys
from relevance_score import computeProgress
from parsed_data import weights, article_content

sys.path.insert(0, '..')

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT") or 8000)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
client = chromadb.PersistentClient(path='./chroma/')

# number of relevant articles to retrieve for comparison
N = 30

dummy_docs = [
    "A group of vibrant parrots chatter loudly, sharing stories of their tropical adventures.",
    "The mathematician found solace in numbers, deciphering the hidden patterns of the universe.",
    "The robot, with its intricate circuitry and precise movements, assembles the devices swiftly.",
    "The chef, with a sprinkle of spices and a dash of love, creates culinary masterpieces.",
    "The ancient tree, with its gnarled branches and deep roots, whispers secrets of the past.",
    "The detective, with keen observation and logical reasoning, unravels the intricate web of clues.",
    "The sunset paints the sky with shades of orange, pink, and purple, reflecting on the calm sea.",
    "In the dense forest, the howl of a lone wolf echoes, blending with the symphony of the night.",
    "The dancer, with graceful moves and expressive gestures, tells a story without uttering a word.",
    "In the quantum realm, particles flicker in and out of existence, dancing to the tunes of probability."   
]

def create_embeddings(documents: list[str], collection_name: str) -> Optional[Client]:
    ids = list(map(lambda i_x: f"id{i_x[0]}_{i_x[1][:5]}", enumerate(documents)))
    vectors = openai_ef(documents)

    collection = client.create_collection(name=collection_name)
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=vectors
    )

def match_embeddings(query: str, collection_name: str, conditions: dict):
    matches = client.get_collection(name=collection_name).query(
        query_embeddings=openai_ef([query]),
        n_results=N,
    )
    return matches

def run_pipeline(query: str):
    matches = match_embeddings(query=query, collection_name=query, conditions={})

    assert "ids" in matches.keys() and "documents" in matches.keys()

    docs = matches["documents"]
    progresses = np.array([np.float64(computeProgress(doc, query)) for doc in docs])
    return np.average(progresses)

def main():
    # possible collection names
    collection_names = ["article_titles", "article_keywords", "article_abstract", "article_paragraphs"]

    ids = [article['paper_id'] for article in article_content]
    # check keys are unique identifier
    assert len(set(ids)) == len(ids)
    
    titles = [article['title'] for article in article_content]
    keywords = [article['Keywords'] for article in article_content]

    assert len(titles) == len(article_content)
    print(titles)
    

    
    return
    
    # Computer progress score
    # queries = ["Potatoes on mars", "Space cats", "Space vehicles"]
    # for query in queries:
        

    pass

if __name__ == '__main__':
    main()