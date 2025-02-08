<script setup>
import { ref, onMounted } from "vue";
import { AgFinancialCharts } from "ag-charts-vue3";
import "ag-charts-enterprise";

// Get current date in YYYY-MM-DD format
const today = new Date().toISOString().split("T")[0];

const btcData = ref([]);
const startDate = ref(today); // Default to today's date
const endDate = ref(today); // Default to today's date
const isLoading = ref(false);

const chartOptions = ref({
  title: { text: "📊 BTC/USDT Candlestick Chart", fontSize: 18 },
  autoSize: true,
  background: { fill: "white" },
  axes: [
    {
      type: "time",
      position: "bottom",
      label: { format: "%Y-%m-%d" },
    },
    {
      type: "number",
      position: "left",
      title: { text: "Price (USDT)" },
      keys: ["open", "high", "low", "close"],
    },
  ],
  series: [
    {
      type: "candlestick",
      xKey: "timestamp",
      openKey: "open",
      highKey: "high",
      lowKey: "low",
      closeKey: "close",
      upColor: "#28a745",
      downColor: "#dc3545",
    },
  ],
  legend: { enabled: false },
});

// Fetch BTC data from FastAPI
const fetchData = async () => {
  try {
    if (!startDate.value || !endDate.value) {
      alert("Please select both start and end dates.");
      return;
    }

    isLoading.value = true;
    let url = `http://127.0.0.1:8000/questdb-data?start_date=${startDate.value}&end_date=${endDate.value}`;

    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch data");

    const data = await response.json();
    btcData.value = data.data.map((row) => ({
      timestamp: new Date(row.timestamp),
      open: row.open,
      high: row.high,
      low: row.low,
      close: row.close,
    }));

    chartOptions.value = { ...chartOptions.value, data: btcData.value };
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};

// Fetch data when the component is mounted
onMounted(fetchData);
</script>

<template>
  <div class="container">
    <h2>BTC</h2>

    <!-- Date Range Selection -->
    <div class="date-filters">
      <div class="input-group">
        <label>Start Date:</label>
        <input type="date" v-model="startDate" />
      </div>
      <div class="input-group">
        <label>End Date:</label>
        <input type="date" v-model="endDate" />
      </div>
      <button @click="fetchData">🔍 Search</button>
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading">⏳ Loading data...</div>

    <!-- Candlestick Chart -->
    <div class="chart-container">
      <ag-financial-charts :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 90%;
  max-width: 1200px;
  margin: 40px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

/* Title */
h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

/* Date Filters */
.date-filters {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
}

.input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-group label {
  font-size: 14px;
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

input[type="date"] {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

/* Search Button */
button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background-color: #0056b3;
}

/* Loading */
.loading {
  font-size: 18px;
  color: #ff9800;
  margin: 10px 0;
}

/* Chart */
.chart-container {
  width: 100%;
  height: 500px;
  min-height: 400px;
  margin-bottom: 20px;
  background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%);
  border-radius: 10px;
  padding: 15px;
}
</style>
