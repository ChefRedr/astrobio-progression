from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/health')
def get_current_time():
    return {'health': 200}


from typing import Dict, List, Literal

# ✅ Dummy database (dictionary of topics to articles)
DUMMY_ARTICLES: Dict[str, List[Dict[str, str]]] = {
    "Space Farming": [
        {
            "ArticleTitle": "Growing Crops in Martian Soil",
            "Author": "Dr. Jane Smith",
            "Link": "https://nasa.gov/mars-agriculture"
        },
        {
            "ArticleTitle": "Photosynthesis Efficiency in Microgravity",
            "Author": "Dr. Alan Chen",
            "Link": "https://nasa.gov/space-farming"
        }
    ],
    "AI Robotics": [
        {
            "ArticleTitle": "Teaching Robots to Learn Like Humans",
            "Author": "Dr. Maria Lopez",
            "Link": "https://ai-research.org/robot-learning"
        },
        {
            "ArticleTitle": "Ethics of Autonomous Systems",
            "Author": "Prof. Henry Clark",
            "Link": "https://ai-ethics.org/autonomous"
        }
    ]
}

# 1️⃣ Get all articles for a given topic/progress bar
@app.route('/api/articles')
def get_articles_by_topic(topic: str) -> List[Dict[str, str]]:
    """
    Given a topic (progress bar name), return all related articles.

    Args:
        topic (str): The name of the topic or progress bar.

    Returns:
        List[Dict[str, str]]:
            A list of dictionaries, each representing an article with:
                {
                    "ArticleTitle": str,
                    "Author": str,
                    "Link": str
                }

    Example:
        [
            {
                "ArticleTitle": "Growing Crops in Martian Soil",
                "Author": "Dr. Jane Smith",
                "Link": "https://nasa.gov/mars-agriculture"
            },
            {
                "ArticleTitle": "Photosynthesis Efficiency in Microgravity",
                "Author": "Dr. Alan Chen",
                "Link": "https://nasa.gov/space-farming"
            }
        ]
    """
    topic = request.args.get("topic")  # get topic from URL query string

    if not topic:
        return jsonify({"error": "Missing 'topic' query parameter"}), 400

    # Get articles for that topic (case-insensitive)
    articles = DUMMY_ARTICLES.get(topic) or DUMMY_ARTICLES.get(topic.title())

    if not articles:
        return jsonify({"message": f"No articles found for topic '{topic}'"}), 404

    return jsonify(articles)

import random
# 2️⃣ Compare methodology & results between two articles
@app.route('/api/compare')
def compare_articles(article1: str, article2: str) -> List[int]:
    """
    Compare two articles' methodology and results using an LLM.

    Args:
        article1 (str): Title of the first article.
        article2 (str): Title of the second article.

    Returns:
        List[int]:
            [methodology_similarity, results_similarity]
            Each value is an integer between 1–100.

    Example:
        [87, 73]
    """
    # Get article titles from query parameters
    article1 = request.args.get("article1")
    article2 = request.args.get("article2")

    # Validate input
    if not article1 or not article2:
        return {"error": "Missing 'article1' or 'article2' query parameter"}, 400

    # Dummy similarity scores (1-100)
    methodology_similarity = random.randint(50, 100)
    results_similarity = random.randint(50, 100)

    # Return as list
    return {
        "article1": article1,
        "article2": article2,
        "similarity": [methodology_similarity, results_similarity]
    }


# 3️⃣ Get a deep descriptive explanation for similarity results
@app.route('/api/deepdive')
def get_comparison_deepdive(
    article1: str,
    article2: str,
    section: Literal["methodology", "results"]
) -> str:
    """
    Provide a detailed explanation of *why* two articles received their similarity
    scores for the specified section.

    Args:
        article1 (str): Title of the first article.
        article2 (str): Title of the second article.
        section (Literal["methodology", "results"]): The section to analyze.

    Returns:
        str: A detailed natural-language comparison result.

    Example:
        "Both studies used CRISPR-based analysis but applied it to different 
         species, which reduced methodological similarity despite similar 
         objectives."
    """
    # Get query parameters
    article1 = request.args.get("article1")
    article2 = request.args.get("article2")
    section = request.args.get("section")

    # Validate input
    if not article1 or not article2 or not section:
        return {"error": "Missing 'article1', 'article2', or 'section' query parameter"}, 400

    if section not in ["methodology", "results"]:
        return {"error": "Invalid 'section' value. Must be 'methodology' or 'results'"}, 400

    # Dummy explanations
    dummy_explanations = {
        "methodology": [
            f"Both studies used similar experimental setups, but {article2} included additional controls not present in {article1}.",
            f"{article1} focused on in vitro experiments while {article2} conducted in vivo studies, affecting methodology similarity."
        ],
        "results": [
            f"The outcomes of {article1} and {article2} overlapped partially, but differences in sample sizes caused variation in results similarity.",
            f"{article1} reported metrics A and B, whereas {article2} emphasized metrics C and D, explaining the results similarity score."
        ]
    }

    # Choose a pseudo-random explanation based on article names
    idx = (sum(ord(c) for c in article1 + article2) % len(dummy_explanations[section]))
    explanation = dummy_explanations[section][idx]

    return {"article1": article1, "article2": article2, "section": section, "deepdive": explanation}



# 4️⃣ Get related articles for a single article
@app.route('/api/related')
def get_related_articles(article_title: str) -> List[Dict[str, str]]:
    """
    Given an article title, return related or similar articles.

    Args:
        article_title (str): Title of the article.

    Returns:
        List[Dict[str, str]]:
            Each dictionary represents a related article with:
                {
                    "ArticleTitle": str,
                    "Author": str,
                    "Link": str
                }

    Example:
        [
            {
                "ArticleTitle": "Soil Nutrient Cycling in Low Gravity",
                "Author": "Dr. L. Brown",
                "Link": "https://nasa.gov/soil-gravity"
            },
            {
                "ArticleTitle": "Hydroponic Growth Systems for Space Missions",
                "Author": "Dr. P. Gomez",
                "Link": "https://nasa.gov/hydroponics"
            }
        ]
    """
    # Get the article title from query parameters
    article_title = request.args.get("article_title")

    # Validate input
    if not article_title:
        return {"error": "Missing 'article_title' query parameter"}, 400

    # Dummy related articles
    DUMMY_RELATED = [
        {
            "ArticleTitle": f"{article_title} - Advanced Insights",
            "Author": "Dr. L. Brown",
            "Link": "https://nasa.gov/related1"
        },
        {
            "ArticleTitle": f"{article_title} - Experimental Follow-up",
            "Author": "Dr. P. Gomez",
            "Link": "https://nasa.gov/related2"
        },
        {
            "ArticleTitle": f"{article_title} - Comparative Study",
            "Author": "Dr. K. Singh",
            "Link": "https://nasa.gov/related3"
        }
    ]

    return {"article_title": article_title, "related_articles": DUMMY_RELATED}



    if __name__ == '__main__':
        app.run(debug=True)
