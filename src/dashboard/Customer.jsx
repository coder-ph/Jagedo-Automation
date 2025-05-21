import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiHome, FiFolder, FiDollarSign, FiMessageSquare, FiSettings, FiLogOut, FiCheckCircle, FiAlertCircle, FiClock, FiUpload, FiDownload } from 'react-icons/fi';

const CustomerDashboard = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [selectedProject, setSelectedProject] = useState(null);
  const [approvalStatus, setApprovalStatus] = useState({});
  const navigate = useNavigate();

  const serviceProviders = {
    fundi: {
      name: "Fundi",
      description: "Skilled tradesperson for hands-on construction work"
    },
    professional: {
      name: "Professional",
      description: "Licensed experts (architects, engineers)"
    },
    contractor: {
      name: "Contractor",
      description: "Project managers overseeing entire construction"
    },
    hardware: {
      name: "Hardware",
      description: "Material suppliers and equipment providers"
    }
  };

  const projects = [
    {
      id: 1,
      title: 'Residential House Construction',
      description: 'Construction of a 3-bedroom bungalow in Karen',
      progress: 65,
      status: 'In Progress',
      startDate: '2025-03-15',
      estimatedCompletion: '2025-08-30',
      budget: 'KES 8,500,000',
      serviceProviders: [
        { type: 'contractor', name: 'BuildRight Contractors', status: 'Active' },
        { type: 'professional', name: 'DesignPlus Architects', status: 'Completed' },
        { type: 'fundi', name: 'Masonry Experts Ltd', status: 'Active' },
        { type: 'hardware', name: 'Jenga Materials', status: 'Pending' }
      ],
      milestones: [
        { name: 'Design Approval', completed: true, date: '2025-04-02' },
        { name: 'Foundation', completed: true, date: '2025-05-18' },
        { name: 'Wall Construction', completed: false, status: 'In Progress' },
        { name: 'Roofing', completed: false },
        { name: 'Finishing', completed: false }
      ],
      documents: [
        { name: 'Signed Contract.pdf', type: 'contract', date: '2025-03-20' },
        { name: 'Architectural Plans.pdf', type: 'design', date: '2025-04-01' },
        { name: 'Foundation Inspection.jpg', type: 'photo', date: '2025-05-20' }
      ],
      pendingApprovals: [
        { 
          title: 'Wall Construction Approval', 
          description: 'Approve completed brickwork before proceeding', 
          provider: 'Masonry Experts Ltd',
          documents: ['Wall Inspection Report.pdf', 'Brickwork Photos.zip']
        }
      ]
    },
    {
      id: 2,
      title: 'Office Renovation',
      description: 'Modernization of 5th floor office space in Westlands',
      progress: 30,
      status: 'In Progress',
      startDate: '2025-05-10',
      estimatedCompletion: '2025-07-25',
      budget: 'KES 3,200,000',
      serviceProviders: [
        { type: 'contractor', name: 'UrbanSpace Renovators', status: 'Active' },
        { type: 'professional', name: 'OfficeDesign Kenya', status: 'Active' },
        { type: 'fundi', name: 'Carpentry Masters', status: 'Pending' }
      ],
      milestones: [
        { name: 'Design Finalization', completed: true, date: '2025-05-05' },
        { name: 'Demolition', completed: true, date: '2025-05-15' },
        { name: 'Electrical Work', completed: false, status: 'In Progress' },
        { name: 'Partitioning', completed: false },
        { name: 'Furnishing', completed: false }
      ],
      documents: [
        { name: 'Renovation Contract.pdf', type: 'contract', date: '2025-05-08' },
        { name: '3D Design Renderings.pdf', type: 'design', date: '2025-05-12' }
      ]
    },
    {
      id: 3,
      title: 'Boundary Wall Construction',
      description: '200m perimeter wall with electric fence',
      progress: 100,
      status: 'Completed',
      startDate: '2025-01-05',
      completionDate: '2025-03-28',
      budget: 'KES 1,750,000',
      serviceProviders: [
        { type: 'contractor', name: 'SecureFence Ltd', status: 'Completed' },
        { type: 'fundi', name: 'Stonework Specialists', status: 'Completed' }
      ],
      milestones: [
        { name: 'Survey & Marking', completed: true, date: '2025-01-10' },
        { name: 'Foundation', completed: true, date: '2025-01-25' },
        { name: 'Wall Construction', completed: true, date: '2025-02-20' },
        { name: 'Fence Installation', completed: true, date: '2025-03-15' },
        { name: 'Final Inspection', completed: true, date: '2025-03-25' }
      ],
      documents: [
        { name: 'Contract Agreement.pdf', type: 'contract', date: '2025-01-07' },
        { name: 'Completion Certificate.pdf', type: 'certificate', date: '2025-03-28' },
        { name: 'Final Wall Photos.jpg', type: 'photo', date: '2025-03-27' }
      ]
    }
  ];

  const handleLogout = () => {
    // Add logout logic here
    navigate('/');
  };

  const handleApprove = (projectId, approvalTitle) => {
    setApprovalStatus(prev => ({
      ...prev,
      [`${projectId}-${approvalTitle}`]: 'approved'
    }));
    // In a real app, you would send this to your backend
  };

  const handleRequestRevision = (projectId, approvalTitle) => {
    setApprovalStatus(prev => ({
      ...prev,
      [`${projectId}-${approvalTitle}`]: 'revision'
    }));
    // In a real app, you would send this to your backend
  };

  const renderHome = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-2">Welcome back to Jagedo!</h2>
        <p className="mb-4">Track your construction projects and collaborate with service providers.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white bg-opacity-20 p-4 rounded">
            <h3 className="font-semibold">Active Projects</h3>
            <p className="text-2xl font-bold">{projects.filter(p => p.status === 'In Progress').length}</p>
          </div>
          <div className="bg-white bg-opacity-20 p-4 rounded">
            <h3 className="font-semibold">Pending Approvals</h3>
            <p className="text-2xl font-bold">{projects.reduce((acc, p) => acc + (p.pendingApprovals?.length || 0), 0)}</p>
          </div>
          <div className="bg-white bg-opacity-20 p-4 rounded">
            <h3 className="font-semibold">Completed Projects</h3>
            <p className="text-2xl font-bold">{projects.filter(p => p.status === 'Completed').length}</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {projects.slice(0, 2).map(project => (
            <div key={project.id} className="border-b pb-4 last:border-b-0 last:pb-0">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-medium">{project.title}</h4>
                  <p className="text-sm text-gray-600">{project.description}</p>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  project.status === 'Completed' ? 'bg-green-100 text-green-800' :
                  project.status === 'In Progress' ? 'bg-blue-100 text-blue-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {project.status}
                </span>
              </div>
              <div className="mt-2">
                <div className="flex justify-between text-sm mb-1">
                  <span>Progress</span>
                  <span>{project.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      project.status === 'Completed' ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${project.progress}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderProjects = () => (
    <div className="space-y-6">
      {projects.map(project => (
        <div key={project.id} className="bg-white p-6 rounded-lg shadow">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h3 className="text-xl font-semibold">{project.title}</h3>
              <p className="text-gray-600">{project.description}</p>
            </div>
            <span className={`px-3 py-1 text-sm rounded-full ${
              project.status === 'Completed' ? 'bg-green-100 text-green-800' :
              project.status === 'In Progress' ? 'bg-blue-100 text-blue-800' :
              'bg-yellow-100 text-yellow-800'
            }`}>
              {project.status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div>
              <h4 className="font-medium mb-2">Project Timeline</h4>
              <div className="space-y-2">
                <p className="text-sm"><span className="font-medium">Started:</span> {project.startDate}</p>
                {project.completionDate ? (
                  <p className="text-sm"><span className="font-medium">Completed:</span> {project.completionDate}</p>
                ) : (
                  <p className="text-sm"><span className="font-medium">Est. Completion:</span> {project.estimatedCompletion}</p>
                )}
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div
                    className={`h-2 rounded-full ${
                      project.status === 'Completed' ? 'bg-green-500' : 'bg-blue-500'
                    }`}
                    style={{ width: `${project.progress}%` }}
                  />
                </div>
                <p className="text-sm text-right">{project.progress}% complete</p>
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-2">Service Providers</h4>
              <div className="space-y-2">
                {project.serviceProviders.map((sp, index) => (
                  <div key={index} className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-2 ${
                      sp.status === 'Active' ? 'bg-blue-500' :
                      sp.status === 'Completed' ? 'bg-green-500' :
                      'bg-gray-300'
                    }`} />
                    <div>
                      <p className="text-sm font-medium">{sp.name}</p>
                      <p className="text-xs text-gray-500">{serviceProviders[sp.type].name} • {sp.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-2">Project Budget</h4>
              <p className="text-lg font-semibold">{project.budget}</p>
              <button className="mt-2 text-sm text-blue-600 hover:text-blue-800">
                View payment schedule
              </button>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="font-medium mb-3">Project Milestones</h4>
            <div className="space-y-3">
              {project.milestones.map((milestone, index) => (
                <div key={index} className="flex items-start">
                  <div className={`mt-1 mr-3 ${
                    milestone.completed ? 'text-green-500' : 
                    milestone.status === 'In Progress' ? 'text-blue-500' : 'text-gray-300'
                  }`}>
                    {milestone.completed ? (
                      <FiCheckCircle className="text-lg" />
                    ) : milestone.status === 'In Progress' ? (
                      <FiClock className="text-lg" />
                    ) : (
                      <div className="w-4 h-4 border-2 border-gray-300 rounded-full" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <p className={`font-medium ${
                        milestone.completed ? 'text-green-700' : 
                        milestone.status === 'In Progress' ? 'text-blue-700' : 'text-gray-700'
                      }`}>
                        {milestone.name}
                      </p>
                      {milestone.date && (
                        <span className="text-xs text-gray-500">{milestone.date}</span>
                      )}
                    </div>
                    {milestone.status === 'In Progress' && (
                      <p className="text-xs text-blue-600 mt-1">Work in progress</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {project.pendingApprovals && project.pendingApprovals.length > 0 && (
            <div className="mb-6">
              <h4 className="font-medium mb-3">Pending Approvals</h4>
              <div className="space-y-4">
                {project.pendingApprovals.map((approval, index) => {
                  const approvalKey = `${project.id}-${approval.title}`;
                  const status = approvalStatus[approvalKey] || 'pending';
                  
                  return (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-medium">{approval.title}</h5>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          status === 'approved' ? 'bg-green-100 text-green-800' :
                          status === 'revision' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {status === 'approved' ? 'Approved' : 
                           status === 'revision' ? 'Revision Requested' : 'Pending'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{approval.description}</p>
                      <p className="text-sm mb-3"><span className="font-medium">From:</span> {approval.provider}</p>
                      
                      <div className="mb-4">
                        <h6 className="text-sm font-medium mb-2">Documents for Review:</h6>
                        <div className="space-y-2">
                          {approval.documents.map((doc, docIndex) => (
                            <div key={docIndex} className="flex items-center text-sm text-gray-700">
                              <FiDownload className="mr-2 text-gray-500" />
                              <span>{doc}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {status === 'pending' && (
                        <div className="flex space-x-3">
                          <button
                            onClick={() => handleApprove(project.id, approval.title)}
                            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleRequestRevision(project.id, approval.title)}
                            className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 text-sm"
                          >
                            Request Revision
                          </button>
                          <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 text-sm">
                            View Details
                          </button>
                        </div>
                      )}

                      {status === 'approved' && (
                        <div className="text-sm text-green-600 flex items-center">
                          <FiCheckCircle className="mr-1" /> You approved this on {new Date().toLocaleDateString()}
                        </div>
                      )}

                      {status === 'revision' && (
                        <div className="text-sm text-yellow-600 flex items-center">
                          <FiAlertCircle className="mr-1" /> You requested revisions on {new Date().toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div>
            <h4 className="font-medium mb-3">Project Documents</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {project.documents.map((doc, index) => (
                <div key={index} className="border rounded-lg p-3 hover:bg-gray-50">
                  <div className="flex items-center mb-2">
                    <div className="bg-blue-100 p-2 rounded-full mr-3">
                      <FiUpload className="text-blue-600" />
                    </div>
                    <div>
                      <p className="font-medium text-sm truncate">{doc.name}</p>
                      <p className="text-xs text-gray-500">{doc.type} • {doc.date}</p>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      View
                    </button>
                    <button className="text-xs text-blue-600 hover:text-blue-800">
                      Download
                    </button>
                  </div>
                </div>
              ))}
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 flex flex-col items-center justify-center hover:bg-gray-50 cursor-pointer">
                <FiUpload className="text-gray-400 text-xl mb-2" />
                <p className="text-sm text-gray-600 text-center">Upload new document</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderPayments = () => (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Payment Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="border rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Total Projects</h4>
            <p className="text-2xl font-bold">{projects.length}</p>
          </div>
          <div className="border rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Total Invested</h4>
            <p className="text-2xl font-bold">KES 13,450,000</p>
          </div>
          <div className="border rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Upcoming Payment</h4>
            <p className="text-2xl font-bold">KES 1,200,000</p>
            <p className="text-sm text-gray-500 mt-1">Due on 2025-06-15</p>
          </div>
        </div>

        <h4 className="font-medium mb-3">Recent Transactions</h4>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Project</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Receipt</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2025-05-10</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">Office Renovation</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">KES 800,000</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Completed</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 hover:text-blue-800">
                  <a href="#">Download</a>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2025-04-25</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">Residential House</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">KES 2,500,000</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Completed</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 hover:text-blue-800">
                  <a href="#">Download</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderMessages = () => (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Messages</h3>
      <div className="text-center py-10">
        <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <FiMessageSquare className="text-gray-400 text-2xl" />
        </div>
        <h4 className="text-lg font-medium text-gray-700 mb-1">No new messages</h4>
        <p className="text-gray-500">Your conversation history with service providers will appear here.</p>
        <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Start New Conversation
        </button>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-6">Account Settings</h3>
      
      <div className="space-y-6">
        <div>
          <h4 className="font-medium mb-3">Profile Information</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                type="text"
                defaultValue="John Mwangi"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                defaultValue="john.mwangi@example.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
              <input
                type="tel"
                defaultValue="+254712345678"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Update Profile
          </button>
        </div>

        <div className="border-t pt-6">
          <h4 className="font-medium mb-3">Change Password</h4>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <input
                type="password"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input
                type="password"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
              <input
                type="password"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
              Change Password
            </button>
          </div>
        </div>

        <div className="border-t pt-6">
          <h4 className="font-medium mb-3">Account Actions</h4>
          <div className="space-y-3">
            <button 
              onClick={handleLogout}
              className="flex items-center text-red-600 hover:text-red-800"
            >
              <FiLogOut className="mr-2" /> Log Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'home':
        return renderHome();
      case 'projects':
        return renderProjects();
      case 'payments':
        return renderPayments();
      case 'messages':
        return renderMessages();
      case 'settings':
        return renderSettings();
      default:
        return null;
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md hidden md:block">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-blue-700 mb-8">Jagedo Dashboard</h1>
          <nav className="space-y-2">
            <button
              onClick={() => setActiveTab('home')}
              className={`w-full flex items-center px-4 py-3 rounded-lg ${
                activeTab === 'home' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiHome className="mr-3 text-lg" />
              Home
            </button>
            <button
              onClick={() => setActiveTab('projects')}
              className={`w-full flex items-center px-4 py-3 rounded-lg ${
                activeTab === 'projects' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiFolder className="mr-3 text-lg" />
              My Projects
            </button>
            <button
              onClick={() => setActiveTab('payments')}
              className={`w-full flex items-center px-4 py-3 rounded-lg ${
                activeTab === 'payments' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiDollarSign className="mr-3 text-lg" />
              Payments
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`w-full flex items-center px-4 py-3 rounded-lg ${
                activeTab === 'messages' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiMessageSquare className="mr-3 text-lg" />
              Messages
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`w-full flex items-center px-4 py-3 rounded-lg ${
                activeTab === 'settings' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiSettings className="mr-3 text-lg" />
              Settings
            </button>
          </nav>
        </div>
        <div className="p-6 border-t">
          <button
            onClick={handleLogout}
            className="w-full flex items-center px-4 py-3 rounded-lg text-gray-600 hover:bg-gray-100"
          >
            <FiLogOut className="mr-3 text-lg" />
            Log Out
          </button>
        </div>
      </aside>

      {/* Mobile bottom navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white shadow-lg md:hidden">
        <div className="flex justify-around">
          <button
            onClick={() => setActiveTab('home')}
            className={`flex flex-col items-center p-3 ${activeTab === 'home' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <FiHome className="text-lg" />
            <span className="text-xs mt-1">Home</span>
          </button>
          <button
            onClick={() => setActiveTab('projects')}
            className={`flex flex-col items-center p-3 ${activeTab === 'projects' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <FiFolder className="text-lg" />
            <span className="text-xs mt-1">Projects</span>
          </button>
          <button
            onClick={() => setActiveTab('payments')}
            className={`flex flex-col items-center p-3 ${activeTab === 'payments' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <FiDollarSign className="text-lg" />
            <span className="text-xs mt-1">Payments</span>
          </button>
          <button
            onClick={() => setActiveTab('messages')}
            className={`flex flex-col items-center p-3 ${activeTab === 'messages' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <FiMessageSquare className="text-lg" />
            <span className="text-xs mt-1">Messages</span>
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex flex-col items-center p-3 ${activeTab === 'settings' ? 'text-blue-600' : 'text-gray-500'}`}
          >
            <FiSettings className="text-lg" />
            <span className="text-xs mt-1">Settings</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 pb-16 md:pb-0">
        <div className="p-4 md:p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl md:text-2xl font-bold capitalize">
              {activeTab === 'home' ? 'Dashboard Overview' : activeTab}
            </h2>
            <div className="md:hidden">
              <button
                onClick={handleLogout}
                className="text-sm text-gray-600 hover:text-gray-800"
              >
                <FiLogOut className="text-lg" />
              </button>
            </div>
          </div>
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default CustomerDashboard;