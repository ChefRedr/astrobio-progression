import React from "react";
import ArticleCard from "./ArticleCard";
import "./ArticleGrid.css";

export default function ArticleGrid({ articles, selected, onSelect, onCompare }) {
  return (
    <div className="article-grid">
      {articles.map((article, index) => (
        <ArticleCard
          key={index}
          article={article}
          isSelected={selected.includes(article.title)}
          onSelect={() => onSelect(article.title)}
        />
      ))}
      {selected.length >= 2 && (
        <button className="compare-button" onClick={onCompare}>
          Compare Selected ({selected.length})
        </button>
      )}
    </div>
  );
}