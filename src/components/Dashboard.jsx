// src/components/Dashboard.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { FaPlusCircle, FaChartLine, FaFileAlt, FaHistory, FaBell, FaSearch, FaUser } from 'react-icons/fa';
import { FiActivity } from 'react-icons/fi';

const Dashboard = () => {
  // Mock data - replace with real data from your API
  const stats = [
    { title: "Active Requests", value: "12", icon: <FiActivity className="text-indigo-500" />, change: "+2", trend: 'up' },
    { title: "Completed", value: "48", icon: <FaFileAlt className="text-green-500" />, change: "+8", trend: 'up' },
    { title: "Pending Approval", value: "5", icon: <FaHistory className="text-yellow-500" />, change: "-1", trend: 'down' },
    { title: "Total Requests", value: "65", icon: <FaChartLine className="text-blue-500" />, change: "+9", trend: 'up' },
  ];

  const recentRequests = [
    { id: "#JPG-1001", type: "Land Survey", status: "In Progress", date: "2023-05-15" },
    { id: "#JPG-1002", type: "Soil Analysis", status: "Completed", date: "2023-05-10" },
    { id: "#JPG-1003", type: "Topographic Map", status: "Pending", date: "2023-05-08" },
    { id: "#JPG-1004", type: "Boundary Survey", status: "In Progress", date: "2023-05-05" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Dashboard Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="mt-2 text-sm text-gray-600">Welcome back! Here's what's happening with your requests.</p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <Link
                to="/customer-request"
                className="inline-flex items-center px-4 py-3 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
              >
                <FaPlusCircle className="mr-2" />
                New Request
              </Link>
              <Link
                to="/customer-dashboard"
                className="inline-flex items-center px-4 py-3 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
              >
                <FaUser className="mr-2" />
                My Dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-10">
          {stats.map((stat, index) => (
            <div 
              key={index} 
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
            >
              <div className="p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 rounded-xl bg-opacity-10 p-4"
                    style={{
                      backgroundColor: stat.trend === 'up' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'
                    }}
                  >
                    {stat.icon}
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.title}
                      </dt>
                      <dd>
                        <div className="text-2xl font-bold text-gray-900">
                          {stat.value}
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
                <div className={`mt-4 flex items-center text-sm ${stat.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.trend === 'up' ? (
                    <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M12 13a1 1 0 100 2h5a1 1 0 001-1v-5a1 1 0 10-2 0v2.586l-4.293-4.293a1 1 0 00-1.414 0L8 9.586l-4.293-4.293a1 1 0 00-1.414 1.414l5 5a1 1 0 001.414 0L11 9.414 14.586 13H12z" clipRule="evenodd" />
                    </svg>
                  )}
                  <span className="font-medium">{stat.change} this week</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Recent Activity and Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Requests */}
          <div className="lg:col-span-2">
            <div className="bg-white shadow-lg rounded-xl overflow-hidden">
              <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 to-indigo-100">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">Recent Requests</h3>
                    <p className="mt-1 text-sm text-gray-600">Your most recent service requests</p>
                  </div>
                  <Link 
                    to="/request-history" 
                    className="text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors duration-200"
                  >
                    View all
                  </Link>
                </div>
              </div>
              <div className="divide-y divide-gray-200">
                {recentRequests.map((request, index) => (
                  <Link 
                    key={index} 
                    to={`/request/${request.id}`} 
                    className="block hover:bg-gray-50 transition-colors duration-150"
                  >
                    <div className="px-6 py-5">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10 rounded-lg bg-indigo-100 flex items-center justify-center">
                            <span className="text-indigo-600 font-medium">
                              {request.id.substring(1, 4)}
                            </span>
                          </div>
                          <div className="ml-4">
                            <h4 className="text-sm font-medium text-gray-900">{request.type}</h4>
                            <p className="text-sm text-gray-500">{request.id}</p>
                          </div>
                        </div>
                        <div className="ml-2 flex-shrink-0 flex">
                          <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                            ${request.status === 'Completed' ? 'bg-green-100 text-green-800' : 
                              request.status === 'In Progress' ? 'bg-blue-100 text-blue-800' : 
                              'bg-yellow-100 text-yellow-800'}`}>
                            {request.status}
                          </span>
                        </div>
                      </div>
                      <div className="mt-3 flex justify-between items-center">
                        <div className="flex items-center text-sm text-gray-500">
                          <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                          </svg>
                          <span>{request.date}</span>
                        </div>
                        <div className="text-sm text-indigo-600 font-medium hover:text-indigo-800">
                          View details
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions and Notifications */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white shadow-lg rounded-xl overflow-hidden">
              <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 to-indigo-100">
                <h3 className="text-xl font-semibold text-gray-900">Quick Actions</h3>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <Link
                    to="/customer-request"
                    className="flex flex-col items-center justify-center p-5 border-2 border-dashed border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-all duration-200 group"
                  >
                    <div className="p-3 rounded-full bg-indigo-100 text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                      <FaPlusCircle className="h-6 w-6" />
                    </div>
                    <span className="mt-3 text-sm font-medium text-gray-700 group-hover:text-indigo-700">New Request</span>
                  </Link>
                  <Link
                    to="/customer-dashboard"
                    className="flex flex-col items-center justify-center p-5 border-2 border-dashed border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-all duration-200 group"
                  >
                    <div className="p-3 rounded-full bg-indigo-100 text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                      <FaUser className="h-6 w-6" />
                    </div>
                    <span className="mt-3 text-sm font-medium text-gray-700 group-hover:text-indigo-700">My Dashboard</span>
                  </Link>
                  <Link
                    to="/search"
                    className="flex flex-col items-center justify-center p-5 border-2 border-dashed border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-all duration-200 group"
                  >
                    <div className="p-3 rounded-full bg-indigo-100 text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                      <FaSearch className="h-6 w-6" />
                    </div>
                    <span className="mt-3 text-sm font-medium text-gray-700 group-hover:text-indigo-700">Search</span>
                  </Link>
                  <Link
                    to="/history"
                    className="flex flex-col items-center justify-center p-5 border-2 border-dashed border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-all duration-200 group"
                  >
                    <div className="p-3 rounded-full bg-indigo-100 text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                      <FaHistory className="h-6 w-6" />
                    </div>
                    <span className="mt-3 text-sm font-medium text-gray-700 group-hover:text-indigo-700">History</span>
                  </Link>
                </div>
              </div>
            </div>

            {/* Notifications */}
            <div className="bg-white shadow-lg rounded-xl overflow-hidden">
              <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-indigo-50 to-indigo-100">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-gray-900">Notifications</h3>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                    3 new
                  </span>
                </div>
              </div>
              <div className="divide-y divide-gray-200">
                <div className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150 group">
                  <div className="flex">
                    <div className="flex-shrink-0 mt-1">
                      <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                        <FaBell className="h-4 w-4" />
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900 group-hover:text-indigo-600">Request #JPG-1001 approved</p>
                      <p className="text-sm text-gray-500">Your land survey request has been approved</p>
                      <div className="mt-1 flex items-center text-xs text-gray-400">
                        <svg className="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                        </svg>
                        <span>2 hours ago</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150 group">
                  <div className="flex">
                    <div className="flex-shrink-0 mt-1">
                      <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                        <FaBell className="h-4 w-4" />
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900 group-hover:text-indigo-600">Document ready</p>
                      <p className="text-sm text-gray-500">Your soil analysis report is available</p>
                      <div className="mt-1 flex items-center text-xs text-gray-400">
                        <svg className="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                        </svg>
                        <span>1 day ago</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="px-6 py-4 hover:bg-gray-50 transition-colors duration-150 group">
                  <div className="flex">
                    <div className="flex-shrink-0 mt-1">
                      <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-200 transition-colors duration-200">
                        <FaBell className="h-4 w-4" />
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900 group-hover:text-indigo-600">Payment received</p>
                      <p className="text-sm text-gray-500">We've received your payment for boundary survey</p>
                      <div className="mt-1 flex items-center text-xs text-gray-400">
                        <svg className="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                        </svg>
                        <span>2 days ago</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
                <Link to="/notifications" className="text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors duration-200">
                  View all notifications
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;