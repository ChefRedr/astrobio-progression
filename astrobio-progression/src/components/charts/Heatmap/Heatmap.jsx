// components/charts/Heatmap/Heatmap.jsx
// expects: data = [{ x: string, y: string, v: number }]
import React from "react";
import ReactECharts from "echarts-for-react";
import "./Heatmap.css";

function buildMatrix(pairs, { hideDiagonal = true } = {}) {
  // Collect all unique topic names
  const all = Array.from(
    new Set(pairs.flatMap(d => [d.x, d.y]))
  );

  // Index map
  const idx = new Map(all.map((t, i) => [t, i]));

  // Fill matrix (default 0)
  const mat = Array.from({ length: all.length }, () =>
    Array.from({ length: all.length }, () => 0)
  );

  // Place values (make symmetric by summing both directions)
  for (const { x, y, v } of pairs) {
    const i = idx.get(x);
    const j = idx.get(y);
    if (i == null || j == null) continue;
    mat[i][j] += v || 0;
    mat[j][i] += v || 0; // symmetric for clarity
  }

  // Optional: hide diagonal (null values aren't rendered)
  if (hideDiagonal) {
    for (let i = 0; i < all.length; i++) mat[i][i] = null;
  }

  // Flatten to ECharts triplets [ix, iy, value]
  const triplets = [];
  for (let i = 0; i < all.length; i++) {
    for (let j = 0; j < all.length; j++) {
      const val = mat[i][j];
      if (val == null) {
        triplets.push([i, j, null]);
      } else {
        triplets.push([i, j, val]);
      }
    }
  }

  const maxV = Math.max(1, ...triplets.map(t => (t[2] || 0)));

  return { topics: all, triplets, maxV };
}

export default function Heatmap({ data = [] }) {
  const { topics, triplets, maxV } = buildMatrix(data, { hideDiagonal: true });

  const option = {
    animation: false,
    grid: {
      left: 150,   // room for long y labels
      right: 80,   // room for vertical color scale
      top: 40,
      bottom: 40
    },
    tooltip: {show: false
    },
    xAxis: {
      type: "category",
      data: topics,
      axisLabel: {
        interval: 0,
        rotate: 30,                  // slight tilt
        width: 120,                  // reserve width
        overflow: "truncate",        // built-in truncation
      },
      axisTick: { show: false },
      splitLine: { show: false }
    },
    yAxis: {
      type: "category",
      data: topics,
      axisLabel: {
        interval: 0,
        width: 130,
        overflow: "truncate",        // wrap/truncate as needed
      },
      axisTick: { show: false },
      splitLine: { show: false }
    },
    // Put the color scale on the right so it doesn't cover axes
    visualMap: {
      orient: "vertical",
      right: 10,
      top: "middle",
      min: 0,
      max: maxV,
      calculable: true,
      text: ["More", "Fewer"],
      inRange: {
        color: ["#0b1b2a", "#174064", "#2b7bbb", "#5fd1d7", "#b2f7ef"]
      },
      // Make the handle small & tidy
      itemWidth: 12,
      itemHeight: 120,
      textStyle: { color: "#cbd5e1", fontSize: 11 }
    },
    series: [
      {
        type: "heatmap",
        data: triplets,
        progressive: 0,
        emphasis: { focus: "series" },
        // Nulls won't be colored; add borders for readability
        itemStyle: {
          borderWidth: 1,
          borderColor: "rgba(255,255,255,0.05)"
        }
      }
    ]
  };

  return <ReactECharts option={option} style={{ width: "100%", height: "100%" }} />;
}

