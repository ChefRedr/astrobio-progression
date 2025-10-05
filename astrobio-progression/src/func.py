from typing import Dict, List, Literal

# 1️⃣ Get all articles for a given topic/progress bar
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
    ...


# 2️⃣ Compare methodology & results between two articles
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
    ...


# 3️⃣ Get a deep descriptive explanation for similarity results
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
    ...


# 4️⃣ Get related articles for a single article
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
    ...