import React, { useState } from "react";
import "./HomeNavBar.css";

export default function NavBar({ onSearch, showBack, onBack }) {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // prevents form from reloading the page
      handleSubmit(e);
    }
  };

  return (
    <nav className="navbar">
      <h1 className="title">Space Research Progress</h1>

      <form className="navbar-search" onSubmit={handleSubmit}>
        {showBack && (
          <button
            type="button"
            className="back-button"
            onClick={onBack}
          >
            ← Back
          </button>
        )}

        <input
          type="text"
          placeholder="Search"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          className="search-input"
        />

        <button type="submit" className="search-button">
          Search
        </button>
      </form>
    </nav>
  );
}
