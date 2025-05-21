import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const CustomerDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('requests');
  const [projects, setProjects] = useState([]);
  const [serviceRequests, setServiceRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState({
    totalRequests: 0,
    activeProjects: 0,
    completedProjects: 0,
    pendingRequests: 0
  });

  // Mock data initialization
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockProjects = [
        {
          id: 'prj-001',
          title: 'Kitchen Renovation',
          serviceRequestId: 'req-001',
          status: 'In Progress',
          provider: 'Elite Contractors Ltd',
          startDate: '2023-06-15',
          estimatedEnd: '2023-07-20',
          budget: 'Ksh 250,000',
          progress: 65,
          updates: [
            {
              date: '2023-06-28',
              message: 'Tiling completed, starting on cabinetry',
              photos: ['tile1.jpg', 'tile2.jpg']
            },
            {
              date: '2023-06-20',
              message: 'Demolition and plumbing work completed',
              photos: ['demo1.jpg']
            }
          ]
        },
        {
          id: 'prj-002',
          title: 'Office Electrical Wiring',
          serviceRequestId: 'req-002',
          status: 'Completed',
          provider: 'Power Solutions Kenya',
          startDate: '2023-05-10',
          endDate: '2023-06-05',
          budget: 'Ksh 120,000',
          progress: 100,
          updates: [
            {
              date: '2023-06-03',
              message: 'Final inspection and testing completed',
              photos: ['final1.jpg', 'final2.jpg']
            }
          ]
        },
        {
          id: 'prj-003',
          title: 'Bathroom Remodel',
          serviceRequestId: 'req-004',
          status: 'In Progress',
          provider: 'Home Perfect Ltd',
          startDate: '2023-07-01',
          estimatedEnd: '2023-08-15',
          budget: 'Ksh 180,000',
          progress: 30,
          updates: [
            {
              date: '2023-07-10',
              message: 'Initial demolition completed, preparing for plumbing',
              photos: ['bath1.jpg']
            }
          ]
        }
      ];

      const mockRequests = [
        {
          id: 'req-001',
          title: 'Kitchen Renovation',
          date: '2023-06-10',
          status: 'In Progress',
          type: 'Contractor',
          region: 'Nairobi',
          budget: 'Ksh 250,000',
          description: 'Complete kitchen renovation including tiling, cabinetry, and plumbing work'
        },
        {
          id: 'req-002',
          title: 'Office Electrical Wiring',
          date: '2023-05-05',
          status: 'Completed',
          type: 'Professional',
          region: 'Nairobi',
          budget: 'Ksh 120,000',
          description: 'Complete electrical wiring for new office space'
        },
        {
          id: 'req-003',
          title: 'Plumbing Repair',
          date: '2023-07-01',
          status: 'Pending',
          type: 'Fundi',
          region: 'Nairobi',
          budget: 'Ksh 15,000',
          description: 'Fix leaking pipes in bathroom'
        },
        {
          id: 'req-004',
          title: 'Bathroom Remodel',
          date: '2023-06-25',
          status: 'In Progress',
          type: 'Contractor',
          region: 'Nairobi',
          budget: 'Ksh 180,000',
          description: 'Complete bathroom remodel with new tiles and fixtures'
        }
      ];

      setProjects(mockProjects);
      setServiceRequests(mockRequests);
      
      // Calculate stats
      setStats({
        totalRequests: mockRequests.length,
        activeProjects: mockProjects.filter(p => p.status === 'In Progress').length,
        completedProjects: mockProjects.filter(p => p.status === 'Completed').length,
        pendingRequests: mockRequests.filter(r => r.status === 'Pending').length
      });

      setIsLoading(false);
    }, 1000);
  }, []);

  const handleNewRequest = () => {
    navigate('/service-request');
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      'Pending': 'bg-yellow-100 text-yellow-800',
      'In Progress': 'bg-blue-100 text-blue-800',
      'Completed': 'bg-green-100 text-green-800',
      'Cancelled': 'bg-red-100 text-red-800'
    };
    
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusClasses[status] || 'bg-gray-100 text-gray-800'}`}>
        {status}
      </span>
    );
  };

  const renderStatsCards = () => {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* Total Requests Card */}
        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-indigo-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Requests</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.totalRequests}</p>
            </div>
            <div className="p-3 rounded-full bg-indigo-100 text-indigo-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </div>

        {/* Active Projects Card */}
        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Active Projects</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.activeProjects}</p>
            </div>
            <div className="p-3 rounded-full bg-blue-100 text-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Completed Projects Card */}
        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Completed Projects</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.completedProjects}</p>
            </div>
            <div className="p-3 rounded-full bg-green-100 text-green-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
        </div>

        {/* Pending Requests Card */}
        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-yellow-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Pending Requests</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.pendingRequests}</p>
            </div>
            <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderRequestsTab = () => {
    if (isLoading) return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
    
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-800">My Service Requests</h2>
            <p className="text-sm text-gray-500 mt-1">Track all your service requests in one place</p>
          </div>
          <button
            onClick={handleNewRequest}
            className="flex items-center px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-medium rounded-md transition-all shadow-sm hover:shadow-md"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            New Request
          </button>
        </div>
        
        {renderStatsCards()}
        
        <div className="bg-white shadow rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Request</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {serviceRequests.map((request) => (
                  <tr key={request.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                          </svg>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{request.title}</div>
                          <div className="text-sm text-gray-500">#{request.id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">{request.type} • {request.region}</div>
                      <div className="text-sm text-gray-500">{request.date}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-col">
                        {getStatusBadge(request.status)}
                        <span className="mt-1 text-xs text-gray-500">
                          {request.budget}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {projects.some(p => p.serviceRequestId === request.id) ? (
                        <Link 
                          to={`/project/${request.id}`} 
                          className="text-indigo-600 hover:text-indigo-900 flex items-center justify-end"
                        >
                          View Project
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </Link>
                      ) : (
                        <span className="text-gray-400">No project yet</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  const renderProjectsTab = () => {
    if (isLoading) return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
    
    const activeProjects = projects.filter(p => p.status === 'In Progress');
    const completedProjects = projects.filter(p => p.status === 'Completed');
    
    return (
      <div className="space-y-8">
        <div>
          <h2 className="text-xl font-bold text-gray-800">My Projects</h2>
          <p className="text-sm text-gray-500 mt-1">Track all your active and completed projects</p>
        </div>
        
        {renderStatsCards()}
        
        {/* Active Projects Section */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Active Projects</h3>
            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
              {activeProjects.length} ongoing
            </span>
          </div>
          
          {activeProjects.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {activeProjects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No active projects</h3>
              <p className="mt-1 text-sm text-gray-500">You currently don't have any active projects.</p>
              <button
                onClick={() => setActiveTab('requests')}
                className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
              >
                View Service Requests
              </button>
            </div>
          )}
        </div>
        
        {/* Completed Projects Section */}
        <div className="pt-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Completed Projects</h3>
            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              {completedProjects.length} completed
            </span>
          </div>
          
          {completedProjects.length > 0 ? (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {completedProjects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No completed projects yet</h3>
              <p className="mt-1 text-sm text-gray-500">Your completed projects will appear here.</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  const ProjectCard = ({ project }) => {
    return (
      <div className="bg-white shadow rounded-xl overflow-hidden border border-gray-100 hover:shadow-md transition-shadow">
        <div className="p-5">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{project.title}</h3>
              <p className="text-sm text-gray-500 mt-1">With {project.provider}</p>
            </div>
            {getStatusBadge(project.status)}
          </div>
          
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Progress</span>
              <span>{project.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className={`h-2.5 rounded-full ${
                  project.progress < 30 ? 'bg-red-500' : 
                  project.progress < 70 ? 'bg-yellow-500' : 
                  'bg-green-500'
                }`} 
                style={{ width: `${project.progress}%` }}
              ></div>
            </div>
          </div>
          
          <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-500">Start Date</p>
              <p className="font-medium">{project.startDate}</p>
            </div>
            <div>
              <p className="text-gray-500">{project.status === 'Completed' ? 'Completed' : 'Estimated End'}</p>
              <p className="font-medium">
                {project.status === 'Completed' ? project.endDate : project.estimatedEnd}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Budget</p>
              <p className="font-medium">{project.budget}</p>
            </div>
            <div>
              <p className="text-gray-500">Linked Request</p>
              <Link 
                to={`/request/${project.serviceRequestId}`} 
                className="font-medium text-indigo-600 hover:underline text-sm"
              >
                View Request
              </Link>
            </div>
          </div>
          
          <div className="mt-5">
            <h4 className="text-xs font-semibold text-gray-900 uppercase tracking-wider mb-2">Recent Updates</h4>
            {project.updates.length > 0 ? (
              <div className="space-y-3">
                {project.updates.slice(0, 2).map((update, idx) => (
                  <div key={idx} className="border-l-2 border-indigo-200 pl-3 py-1">
                    <p className="text-xs text-gray-500">{update.date}</p>
                    <p className="text-sm">{update.message}</p>
                    {update.photos && update.photos.length > 0 && (
                      <div className="flex space-x-2 mt-1">
                        {update.photos.map((photo, i) => (
                          <div key={i} className="w-10 h-10 bg-gray-100 rounded flex items-center justify-center overflow-hidden">
                            <span className="text-xs text-gray-400">Photo</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500">No updates yet</p>
            )}
          </div>
        </div>
        
        <div className="bg-gray-50 px-5 py-3 flex justify-end">
          <Link
            to={`/project/${project.id}`}
            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
          >
            View Details
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    );
  };

  const renderMessagesTab = () => {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Messages</h2>
          <p className="text-sm text-gray-500 mt-1">Communicate with your service providers</p>
        </div>
        
        <div className="bg-white shadow rounded-xl overflow-hidden">
          <div className="p-6 text-center">
            <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">No messages yet</h3>
            <p className="mt-2 text-sm text-gray-500">When you start a project, you'll be able to message with your service provider here.</p>
            <div className="mt-6">
              <button
                onClick={() => setActiveTab('projects')}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
              >
                View My Projects
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <ToastContainer position="top-right" autoClose={3000} />
      
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <Link to="/" className="text-xl font-bold text-gray-900 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                ServiceHub
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none relative">
                <span className="sr-only">Notifications</span>
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-red-500"></span>
              </button>
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center">
                  <span className="text-indigo-600 font-medium">JD</span>
                </div>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-700">John Doe</p>
                  <p className="text-xs text-gray-500">Customer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('requests')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'requests'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Service Requests
            </button>
            <button
              onClick={() => setActiveTab('projects')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'projects'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Projects
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'messages'
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Messages
            </button>
          </nav>
        </div>
        
        {/* Tab Content */}
        <div>
          {activeTab === 'requests' && renderRequestsTab()}
          {activeTab === 'projects' && renderProjectsTab()}
          {activeTab === 'messages' && renderMessagesTab()}
        </div>
      </main>
    </div>
  );
};

export default CustomerDashboard;
