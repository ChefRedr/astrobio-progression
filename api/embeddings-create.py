import numpy as np
import chromadb
from chromadb import api 
from chromadb.api.client import Client
from typing import Optional
import os
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT") or 8000)
OPENAI_API_KEY = os.getenv("")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )

# number of relevant articles to retrieve for comparison
N = 500

documents = [
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

def store_embeddings_in_db(client):
    pass

def create_embeddings(texts: list[str]) -> Optional[Client]:
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    collection_to_add = client.get_or_create_collection(name="new_text", )








    

    

    
def match_embeddings(text: str, client):
    