import React from "react";
import "./ArticleCard.css";

export default function ArticleCard({ article, isSelected, onSelect }) {
  return (
    <div
      className={`article-card ${isSelected ? "selected" : ""}`}
      onClick={() => onSelect(article.title)}
    >
      <div className="article-header">
        <h3>{article.title}</h3>
        <p className="author">{article.author}</p>
      </div>
      <a href={article.link} target="_blank" rel="noreferrer">
        Read More
      </a>
    </div>
  );
}