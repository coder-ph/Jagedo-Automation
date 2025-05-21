import React, { useState } from 'react';

const CustomerDashboard = () => {
  const [activeTab, setActiveTab] = useState('home');

  const projects = [
    {
      id: 1,
      title: 'Home Renovation',
      description: 'Complete interior renovation of living room and kitchen.',
      progress: 70,
      status: 'In Progress',
    },
    {
      id: 2,
      title: 'Plumbing Work',
      description: 'Fixing leaking pipes and installing new fixtures.',
      progress: 100,
      status: 'Completed',
    },
    {
      id: 3,
      title: 'Painting Job',
      description: 'Repainting bedrooms and hallway.',
      progress: 40,
      status: 'In Progress',
    },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <div className="text-lg font-medium">
            Welcome to your dashboard! Use the sidebar to navigate.
          </div>
        );
      case 'projects':
        return (
          <div className="space-y-4">
            {projects.map((project) => (
              <div key={project.id} className="bg-white p-4 rounded shadow">
                <h3 className="text-xl font-semibold">{project.title}</h3>
                <p className="text-gray-600">{project.description}</p>
                <div className="mt-2">
                  <div className="text-sm text-gray-500 mb-1">
                    Status: {project.status} ({project.progress}%)
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-blue-500 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${project.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        );
      case 'payments':
        return (
          <div>
            <p className="mb-2">You have no pending payments.</p>
            <p>Last payment: KES 8,000 for Home Renovation - April 2025</p>
          </div>
        );
      case 'messages':
        return (
          <div>
            <p className="mb-2">No new messages.</p>
            <p>Need help? Reach out to our support via the chat option.</p>
          </div>
        );
      case 'settings':
        return (
          <div>
            <p>Update your profile, email, and password here.</p>
            <p className="text-sm text-gray-500 mt-2">Feature coming soon.</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white p-6 shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-blue-700">Dashboard</h1>
        <nav className="space-y-4">
          <button
            onClick={() => setActiveTab('home')}
            className={`w-full text-left px-4 py-2 rounded ${
              activeTab === 'home'
                ? 'bg-blue-100 text-blue-700 font-semibold'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            🏠 Home
          </button>
          <button
            onClick={() => setActiveTab('projects')}
            className={`w-full text-left px-4 py-2 rounded ${
              activeTab === 'projects'
                ? 'bg-blue-100 text-blue-700 font-semibold'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            📁 My Projects
          </button>
          <button
            onClick={() => setActiveTab('payments')}
            className={`w-full text-left px-4 py-2 rounded ${
              activeTab === 'payments'
                ? 'bg-blue-100 text-blue-700 font-semibold'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            💳 Payments
          </button>
          <button
            onClick={() => setActiveTab('messages')}
            className={`w-full text-left px-4 py-2 rounded ${
              activeTab === 'messages'
                ? 'bg-blue-100 text-blue-700 font-semibold'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            📩 Messages
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`w-full text-left px-4 py-2 rounded ${
              activeTab === 'settings'
                ? 'bg-blue-100 text-blue-700 font-semibold'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            ⚙️ Settings
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6">
        <h2 className="text-xl font-bold capitalize mb-4">{activeTab}</h2>
        <div className="bg-white p-6 rounded shadow">{renderContent()}</div>
      </main>
    </div>
  );
};

export default CustomerDashboard;



