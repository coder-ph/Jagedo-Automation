// ProjectsTabs.jsx
import React from 'react';

const ProjectsTabs = ({ activeTab, setActiveTab }) => {
  return (
    <div className="border-b border-gray-200 mb-6">
      <nav className="-mb-px flex space-x-8">
        <button
          onClick={() => setActiveTab('active')}
          className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'active' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
        >
          Active Projects
        </button>
        <button
          onClick={() => setActiveTab('completed')}
          className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'completed' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
        >
          Completed (Pending Approval)
        </button>
        <button
          onClick={() => setActiveTab('approved')}
          className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'approved' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
        >
          Approved Projects
        </button>
        <button
          onClick={() => setActiveTab('rejected')}
          className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'rejected' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
        >
          Rejected Projects
        </button>
      </nav>
    </div>
  );
};

export default ProjectsTabs;