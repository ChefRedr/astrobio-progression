import { useNavigate } from "react-router-dom";
import { useState } from "react";
import BarContainer from "../../components/layout/BarContainer/BarContainer.jsx";
import NavBar from "../../components/layout/NavBar/HomeNavBar.jsx";
import ArticleSearch from "../../components/articles/ArticleSearch.jsx";
import "./HomePage.css"

function HomePage() {

  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (query) => {
    setQuery(query.trim());
  };

  const handleBack = () => {
    setQuery("");
  };

  return (
    <div className="home-container">
      <NavBar onSearch={handleSearch} showBack={!!query} onBack={handleBack} />
      {query ? <ArticleSearch query={query} /> : <BarContainer />}
    </div>
  );
}

export default HomePage;