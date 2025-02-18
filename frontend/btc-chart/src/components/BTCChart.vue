<template>
  <div>
    <h1 class="chart-title">BITCOIN/USDT Price Prediction Chart</h1>
    <div id="chart-container" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  data() {
    return {
      actualData: [],
      predictedData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const actualRes = await fetch("http://127.0.0.1:8000/actual-data");
        const predictedRes = await fetch("http://127.0.0.1:8000/prediction-data");

        const actualPrices = await actualRes.json();
        const predictedPrices = await predictedRes.json();

        this.actualData = actualPrices.map((d) => [d.timestamp, d.actual_price]);
        this.predictedData = predictedPrices.map((d) => [d.timestamp, d.predicted_price]);

        this.renderChart();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    renderChart() {
      const chart = echarts.init(document.getElementById("chart-container"));

      const option = {
        backgroundColor: "#121212",
        title: {
          text: "BTC/USDT Actual & Predicted Prices",
          left: "center",
          textStyle: { color: "#fff", fontSize: 16 },
        },
        tooltip: {
          trigger: "axis",
          axisPointer: { type: "cross", label: { backgroundColor: "#333" } },
        },
        legend: {
          data: ["Actual Price", "Predicted Price"],
          bottom: 10,
          textStyle: { color: "#fff" },
        },
        xAxis: {
          type: "time",
          axisLabel: { color: "#ccc" },
          axisLine: { lineStyle: { color: "#888" } },
          splitLine: { show: true, lineStyle: { color: "#444" } },
        },
        yAxis: {
          type: "value",
          scale: true, // Makes the Y-axis scale dynamically
          axisLabel: { color: "#ccc" },
          axisLine: { lineStyle: { color: "#888" } },
          splitLine: { show: true, lineStyle: { color: "#444" } },
        },
        grid: {
          left: "10%",
          right: "10%",
          bottom: "15%",
          containLabel: true,
        },
        dataZoom: [
          {
            type: "inside", // Scroll using mouse wheel or pinch on mobile
          },
          {
            type: "slider",
            show: true,
            xAxisIndex: 0,
            bottom: 5,
            textStyle: { color: "#ccc" },
          },
        ],
        series: [
          {
            name: "Actual Price",
            type: "line",
            data: this.actualData,
            itemStyle: { color: "#2196F3" },
            lineStyle: { width: 2.5 },
            symbolSize: 3,
          },
          {
            name: "Predicted Price",
            type: "line",
            data: this.predictedData,
            itemStyle: { color: "#FF9800" },
            lineStyle: { width: 3.5, type: "dashed" },
            symbolSize: 5,
          },
        ],
      };

      chart.setOption(option);
    },
  },
};
</script>

<style>
.chart-title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 10px;
  color: white;
}
body {
  background-color: #121212;
}
</style>