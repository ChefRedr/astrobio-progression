import numpy as np
import chromadb
from chromadb.api.client import Client
from typing import Optional, List
import os
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import sys
from relevance_score import computeProgress
from clean_documents import clean_documents
from parsed_data import article_content
from pprint import pprint
import re

sys.path.insert(0, '..')

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
client = chromadb.PersistentClient(path='./chroma/')

def get_relevant_articles(query: str, N: int):
    query_embedding = openai_ef([query])
    article_title_matches = client.get_collection(name="article_titles").query(
        query_embeddings=query_embedding,
        n_results=(N * 10)
    )
    article_keyword_matches = client.get_collection(name="article_keywords").query(
        query_embeddings=query_embedding,
        n_results=(N * 10)
    )

    # if set(article_title_matches["ids"][0]) != set(article_keyword_matches["ids"][0]):
    #     pprint(f'first few title ids are: {article_title_matches["ids"][0][:10]}')
    #     pprint(f'first few keyword ids are: {article_keyword_matches["ids"][0][:10]}')
    #     pprint(f'difference: {set(article_title_matches["ids"][0]) - set(article_keyword_matches["ids"][0])}')
    #     assert set(article_title_matches["ids"][0]) == set(article_keyword_matches["ids"][0])

    title_ids = article_title_matches["ids"][0]
    title_dists = article_title_matches["distances"][0]
    keyword_ids = article_keyword_matches["ids"][0]
    keyword_dists = article_keyword_matches["distances"][0]

    titles_map = dict(zip(title_ids, title_dists))
    keywords_map = dict(zip(keyword_ids, keyword_dists))

    common_ids = set(title_ids).intersection(set(keyword_ids))

    scores: list[tuple[str, float]] = []
    title_weight = .5
    keywords_weight = 1

    for id in common_ids:
        score = float(title_weight * titles_map[id] + keywords_weight * keywords_map[id])
        
        scores.append((id, score))

        # title_index = article_title_matches["ids"].index(id)
        # keyword_index = article_keyword_matches["ids"].index(id)

        # title_dist: float = article_title_matches["distances"][title_index]
        # keywords_dist: float = article_keyword_matches["distances"][keyword_index] 


    # sort by scores
    # assert len(scores) == len(article_title_matches["ids"])
    scores.sort(key=lambda x: x[1])
    scores = scores[:N]

    collection_names = ["article_titles", "article_keywords", "article_paragraphs"]

    relevant_ids = [id_score[0] for id_score in scores]
    relevant_paragraph_ids: list[list[str]] = [f'{id}_paragraph_num_{j}' for id in relevant_ids for j in range(len(client))]

    relevant_titles = client.get_collection(name="article_titles").get(ids=relevant_ids)['documents']
    relevant_keywords = client.get_collection(name="article_keywords").get(ids=relevant_ids)['documents']

    for i, id in enumerate(ids):
        create_embeddings(
            documents=paragraphs[i], 
            collection_name=f"article_paragraphs_{id}", 
            ids=[f'{id}_paragraph_num_{j}' for j in range(len(paragraphs[i]))]
        )

    paragraphs: list[list[str]] = [
        client.get_collection(name=f"article_paragraphs_{id}").get(ids=)
    ]

    return list(zip(relevant_ids, relevant_titles, relevant_keywords))

def compute_score(query: str, collection_names: list[str], N: int):
    # ids of articles that are releavnt
    # client.get_collection(name=collection_name).update(
    #     ids=relevant_ids,
    #     metadatas=[{"relevant": True} for _ in relevant_ids]
    # )

    overall_score = 0
    for paragraph_collection in collection_names:
        matching_paragraphs = client.get_collection(name=paragraph_collection).query(
            query_embeddings=openai_ef([query]),
            n_results=N,
        )

        assert isinstance(matching_paragraphs["documents"], list)

        this_article_score = 0
        for paragraph in matching_paragraphs["documents"][0]:
            this_article_score += computeProgress(paragraph, query)
        this_article_score /= len(matching_paragraphs["documents"][0])
        overall_score += this_article_score
    overall_score /= len(collection_names)
    return overall_score

relevant_articles = get_relevant_articles('homo sapiens', N=50)
