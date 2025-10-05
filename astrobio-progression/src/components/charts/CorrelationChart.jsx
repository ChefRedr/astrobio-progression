import React from "react";

export default function CorrelationChart({ data }) {
  return (
    <div className="correlation-chart">
      <h3>Correlation Analysis</h3>
      <div className="chart-container">
        {data && data.map((value, index) => (
          <div key={index} className="correlation-bar">
            <div 
              className="bar-fill" 
              style={{ height: `${value * 100}%` }}
            ></div>
            <span>Study {index + 1}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
