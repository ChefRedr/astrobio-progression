import { useNavigate } from "react-router-dom";
import { useState } from "react";
import BarContainer from "./BarContainer/BarContainer.jsx";
import NavBar from "./NavBar/HomeNavBar.jsx";
import ArticleSearch from "../../Common/ArticleSearch/ArticleSearch.jsx";
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