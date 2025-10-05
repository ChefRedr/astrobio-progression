// Pages/Dashboard/Dashboard.jsx
import { useMemo, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import NavBar from "../../components/layout/DashboardNavBar/DashboardNavBar.jsx";
import BarGraph from "../../components/charts/BarGraph/BarGraph.jsx";
import Heatmap from "../../components/charts/Heatmap/Heatmap.jsx";
import WordGraph from "../../components/charts/WordGraph/WordGraph.jsx";
import Consensus from "../../components/charts/Consensus/Consensus.jsx";
import ArticleSearch from "../../components/articles/ArticleSearch.jsx";
import { categories } from "../../components/layout/BarContainer/categories.js";
import "./Dashboard.css";

function Dashboard() {
  const { category: param } = useParams();
  const [query, setQuery] = useState("");

  const handleSearch = (q) => setQuery(q.trim());
  const handleBack = () => {
    setQuery("");
  };

  // clear search when changing category
  useEffect(() => setQuery(""), [param]);

  const cat = useMemo(() => categories.find(c => c.param === param), [param]);

  if (!cat) {
    return (
      <div className="dashboard-container">
        <NavBar onSearch={handleSearch} category="Dashboard" />
        <main className="graphs-container">
          <h1>Dashboard</h1>
          <p>Select a category from the home page.</p>
        </main>
      </div>
    );
  }

  // ----- Transformations for charts -----
  const barData = cat.topics.map(t => ({ name: t.topic, value: t.count,  }));
  const sortedBarData = barData.sort((a, b) => b.value - a.value).slice(0, 5);
  const heatmapData = cat.topics.map(t => ({
    x: t.topic,
    y: t.consensusPct >= 70 ? "High consensus (≥70%)"
       : t.consensusPct >= 40 ? "Medium (40–69%)"
       : "Low (<40%)",
    v: t.count
  }));
  const wordData = cat.topics.map(t => ({ text: t.topic, weight: t.count }));
  const consensusItems = cat.topics.map(t => ({
    topic: t.topic,
    consensusPct: t.consensusPct
  }));

  const hasQuery = query.length > 0;
  const showBack = () => {
    console.log("showBack", query);
    return !!query;
  }
  

  return (
    <div className="dashboard-container">
      <NavBar onSearch={handleSearch} showBack={hasQuery} onBack={handleBack} category={cat.label} />

      {hasQuery ? (
        <main className="search-container" style={{ padding: "14px" }}>
          <ArticleSearch query={query} />
        </main>
      ) : (
        <main className="graphs-container">
          <section>
            <h2>Top Topics</h2>
            <BarGraph data={sortedBarData} />
          </section>

          <section>
            <h2>Overlapping Research and Gaps</h2>
            <Heatmap data={heatmapData} />
          </section>

          <section>
            <h2>Word Graph</h2>
            <WordGraph words={wordData} />
          </section>

          <section className="consensus-panel">
            <h2>Consensus by Topic</h2>
            <Consensus items={consensusItems} />
          </section>
        </main>
      )}
    </div>
  );
}

export default Dashboard;
