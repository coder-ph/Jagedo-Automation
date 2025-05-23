// RecentJobs.jsx
import React from 'react';

const RecentJobs = () => {
  const jobs = [
    { id: 1, title: 'Kitchen Remodeling', client: 'Sarah Johnson', status: 'In Progress', date: '2023-08-15' },
    { id: 2, title: 'Office Interior Design', client: 'Tech Solutions Ltd', status: 'Completed', date: '2023-08-10' },
    { id: 3, title: 'Garden Landscaping', client: 'Michael Brown', status: 'Pending', date: '2023-08-05' },
    { id: 4, title: 'Bathroom Renovation', client: 'Lisa Wangari', status: 'In Progress', date: '2023-07-28' },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'Completed': return 'bg-green-100 text-green-800';
      case 'Pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Jobs</h2>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div key={job.id} className="border-b border-gray-200 pb-4 last:border-0 last:pb-0">
            <div className="flex justify-between">
              <h3 className="text-sm font-medium text-indigo-600">{job.title}</h3>
              <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(job.status)}`}>
                {job.status}
              </span>
            </div>
            <p className="text-sm text-gray-500 mt-1">Client: {job.client}</p>
            <p className="text-xs text-gray-400 mt-1">Started: {job.date}</p>
          </div>
        ))}
      </div>
      <div className="mt-4 text-right">
        <button className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
          View all jobs →
        </button>
      </div>
    </div>
  );
};

export default RecentJobs;