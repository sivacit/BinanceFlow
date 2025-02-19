<template>
  <div>
    <h2 class="chart-title">Date Filter</h2>

    <div class="filter-container">
      <label for="start-date">Start Date:</label>
      <input type="date" id="start-date" v-model="startDate" />

      <label for="end-date">End Date:</label>
      <input type="date" id="end-date" v-model="endDate" />

      <button @click="fetchCandlestickData" class="search-btn">Search</button>
    </div>

    <div id="chart-container"></div>
  </div>
</template>

<script>
import axios from "axios";
import * as echarts from "echarts";

export default {
  name: "FilterDate",
  data() {
    return {
      chartData: [],
      startDate: "",
      endDate: "",
      chartInstance: null,
    };
  },
  mounted() {
    this.setDefaultDateRange();
    this.fetchCandlestickData();
    window.addEventListener("resize", this.resizeChart); // Handle resizing
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.resizeChart);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    setDefaultDateRange() {
      const today = new Date();
      this.endDate = today.toISOString().split("T")[0];

      const pastDate = new Date();
      pastDate.setDate(today.getDate() - 7);
      this.startDate = pastDate.toISOString().split("T")[0];
    },

    async fetchCandlestickData() {
      if (!this.startDate || !this.endDate) {
        alert("Please select both start and end dates.");
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/filtered-actual-data?start=${this.startDate}&end=${this.endDate}`
        );

        console.log("Fetched candlestick data:", response.data);

        this.chartData = response.data.map((item) => [
          item.timestamp,
          item.actual_price || item.close, // Fallback to close if actual_price is missing
        ]);

        if (this.chartData.length === 0) {
          console.warn("No data available. Chart won't render.");
          return;
        }

        this.initChart();
      } catch (error) {
        console.error("Error fetching candlestick data:", error);
      }
    },

    initChart() {
      const chartContainer = document.getElementById("chart-container");
      if (!chartContainer) {
        console.error("Chart container not found.");
        return;
      }

      if (this.chartInstance) {
        this.chartInstance.dispose();
      }

      this.chartInstance = echarts.init(chartContainer);

      const option = {
        tooltip: { trigger: "axis", axisPointer: { type: "line" } },
        grid: { top: "10%", bottom: "15%", left: "10%", right: "10%" },
        xAxis: {
          type: "time",
          axisLabel: {
            formatter: (value) => {
              const date = new Date(value);
              return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
            },
          },
        },
        yAxis: {
          type: "value",
          scale: true,
          splitLine: { show: true, lineStyle: { type: "dashed", color: "#ddd" } },
        },
        dataZoom: [
          { type: "slider", xAxisIndex: 0, start: 0, end: 100 },
          { type: "inside", xAxisIndex: 0, start: 0, end: 100 },
        ],
        series: [
          {
            name: "Actual Price",
            type: "line",
            smooth: true,
            data: this.chartData,
            lineStyle: {
              color: "#00aaff",
              width: 2,
            },
            areaStyle: {
              color: "rgba(0, 170, 255, 0.3)",
            },
          },
        ],
      };

      this.chartInstance.setOption(option);
    },

    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },
  },
};
</script>

<style scoped>
.chart-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.filter-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.filter-container label {
  font-size: 16px;
}

.filter-container input {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.search-btn {
  background-color: #ff9800;
  color: white;
  border: none;
  padding: 8px 15px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}

.search-btn:hover {
  background-color: #e68900;
}

#chart-container {
  width: 100%;
  height: 500px;
}
</style>
