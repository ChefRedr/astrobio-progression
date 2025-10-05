import React from "react";
import "./ArticleModal.css";

export default function ArticleModal({ article, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()} // prevent closing when clicking inside
      >
        <div className="modal-header">
          <h2>{article.name}</h2>
          <p className="modal-author">{article.author}</p>
        </div>

        <div className="modal-body">
          <div className="modal-left">
            <p>{article.summary}</p>
          </div>
          <div className="modal-right">
            <img src={article.image} alt={article.name} className="modal-image" />
            <a href={article.link} target="_blank" rel="noreferrer">
              Read Full Article
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
