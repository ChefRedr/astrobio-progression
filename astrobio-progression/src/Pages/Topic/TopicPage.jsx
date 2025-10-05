import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ArticleGrid from "../../components/topic/ArticleGrid";
import ComparePanel from "../../components/topic/ComparePanel";
import BackButton from "../../components/common/BackButton";
import "./TopicPage.css";

export default function TopicPage() {
  const { topic } = useParams(); // assuming route like /topic/:topic
  const navigate = useNavigate();

  const [articles, setArticles] = useState([]);
  const [selectedArticles, setSelectedArticles] = useState([]);

  useEffect(() => {
    async function fetchArticles() {
      // 🔧 Replace with backend call
      const data = [
        { title: "Mars Habitat Systems", author: "Dr. Smith", link: "#" },
        { title: "Lunar Agriculture", author: "Dr. Chen", link: "#" },
        { title: "Closed Loop Ecosystems", author: "Dr. Rao", link: "#" },
        { title: "Biosphere Life Support", author: "Dr. Nguyen", link: "#" },
      ];
      setArticles(data);
    }
    fetchArticles();
  }, [topic]);

  const handleSelect = (title) => {
    setSelectedArticles((prev) =>
      prev.includes(title)
        ? prev.filter((t) => t !== title)
        : [...prev, title]
    );
  };

  const handleCompare = () => {
    console.log("Comparing:", selectedArticles);
  };

  return (
    <div className="topic-page-container">
      <div className="topic-header">
        <BackButton onClick={() => navigate("/")} />
        <h1 className="topic-title">{topic}</h1>
      </div>

      {selectedArticles.length >= 2 && (
        <ComparePanel selected={selectedArticles} />
      )}

      <ArticleGrid
        articles={articles}
        selected={selectedArticles}
        onSelect={handleSelect}
        onCompare={handleCompare}
      />
    </div>
  );
}