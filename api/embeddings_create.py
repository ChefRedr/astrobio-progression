import chromadb
from chromadb.api.client import Client
import os
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import sys
from relevance_score import computeProgress
from clean_documents import clean_documents
from parsed_data import article_content
from pprint import pprint

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

def create_embeddings(documents: list[str], collection_name: str, ids: list[str]) -> None:
    # Clean documents but preserve original text content for embeddings
    documents = clean_documents(documents)
    try:
        vectors = openai_ef(documents)

        collection = client.create_collection(name=collection_name)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=vectors
        )
    except Exception as e:
        print(f"EXCEPTION OCCURED IN `create_embeddings`, exception is {e}\n")
        with open('error_content.txt', 'w') as f:
            for i, doc in enumerate(documents):
                try:
                    vectors = openai_ef([doc])
                except Exception as e:
                    print('===================================================\n')
                    print(f'Error occured at below file\n')
                    print(f'i: \t{i}\n')
                    print(f'id: \t{ids[i]}\n')
                    print(f'document: \t{doc}\n')


def get_relevant_articles(query: str, N: int):
    article_title_matches = client.get_collection(name="article_titles").query(
        query_embeddings=openai_ef([query]),
    )
    article_keyword_matches = client.get_collection(name="article_keywords").query(
        query_embeddings=openai_ef([query]),
    )

    assert set(article_title_matches["ids"]) == set(article_keyword_matches["ids"])

    scores: list[tuple[str, float]] = []
    title_weight = .5
    keywords_weight = 1
    for id in article_keyword_matches["ids"]:
        title_index = article_title_matches["ids"].index(id)
        keyword_index = article_keyword_matches["ids"].index(id)

        title_dist: float = article_title_matches["distances"][title_index]
        keywords_dist: float = article_keyword_matches["distances"][keyword_index] 

        score = float(title_weight * title_dist + keywords_weight * keywords_dist)
        scores.append((id, score))

    # sort by scores
    scores.sort(key=lambda x: x[1])
    assert len(scores) == len(article_title_matches["ids"])

    return scores[:N]
    
def compute_score(query: str, collection_name: str, relevant_ids: list[str], N: int):
    # ids of articles that are releavnt
    client.get_collection(name=collection_name).update(
        ids=relevant_ids,
        metadatas=[{"relevant": True} for _ in relevant_ids]
    )

    matches = client.get_collection(name=collection_name).query(
        query_embeddings=openai_ef([query]),
        n_results=N,
        where={"relevant": True}
    )

    assert "ids" in matches.keys() and "documents" in matches.keys()

    docs = matches["documents"]
    # progresses = np.array([np.float64(computeProgress(doc, query)) for doc in docs])
    # return np.average(progresses)

def data_export() -> tuple[list[str], list[str], list[str], list[list[str]]]:
    ids = [article['paper_id'] for article in article_content]
    titles = [article['title'] for article in article_content]
    keywords = [article['keywords'] if "keywords" in article.keys() else "" for article in article_content]
    paragraphs = [article['paragraphs'] for article in article_content]
    return ids, titles, keywords, paragraphs

def main():

    # pprint(f'length is {len(article_content)}')
    # pprint(article_content[0])

    # return

    embeddings_generated = False
    # possible collection names
    collection_names = ["article_titles", "article_keywords", "article_paragraphs"]
    
    ids = [article['paper_id'] for article in article_content]
    titles = [article['title'] for article in article_content]
    keywords = [article['keywords'] if "keywords" in article.keys() else "" for article in article_content]
    paragraphs = [article['paragraphs'] for article in article_content]

    # check keys are unique identifier
    assert len(set(ids)) == len(ids) == len(article_content)
    assert len(titles) == len(ids)
    assert len(keywords) == len(ids)
    assert len(paragraphs) == len(ids)
    assert all([isinstance(t, str) for t in titles])
    assert all([isinstance(k, str) for k in keywords])
    assert all([len(ps) >= 1 for ps in paragraphs])
    assert isinstance(paragraphs, list)
    assert all(isinstance(ps, list) for ps in paragraphs) and all(isinstance(p, str) for ps in paragraphs for p in ps)

    # pprint.pprint(len(paragraphs[43]))
    # pprint.pprint(keywords)
    # pprint.pprint(len(paragraphs))
    # with open("article_content.txt", "w", encoding='utf-8') as f:
    #     f.write(pprint.PrettyPrinter().pformat(titles)) 

    if not embeddings_generated:
        create_embeddings(documents=titles, collection_name="article_titles", ids=ids)
        create_embeddings(documents=keywords, collection_name="article_keywords", ids=ids)
        for i, id in enumerate(ids):
            create_embeddings(
                documents=paragraphs[i], 
                collection_name=f"article_paragraphs_{id}", 
                ids=[f'{id}_paragraph_num_{j}' for j in range(len(paragraphs[i]))]
            )
    return
    
    # Computer progress score
    # queries = ["Potatoes on mars", "Space cats", "Space vehicles"]
    # for query in queries:

if __name__ == '__main__':
    main()