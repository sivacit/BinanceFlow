<template>
  <div id="chart-container" style="height: 500px;"></div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'CandleView',
  data() {
    return {
      chartData: [] // Store candlestick data
    };
  },
  mounted() {
    this.fetchCandlestickData(); // Fetch data when the component mounts
  },
  methods: {
    // Fetch candlestick data from FastAPI
    async fetchCandlestickData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/candlestick-data');
        console.log('Fetched candlestick data:', response.data);

        // Ensure timestamps are correct
        this.chartData = response.data.map(item => [
          item.timestamp, // Use this if already in milliseconds
          item.open,
          item.close,
          item.low,
          item.high
        ]);

        console.log('Formatted chart data:', JSON.stringify(this.chartData));

        if (this.chartData.length === 0) {
          console.error("No candlestick data available. Chart won't render.");
          return;
        }

        this.initChart();
      } catch (error) {
        console.error('Error fetching candlestick data:', error);
      }
    },
    
    // Initialize ECharts
    initChart() {
      const chartContainer = document.getElementById('chart-container');
      if (!chartContainer) {
        console.error("Chart container not found.");
        return;
      }

      const chart = echarts.init(chartContainer);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross' }
        },
        grid: {
          top: '10%', bottom: '15%', left: '10%', right: '10%'
        },
        xAxis: {
          type: 'time',
          axisLabel: {
            formatter: (value) => {
              const date = new Date(value);
              return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
            }
          }
        },
        yAxis: { scale: true },
        dataZoom: [
          { type: 'slider', xAxisIndex: 0, start: 0, end: 100 }, // Horizontal zoom
          { type: 'inside', xAxisIndex: 0, start: 0, end: 100 }, // Scroll zoom
          { type: 'slider', yAxisIndex: 0, start: 0, end: 100 }, // Vertical zoom
          { type: 'inside', yAxisIndex: 0, start: 0, end: 100 }  // Scroll zoom for y-axis
        ],
        series: [{
          name: 'Candlestick',
          type: 'candlestick',
          data: this.chartData,
          itemStyle: {
            color: '#00da3c', color0: '#ec0000',
            borderColor: '#008F28', borderColor0: '#8A0000'
          }
        }]
      };

      console.log("Setting chart options...");
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
#chart-container {
  width: 100%;
  height: 500px;
}
</style>
