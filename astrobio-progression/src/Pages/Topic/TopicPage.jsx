import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ArticleGrid from "../../components/topic/ArticleGrid";
import ComparePanel from "../../components/topic/ComparePanel";
import BackButton from "../../components/common/BackButton";
import "./TopicPage.css";

export default function TopicPage() {
  const { topic } = useParams();
  const navigate = useNavigate();

  const [articles, setArticles] = useState([]);
  const [selectedArticles, setSelectedArticles] = useState([]);
  const [consoleArticles, setConsoleArticles] = useState([]); // <-- snapshot
  const [mode, setMode] = useState(null); // "insight" | "compare" | null

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
        : prev.length < 2
        ? [...prev, title]
        : prev
    );
  };

  const handleAction = () => {
    if (selectedArticles.length === 1) {
      setConsoleArticles([...selectedArticles]); // snapshot
      setMode("insight");
    } else if (selectedArticles.length === 2) {
      setConsoleArticles([...selectedArticles]); // snapshot
      setMode("compare");
    }
  };

  return (
    <div className="topic-page-container">
      <div className="topic-header">
        <BackButton onClick={() => navigate("/")} />
        <h1 className="topic-title">{topic}</h1>
      </div>

      <div className="topic-content">
        {/* LEFT: Article list */}
        <div className="articles-panel">
          <ArticleGrid
            articles={articles}
            selected={selectedArticles}
            onSelect={handleSelect}
            onAction={handleAction}
          />
        </div>

        {/* RIGHT: Console */}
        <div className="console-panel">
          {mode === "insight" && consoleArticles.length === 1 && (
            <div className="insight-panel">
              <h2>Insights for {consoleArticles[0]}</h2>
              <p>🔬 Keywords, summary, methodology breakdown, etc.</p>
            </div>
          )}

          {mode === "compare" && consoleArticles.length === 2 && (
            <ComparePanel selected={consoleArticles} />
          )}
        </div>
      </div>
    </div>
  );
}