import React from "react";
import "./ProgressBar.css";

/**
 * Reusable ProgressBar component
 * @param {string} label - Text to display above the bar
 * @param {number} value - Progress value (0–100)
 * @param {string} color - Bar color (default: blue)
 */

const ProgressBar = ({ label, progress }) => {
  return (
    <div className="progress-container">
      <div className="progress-label">
        <span>{label}</span>
        <span>{progress}%</span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
    
  );
};

export default ProgressBar;
