// BidStatusChart.jsx
import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BidStatusChart = () => {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    datasets: [
      {
        label: 'Submitted',
        data: [5, 8, 6, 9, 12, 10, 15],
        backgroundColor: 'rgba(79, 70, 229, 0.5)',
      },
      {
        label: 'Accepted',
        data: [3, 5, 4, 6, 8, 7, 10],
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
      },
      {
        label: 'Rejected',
        data: [2, 3, 2, 3, 4, 3, 5],
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Bid Status Overview (Last 7 Months)',
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 2,
        },
      },
    },
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <Bar options={options} data={data} />
    </div>
  );
};

export default BidStatusChart;