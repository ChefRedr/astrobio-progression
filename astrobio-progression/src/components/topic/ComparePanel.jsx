import React, { useEffect, useState } from "react";
import CorrelationChart from "../charts/CorrelationChart";
import KeywordsChart from "../charts/KeywordsChart";
import AgreementChart from "../charts/AgreementChart";
import "./ComparePanel.css";

export default function ComparePanel({ selected }) {
  const [comparisonData, setComparisonData] = useState(null);

  useEffect(() => {
    if (selected.length >= 2) {
      // 🔧 Replace with backend comparison call
      setComparisonData({
        correlation: [0.8, 0.9, 0.7],
        keywords: ["oxygen", "growth", "radiation", "pressure"],
        agreement: 85,
      });
    }
  }, [selected]);

  if (!comparisonData) return null;

  return (
    <div className="compare-panel">
      <h2>Comparison Results</h2>
      <CorrelationChart data={comparisonData.correlation} />
      <KeywordsChart keywords={comparisonData.keywords} />
      <AgreementChart score={comparisonData.agreement} />
    </div>
  );
}