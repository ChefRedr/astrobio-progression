import React from "react";

export default function AgreementChart({ score }) {
  return (
    <div className="agreement-chart">
      <h3>Agreement Score</h3>
      <div className="score-container">
        <div className="score-circle">
          <span className="score-value">{score}%</span>
        </div>
        <p>Overall agreement between selected studies</p>
      </div>
    </div>
  );
}
