// DashboardOverview.jsx
import React from 'react';
import StatCard from './StatCard';
import RecentJobs from './RecentJobs';
import BidStatusChart from './BidStatusChart';

const DashboardOverview = () => {
  const stats = [
    { title: 'Active Bids', value: '12', change: '+2', trend: 'up' },
    { title: 'Jobs Won', value: '8', change: '+3', trend: 'up' },
    { title: 'Total Earnings', value: 'Ksh 245,000', change: '+15%', trend: 'up' },
    { title: 'Response Rate', value: '89%', change: '-2%', trend: 'down' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <BidStatusChart />
        </div>
        <div>
          <RecentJobs />
        </div>
      </div>
    </div>
  );
};

export default DashboardOverview;