<script setup>
import { ref } from "vue";

const btcData = ref([]);
const startDate = ref(""); // Start Date
const endDate = ref("");   // End Date
const isLoading = ref(false); // Loading state

// Fetch data when clicking the search button
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
    btcData.value = data.data;
  } catch (error) {
    console.error("Error fetching data:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="container">
    <h2>📊 BinanceFlow Data</h2>

    <!-- Date Range Filters + Search Button -->
    <div class="date-filters">
      <div class="input-group">
        <label>Start Date:</label>
        <input type="date" v-model="startDate" />
      </div>
      <div class="input-group">
        <label>End Date:</label>
        <input type="date" v-model="endDate" />
      </div>
      <!-- Search Button -->
      <button @click="fetchData">🔍 Search</button>
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading">⏳ Loading data...</div>

    <!-- Data Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>📅 Timestamp</th>
            <th>📈 Open</th>
            <th>📊 High</th>
            <th>📉 Low</th>
            <th>🔴 Close</th>
            <th>📦 Volume</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in btcData" :key="row.timestamp">
            <td>{{ row.timestamp }}</td>
            <td>{{ row.open }}</td>
            <td>{{ row.high }}</td>
            <td>{{ row.low }}</td>
            <td>{{ row.close }}</td>
            <td>{{ row.volume }}</td>
          </tr>
          <tr v-if="btcData.length === 0">
            <td colspan="6" class="no-data">🚫 No data available</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 90%;
  max-width: 1000px;
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

/* Table */
.table-container {
  display: flex;
  justify-content: center;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #007bff;
  color: white;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

.no-data {
  padding: 20px;
  color: #888;
  font-style: italic;
}
</style>
