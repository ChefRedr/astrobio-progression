import React, { useMemo, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom"; 
import "./DashboardNavBar.css";

export default function NavBar({ onSearch, showBack, onBack, category }) {
  const [query, setQuery] = useState("");
  const { topic: param } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (!showBack) setQuery("");
  }, [showBack]);

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query.trim());
    }
  };

  const handleDashboard = () => {
    navigate(`/dashboard/${param}`);  // 👈 go to the dashboard for this category
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // prevents form from reloading the page
      handleSubmit(e);
    }
  };

  return (
    <nav className="dashboard-navbar">
      <h1 className="title">{category}</h1>

      <button type="button" className="dashboard-button" onClick={handleDashboard}>
        Analysis Dashboard
      </button>

      <form className="navbar-search" onSubmit={handleSubmit}>
        {showBack && (
          <button
            type="button"
            className="clear-button"
            onClick={onBack}
          >
            Clear
          </button>
        )}

        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="search-input"
          aria-label="Search articles"
        />
        <button type="submit" className="search-button">Search</button>
      </form>
    </nav>
  );

}