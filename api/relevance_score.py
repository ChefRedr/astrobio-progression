from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os
import chromadb.utils.embedding_functions as embedding_functions

load_dotenv()

possible_progress_values = np.linspace(start=0, stop=1, num=11)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )

def computeProgress(paragraph: str, query: str):
    progress_prompt = f"The text below indicates something about how far close we are to achieving {query}. Based solely on the text below, answer on a scale of [ {possible_progress_values} ] how close we are to achieving {query}."
    
    # client = chromadb.PersistentClient(path='./chroma/')

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o, gpt-4.1, etc.
        messages=[
            {"role": "system", "content": (
                "You are a research evaluator. Given a prompt and a paragraph, "
                "rate how relevant the paragraph is to the prompt. "
                "Output only a number between 0 and 1, where 1 means 'highly relevant' "
                "and 0 means 'completely irrelevant'."
            )},
            {"role": "user", "content": f"Prompt: {progress_prompt}\n\nParagraph: {paragraph}"}
        ]
    )

    score = float(response.choices[0].message.content.strip())
    assert np.any(np.isin(possible_progress_values, score))

    return score