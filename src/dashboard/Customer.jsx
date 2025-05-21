import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiHome, FiFolder, FiDollarSign, FiMessageSquare, FiUser, FiLogOut } from 'react-icons/fi';

const CustomerDashboard = () => {
  const [activeTab, setActiveTab] = useState('projects');
  const navigate = useNavigate();

  // Sample projects data
  const [projects, setProjects] = useState([
    {
      id: 1,
      title: 'House Construction',
      status: 'In Progress',
      progress: 65,
      budget: 'KES 8.5M',
      provider: 'BuildRight Ltd'
    },
    {
      id: 2,
      title: 'Office Renovation',
      status: 'Planning',
      progress: 20,
      budget: 'KES 3.2M',
      provider: 'UrbanSpace'
    }
  ]);

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Compact Navbar */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">Jagedo</h1>
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-full hover:bg-gray-100">
              <FiUser className="text-gray-600" />
            </button>
            <button 
              onClick={handleLogout}
              className="p-2 rounded-full hover:bg-gray-100"
            >
              <FiLogOut className="text-gray-600" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-6">
        {/* Centered Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <nav className="inline-flex rounded-md shadow">
            <button
              onClick={() => setActiveTab('projects')}
              className={`px-4 py-2 text-sm font-medium rounded-l-md ${
                activeTab === 'projects' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FiFolder className="inline mr-2" />
              Projects
            </button>
            <button
              onClick={() => setActiveTab('payments')}
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === 'payments' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FiDollarSign className="inline mr-2" />
              Payments
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`px-4 py-2 text-sm font-medium rounded-r-md ${
                activeTab === 'messages' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FiMessageSquare className="inline mr-2" />
              Messages
            </button>
          </nav>
        </div>

        {/* Content Section */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {activeTab === 'projects' && (
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold">My Projects</h2>
                <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
                  + New Project
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {projects.map(project => (
                  <div key={project.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-medium">{project.title}</h3>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        project.status === 'In Progress' ? 'bg-blue-100 text-blue-800' :
                        project.status === 'Completed' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {project.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">{project.provider}</p>
                    
                    <div className="mb-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span>Progress</span>
                        <span>{project.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full" 
                          style={{ width: `${project.progress}%` }}
                        />
                      </div>
                    </div>

                    <div className="flex justify-between text-sm">
                      <span className="font-medium">Budget:</span>
                      <span>{project.budget}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'payments' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-6">Payment History</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Project</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">House Construction</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">KES 2,500,000</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">2025-04-25</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Paid</span>
                      </td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">Office Renovation</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">KES 800,000</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">2025-05-10</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Paid</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'messages' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-6">Messages</h2>
              <div className="text-center py-10 bg-gray-50 rounded-lg">
                <FiMessageSquare className="mx-auto text-4xl text-gray-400 mb-3" />
                <p className="text-gray-500">No new messages</p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default CustomerDashboard;