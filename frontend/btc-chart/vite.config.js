import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "127.0.0.1",
    port: 8001, // ✅ Running on port 8001
  },
  optimizeDeps: {
    include: ["echarts"], // ✅ Preload ECharts for faster load times
  },
});
