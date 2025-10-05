import React, { useMemo } from "react";
import ReactECharts from "echarts-for-react";
import "echarts-wordcloud";

function WordGraph({ words = [] }) {
    // normalize data to { name, value }
    const data = useMemo(
        () =>
        (Array.isArray(words) ? words : []).map(w => ({
            name: w.text,
            value: Math.max(1, Number(w.weight) || 1),
        })),
        [words]
    );

    const option = {
        tooltip: { formatter: (p) => `${p.name}: ${p.value}` },
        series: [
        {
            type: "wordCloud",
            // try sizes that work well within your 2×2 card
            gridSize: 6,
            sizeRange: [12, 42],            // min/max font size (px)
            rotationRange: [-45, 45],
            rotationStep: 15,
            // keep it centered in the panel
            left: "center",
            top: "center",
            width: "95%",
            height: "95%",
            // color fn (spacey palette)
            textStyle: {
            color: () => {
                const palette = ["#7c9cff", "#26ffd8", "#9aa8c7", "#eaf1ff"];
                return palette[Math.floor(Math.random() * palette.length)];
            },
            emphasis: {
                shadowBlur: 8,
                shadowColor: "rgba(0,0,0,0.35)",
            },
            },
            data,
        },
        ],
    };

    return (
        <ReactECharts
        option={option}
        style={{ width: "100%", height: "100%" }}
        notMerge
        lazyUpdate
        />
    );
}


export default WordGraph;

