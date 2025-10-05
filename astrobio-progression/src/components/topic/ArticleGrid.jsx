import React from "react";
import ArticleCard from "./ArticleCard";
import "./ArticleGrid.css";

export default function ArticleGrid({ articles, selected, onSelect, onAction }) {
  return (
    <div className="article-grid-container">
      <div className="article-grid">
        {articles.map((article) => (
          <ArticleCard
            key={article.title}
            article={article}
            isSelected={selected.includes(article.title)}
            onSelect={onSelect}
          />
        ))}
      </div>

      {selected.length > 0 && (
        <button className="action-button" onClick={onAction}>
          {selected.length === 1 ? "Generate Insights" : "Compare Articles"}
        </button>
      )}
    </div>
  );
}