import React, { useState, useEffect } from "react";
import Article from "./Article/Article.jsx";
import ArticleModal from "./ArticleModal/ArticleModal.jsx";
import placeholderImage from "../../../assets/react.svg";
import "./ArticleSearch.css";

export default function ArticleSearch({ query }) {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);

  useEffect(() => {
    // Simulate fetching articles related to query
    const mockArticles = [
      {
        id: 1,
        name: `Impact of ${query} on Space Agriculture`,
        author: "Dr. Jane Doe",
        keywords: ["oxygen", "photosynthesis", "growth", "radiation"],
        summary:
          "This study explores how microgravity influences plant growth and nutrient cycles...",
        image: placeholderImage,
        link: "#",
      },
      {
        id: 2,
        name: `${query} Research in Microbial Life`,
        author: "Dr. Mark Patel",
        keywords: ["microbes", "biome", "ISS", "lab", "experiments"],
        summary:
          "Examines microbial adaptation in space environments and implications for life support systems...",
        image: placeholderImage,
        link: "#",
      },
    ];
    setArticles(mockArticles);
  }, [query]);

  return (
    <div className="article-search-container">
      {articles.map((article) => (
        <Article
          key={article.id}
          article={article}
          onClick={() => setSelectedArticle(article)}
        />
      ))}

      {selectedArticle && (
        <ArticleModal
          article={selectedArticle}
          onClose={() => setSelectedArticle(null)}
        />
      )}
    </div>
  );
}