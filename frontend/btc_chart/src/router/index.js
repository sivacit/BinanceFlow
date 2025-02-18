import { createRouter, createWebHistory } from "vue-router";
import BTCChart from "../components/BTCChart.vue";
import CandleView from "../components/CandleView.vue"; // Import the CandleView component

const routes = [
  {
    path: "/",
    name: "BTCChart",
    component: BTCChart,
  },
  {
    path: "/candle-view",
    name: "CandleView",
    component: CandleView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
