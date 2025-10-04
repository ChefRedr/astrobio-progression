from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

possible_progress_values = np.linspace(start=0, stop=1, num=11)

client = OpenAI(api_key="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")

prompt = "How does social media use affect teenage mental health?" 
paragraph = """
In this study, we examined the correlation between social media screen time and sleep quality
among university students. Our results indicate that longer screen time before bed was associated
with reduced sleep duration.
"""

def computeProgress(text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or gpt-4o, gpt-4.1, etc.
        messages=[
            {"role": "system", "content": (
                "You are a research evaluator. Given a prompt and a paragraph, "
                "rate how relevant the paragraph is to the prompt. "
                "Output only a number between 0 and 1, where 1 means 'highly relevant' "
                "and 0 means 'completely irrelevant'."
            )},
            {"role": "user", "content": f"Prompt: {prompt}\n\nParagraph: {paragraph}"}
        ]
    )

    score = float(response.choices[0].message.content.strip())
    print("Relevance Score:", score)