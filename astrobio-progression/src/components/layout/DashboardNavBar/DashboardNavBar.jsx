import React, { useState } from "react";
import "./DashboardNavBar.css";

export default function NavBar({ onSearch, category }) {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(query.trim());
    }
  };

  return (
    <nav className="dashboard-navbar">
      <h1 className="title">{category}</h1>
      <form className="navbar-search" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={handleChange}
          className="search-input"
          aria-label="Search articles"
        />
        <button type="submit" className="search-button">Search</button>
      </form>
    </nav>
  );

}