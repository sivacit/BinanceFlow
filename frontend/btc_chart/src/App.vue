<template>
  <div>
    <h1>BTC/USDT Price Prediction Chart</h1>
    <BTCChart />
  </div>
  <div id="app">
    <router-view /> <!-- This is where your route components will be displayed -->
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Set the background color for the entire app */
body {
  background-color: #121212; /* Dark background color */
  color: white; /* White text color for contrast */
  margin: 0;
  padding: 0;
}

/* Optional styling for the header */
h1 {
  color: #3d1fe2;
  text-align: center;
  margin-top: 20px;
}
</style>
