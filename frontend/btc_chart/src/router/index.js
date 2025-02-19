import { createRouter, createWebHistory } from "vue-router";
import BTCChart from "../components/BTCChart.vue";
import CandleView from "../components/CandleView.vue";
import FilterDate from "../components/FilterDate.vue"; // Import the FilterDate component

const routes = [
  { path: "/", name: "BTCChart", component: BTCChart },
  { path: "/candle-view", name: "CandleView", component: CandleView },
  { path: "/filter-date", name: "FilterDate", component: FilterDate }, // Ensure this route exists
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
