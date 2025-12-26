async function fetchSalesData() {
  // Fetch the data from Django API
  const res = await fetch('/myadmin/api/live-sales/');  // change URL to your view
  const data = await res.json();

  // Transform backend data into ApexCharts format
  return data.map(item => ({ x: item.time, y: item.value }));
}

async function renderChart() {
  const salesData = await fetchSalesData();

  const options = {
    chart: {
      type: 'line',
      height: 400,
      zoom: { enabled: true },
      toolbar: { show: false },
      animations: { enabled: true, easing: 'easeinout', speed: 800 }
    },
    series: [
      {
        name: 'Sales',
        data: salesData
      }
    ],
    stroke: { curve: 'smooth', width: 3 },
    markers: { size: 6, hover: { size: 8 } },
    grid: {
      borderColor: '#f0f0f0',
      row: { colors: ['#f9f9f9', 'transparent'], opacity: 0.5 }
    },
    xaxis: { type: 'category', title: { text: 'Time' } },
    yaxis: { title: { text: 'Sales Value' } },
    tooltip: { theme: 'dark', x: { format: 'HH:mm' } },
    colors: ['#00BFFF'],
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        type: 'vertical',
        shadeIntensity: 0.5,
        opacityFrom: 0.8,
        opacityTo: 0.3
      }
    },
    theme: { mode: 'light' }  // Change to 'dark' for dark mode
  };

  const chart = new ApexCharts(document.querySelector("#sales-chart"), options);
  chart.render();
}

// Render chart
renderChart();
