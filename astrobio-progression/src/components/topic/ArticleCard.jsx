import React from "react";
import "./ArticleCard.css";

export default function ArticleCard({ article, isSelected, onSelect }) {
  return (
    <div
      className={`article-card ${isSelected ? "selected" : ""}`}
      onClick={onSelect}
    >
      <div className="select-indicator">{isSelected ? "✓" : "+"}</div>
      <div className="article-content">
        <h3>{article.title}</h3>
        <p>{article.author}</p>
        <a href={article.link} target="_blank" rel="noreferrer">
          View Article
        </a>
      </div>
    </div>
  );
}