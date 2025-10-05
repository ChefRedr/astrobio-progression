import React from "react";

export default function KeywordsChart({ keywords }) {
  return (
    <div className="keywords-chart">
      <h3>Common Keywords</h3>
      <div className="keywords-container">
        {keywords && keywords.map((keyword, index) => (
          <span key={index} className="keyword-tag">
            {keyword}
          </span>
        ))}
      </div>
    </div>
  );
}
