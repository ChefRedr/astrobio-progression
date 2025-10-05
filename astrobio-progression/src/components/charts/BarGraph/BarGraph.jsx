// components/charts/BarGraph/BarGraph.jsx
// expects: data = [{ name: string, value: number }]
import ReactECharts from "echarts-for-react";
import React from "react";
import "./BarGraph.css"

function BarGraph({ data = [] }) {
    const maxLabel = 15; 

    const option = {
    grid: { left: 120, right: 16, top: 24, bottom: 24 },
    xAxis: { type: "value" },
    yAxis: {
        type: "category",
        data: data.map(d => d.name),
        inverse: true,
        axisLabel: {
        interval: 0,  
        hideOverlap: true, 
        formatter: (v) => (v.length > maxLabel ? v.slice(0, maxLabel) + "…" : v),
        }
    },
    series: [
        {
        type: "bar",
        data: data.map(d => d.value),
        label: { show: true,
      position: "right",
      color: "rgba(255,255,255,0.7)", // softer white
      fontSize: 11,                   // smaller text
      fontWeight: 400  }
        }
    ],
    tooltip: {show: false,}
    };

    return (
        <ReactECharts className="bar-graph" option={option} style={{ width: "100%", height: "100%" }}/>
    );
}
export default BarGraph;
