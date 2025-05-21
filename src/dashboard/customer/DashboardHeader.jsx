// DashboardHeader.jsx
import React from 'react';

const DashboardHeader = ({ navigate }) => {
  return (
    <header className="bg-white shadow-sm sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Customer Dashboard</h1>
        <button
          onClick={() => navigate('/create-request')}
          className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-md hover:from-indigo-700 hover:to-purple-700 transition-colors"
        >
          + New Request
        </button>
      </div>
    </header>
  );
};

export default DashboardHeader;