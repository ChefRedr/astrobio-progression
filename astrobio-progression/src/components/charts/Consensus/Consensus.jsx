// components/charts/Consensus/Consensus.jsx
// expects: items = [{ topic: string, consensusPct: number }]
import React from "react";
import "./Consensus.css"

function Consensus({ items = [] }) {
    const color = (pct) => (pct >= 70 ? "#16a34a" : pct >= 40 ? "#ca8a04" : "#dc2626");

    return (
        <div className="consensus-grid">
        {items.map((it) => (
            <div key={it.topic} className="consensus-card">
            <div className="consensus-topic">{it.topic}</div>
            <div className="consensus-value" style={{ color: color(it.consensusPct) }}>
                {Math.round(it.consensusPct)}%
            </div>
            </div>
        ))}
        </div>
    );
}


export default Consensus;
