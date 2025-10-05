import React, { useEffect, useState } from "react";
import { fetchArticles } from "../../services/api";
import ArticleCard from "./ArticleCard";
import "./ArticleGrid.css";

export default function ArticleGrid({ topic }) {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetchArticles(topic).then(setArticles).catch(console.error);
  }, [topic]);

  return (
    <div className="article-grid">
      {articles.map((a) => (
        <ArticleCard key={a.id} article={a} />
      ))}
    </div>
  );
}