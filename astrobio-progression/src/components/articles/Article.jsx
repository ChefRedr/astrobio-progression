import React from "react";
import "./Article.css";

export default function Article({ article, onClick }) {
  return (
    <div className="article-bar" onClick={onClick}>
      <div className="article-left">
        <h3 className="article-title">{article.name}</h3>
        <p className="article-author">{article.author}</p>
      </div>
      <div className="article-right">
        {article.keywords.slice(0, 5).map((kw, idx) => (
          <span key={idx} className="keyword-pill">
            {kw}
          </span>
        ))}
      </div>
    </div>
  );
}
