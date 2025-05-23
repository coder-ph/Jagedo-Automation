// BidStatusTabs.jsx
import React from 'react';

const BidStatusTabs = ({ activeStatus, onChange, counts }) => {
  const tabs = [
    { id: 'all', label: 'All Bids', count: counts.all },
    { id: 'pending', label: 'Pending', count: counts.pending },
    { id: 'accepted', label: 'Accepted', count: counts.accepted },
    { id: 'rejected', label: 'Rejected', count: counts.rejected },
  ];

  return (
    <div className="border-b border-gray-200">
      <nav className="-mb-px flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
              activeStatus === tab.id
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            {tab.label}
            {tab.count > 0 && (
              <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-medium ${
                activeStatus === tab.id
                  ? 'bg-indigo-100 text-indigo-600'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </nav>
    </div>
  );
};

export default BidStatusTabs;