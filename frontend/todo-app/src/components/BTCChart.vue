<template>
  <div class="chart-container">
    <canvas ref="btcChart"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

export default {
  setup() {
    const btcChart = ref(null);

    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/questdb-data"); // Adjust URL if needed
        const jsonData = await response.json();
        
        if (!jsonData.data || jsonData.data.length === 0) {
          console.error("No data received from API.");
          return;
        }

        const timestamps = jsonData.data.map(item => new Date(item.timestamp).toLocaleString());
        const prices = jsonData.data.map(item => item.close);

        renderChart(timestamps, prices);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const renderChart = (labels, data) => {
      if (btcChart.value) {
        new Chart(btcChart.value, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "BTC Price (USD)",
                data: data,
                borderColor: "#ff9900",
                backgroundColor: "rgba(255, 153, 0, 0.2)",
                borderWidth: 2,
                fill: true,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      }
    };

    onMounted(fetchData);

    return { btcChart };
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>       