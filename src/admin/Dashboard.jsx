// src/pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { fetchDashboardData } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchDashboardData();
        setStats(data);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard Overview</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard 
          title="Total Users" 
          value={stats.total_users} 
          icon="👥" 
          color="bg-blue-100 text-blue-800"
        />
        <StatCard 
          title="Active Projects" 
          value={stats.active_projects} 
          icon="🏗️" 
          color="bg-green-100 text-green-800"
        />
        <StatCard 
          title="Pending Bids" 
          value={stats.pending_bids} 
          icon="📝" 
          color="bg-yellow-100 text-yellow-800"
        />
        <StatCard 
          title="Revenue" 
          value={`$${stats.revenue.toLocaleString()}`} 
          icon="💰" 
          color="bg-purple-100 text-purple-800"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-4">
          {stats.recent_activity.map((activity, index) => (
            <ActivityItem key={index} activity={activity} />
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color }) {
  return (
    <div className={`${color} p-6 rounded-lg shadow`}>
      <div className="flex justify-between">
        <div>
          <p className="text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </div>
  );
}

function ActivityItem({ activity }) {
  return (
    <div className="flex items-start border-b pb-3 last:border-0 last:pb-0">
      <div className="bg-gray-100 p-2 rounded-full mr-3">
        {activity.type === 'user' ? '👤' : activity.type === 'project' ? '📋' : '💰'}
      </div>
      <div>
        <p className="font-medium">{activity.message}</p>
        <p className="text-sm text-gray-500">{new Date(activity.timestamp).toLocaleString()}</p>
      </div>
    </div>
  );
}