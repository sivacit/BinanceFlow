import { createRouter, createWebHistory } from "vue-router";
import BTCChart from "../components/BTCChart.vue";
import CandleView from "../components/CandleView.vue";

const routes = [
  { path: "/", name: "BTCChart", component: BTCChart },
  { path: "/candle-view", name: "CandleView", component: CandleView },
  { path: "/filter-date", name: "FilterDate", component: () => import("../components/FilterDate.vue") }, // Lazy loading
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
