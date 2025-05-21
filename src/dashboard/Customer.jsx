// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';

// const projectStatuses = {
//   PENDING: { label: 'Pending', color: 'bg-yellow-100 text-yellow-800' },
//   IN_PROGRESS: { label: 'In Progress', color: 'bg-blue-100 text-blue-800' },
//   COMPLETED: { label: 'Completed', color: 'bg-green-100 text-green-800' },
//   APPROVED: { label: 'Approved', color: 'bg-purple-100 text-purple-800' },
//   REJECTED: { label: 'Rejected', color: 'bg-red-100 text-red-800' }
// };

// const CustomerDashboard = () => {
//   const navigate = useNavigate();
//   const [activeTab, setActiveTab] = useState('active');
//   const [projects, setProjects] = useState([]);
//   const [selectedProject, setSelectedProject] = useState(null);
//   const [isViewingDetails, setIsViewingDetails] = useState(false);
//   const [isViewingFiles, setIsViewingFiles] = useState(false);
//   const [newMessage, setNewMessage] = useState('');
//   const [isApproving, setIsApproving] = useState(false);
//   const [isRejecting, setIsRejecting] = useState(false);
//   const [rejectionReason, setRejectionReason] = useState('');

//   // Mock data - in a real app, this would come from an API
//   useEffect(() => {
//     const mockProjects = [
//       {
//         id: '1',
//         title: 'Home Plumbing Repair',
//         serviceType: 'Fundi',
//         provider: 'John Plumbing Services',
//         status: 'IN_PROGRESS',
//         budget: '15,000 Ksh',
//         startDate: '2023-06-15',
//         estimatedCompletion: '2023-06-25',
//         location: 'Nairobi, Kilimani',
//         description: 'Fixing leaking pipes in the kitchen and bathroom, installing new faucets',
//         files: [
//           { name: 'plumbing_quote.pdf', type: 'pdf', size: '2.4MB', uploaded: '2023-06-10' },
//           { name: 'kitchen_layout.jpg', type: 'image', size: '1.2MB', uploaded: '2023-06-11' }
//         ],
//         updates: [
//           { 
//             date: '2023-06-16', 
//             message: 'Initial assessment completed. Materials ordered.', 
//             sender: 'provider',
//             attachments: []
//           },
//           { 
//             date: '2023-06-18', 
//             message: 'Materials delivered. Work started on kitchen pipes.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'materials_delivered.jpg', type: 'image', size: '0.8MB' }
//             ]
//           }
//         ]
//       },
//       {
//         id: '2',
//         title: 'Office Electrical Wiring',
//         serviceType: 'Professional',
//         provider: 'ElectroTech Solutions',
//         status: 'COMPLETED',
//         budget: '45,000 Ksh',
//         startDate: '2023-05-20',
//         estimatedCompletion: '2023-06-10',
//         completionDate: '2023-06-08',
//         location: 'Nairobi, Westlands',
//         description: 'Complete rewiring of office space, installation of new sockets and lighting',
//         files: [
//           { name: 'electrical_plan.pdf', type: 'pdf', size: '3.1MB', uploaded: '2023-05-15' },
//           { name: 'materials_list.pdf', type: 'pdf', size: '0.5MB', uploaded: '2023-05-18' }
//         ],
//         updates: [
//           { 
//             date: '2023-05-22', 
//             message: 'Initial wiring completed. Waiting for inspection.', 
//             sender: 'provider',
//             attachments: []
//           },
//           { 
//             date: '2023-06-05', 
//             message: 'Inspection passed. Finalizing installations.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'inspection_report.pdf', type: 'pdf', size: '1.5MB' }
//             ]
//           },
//           { 
//             date: '2023-06-08', 
//             message: 'Project completed. Please review and approve.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'final_work.jpg', type: 'image', size: '2.1MB' },
//               { name: 'completion_certificate.pdf', type: 'pdf', size: '0.7MB' }
//             ]
//           }
//         ]
//       },
//       {
//         id: '3',
//         title: 'Garden Landscaping',
//         serviceType: 'Contractor',
//         provider: 'GreenScape Ltd',
//         status: 'APPROVED',
//         budget: '75,000 Ksh',
//         startDate: '2023-04-10',
//         estimatedCompletion: '2023-05-15',
//         completionDate: '2023-05-12',
//         approvalDate: '2023-05-18',
//         location: 'Nairobi, Karen',
//         description: 'Complete garden redesign including new plants, irrigation system, and stone pathways',
//         files: [
//           { name: 'landscape_design.pdf', type: 'pdf', size: '5.2MB', uploaded: '2023-04-05' },
//           { name: 'plant_selection.jpg', type: 'image', size: '1.8MB', uploaded: '2023-04-07' }
//         ],
//         updates: [
//           { 
//             date: '2023-04-12', 
//             message: 'Site preparation completed. Materials delivered.', 
//             sender: 'provider',
//             attachments: []
//           },
//           { 
//             date: '2023-04-25', 
//             message: 'Irrigation system installed. Starting on pathways.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'irrigation_system.jpg', type: 'image', size: '1.5MB' }
//             ]
//           },
//           { 
//             date: '2023-05-10', 
//             message: 'Planting completed. Final touches in progress.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'planting_progress.jpg', type: 'image', size: '2.3MB' }
//             ]
//           },
//           { 
//             date: '2023-05-12', 
//             message: 'Project completed. Awaiting your approval.', 
//             sender: 'provider',
//             attachments: [
//               { name: 'final_garden.jpg', type: 'image', size: '3.1MB' }
//             ]
//           }
//         ]
//       }
//     ];
//     setProjects(mockProjects);
//   }, []);

//   const filteredProjects = projects.filter(project => {
//     if (activeTab === 'active') {
//       return project.status !== 'COMPLETED' && project.status !== 'APPROVED' && project.status !== 'REJECTED';
//     } else if (activeTab === 'completed') {
//       return project.status === 'COMPLETED';
//     } else if (activeTab === 'approved') {
//       return project.status === 'APPROVED';
//     } else if (activeTab === 'rejected') {
//       return project.status === 'REJECTED';
//     }
//     return true;
//   });

//   const viewProjectDetails = (project) => {
//     setSelectedProject(project);
//     setIsViewingDetails(true);
//   };

//   const viewProjectFiles = (project) => {
//     setSelectedProject(project);
//     setIsViewingFiles(true);
//   };

//   const sendMessage = () => {
//     if (!newMessage.trim()) return;
    
//     const updatedProject = {
//       ...selectedProject,
//       updates: [
//         ...selectedProject.updates,
//         {
//           date: new Date().toISOString().split('T')[0],
//           message: newMessage,
//           sender: 'customer',
//           attachments: []
//         }
//       ]
//     };
    
//     setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
//     setSelectedProject(updatedProject);
//     setNewMessage('');
//     toast.success('Message sent successfully!');
//   };

//   const approveProject = () => {
//     setIsApproving(true);
//     // In a real app, this would be an API call
//     setTimeout(() => {
//       const updatedProject = {
//         ...selectedProject,
//         status: 'APPROVED',
//         approvalDate: new Date().toISOString().split('T')[0],
//         updates: [
//           ...selectedProject.updates,
//           {
//             date: new Date().toISOString().split('T')[0],
//             message: 'Customer approved the completed work.',
//             sender: 'system',
//             attachments: []
//           }
//         ]
//       };
      
//       setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
//       setSelectedProject(updatedProject);
//       setIsApproving(false);
//       setIsViewingDetails(false);
//       toast.success('Project approved successfully!');
//     }, 1000);
//   };

//   const rejectProject = () => {
//     if (!rejectionReason.trim()) {
//       toast.error('Please provide a reason for rejection');
//       return;
//     }
    
//     setIsRejecting(true);
//     // In a real app, this would be an API call
//     setTimeout(() => {
//       const updatedProject = {
//         ...selectedProject,
//         status: 'REJECTED',
//         updates: [
//           ...selectedProject.updates,
//           {
//             date: new Date().toISOString().split('T')[0],
//             message: `Customer rejected the completed work. Reason: ${rejectionReason}`,
//             sender: 'system',
//             attachments: []
//           }
//         ]
//       };
      
//       setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
//       setSelectedProject(updatedProject);
//       setIsRejecting(false);
//       setRejectionReason('');
//       setIsViewingDetails(false);
//       toast.success('Project rejected. The service provider has been notified.');
//     }, 1000);
//   };

//   const getFileIcon = (fileType) => {
//     switch (fileType) {
//       case 'pdf':
//         return (
//           <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
//           </svg>
//         );
//       case 'image':
//         return (
//           <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
//           </svg>
//         );
//       default:
//         return (
//           <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
//           </svg>
//         );
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gray-50">
//       <ToastContainer position="top-center" autoClose={3000} />
      
//       {/* Header */}
//       <header className="bg-white shadow-sm">
//         <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
//           <h1 className="text-2xl font-bold text-gray-900">Customer Dashboard</h1>
//           <button
//             onClick={() => navigate('/create-request')}
//             className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-md hover:from-indigo-700 hover:to-purple-700 transition-colors"
//           >
//             + New Request
//           </button>
//         </div>
//       </header>

//       {/* Main Content */}
//       <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
//         {/* Tabs */}
//         <div className="border-b border-gray-200 mb-6">
//           <nav className="-mb-px flex space-x-8">
//             <button
//               onClick={() => setActiveTab('active')}
//               className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'active' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
//             >
//               Active Projects
//             </button>
//             <button
//               onClick={() => setActiveTab('completed')}
//               className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'completed' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
//             >
//               Completed (Pending Approval)
//             </button>
//             <button
//               onClick={() => setActiveTab('approved')}
//               className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'approved' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
//             >
//               Approved Projects
//             </button>
//             <button
//               onClick={() => setActiveTab('rejected')}
//               className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'rejected' ? 'border-indigo-500 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
//             >
//               Rejected Projects
//             </button>
//           </nav>
//         </div>

//         {/* Projects List */}
//         <div className="bg-white shadow rounded-lg overflow-hidden">
//           {filteredProjects.length === 0 ? (
//             <div className="p-8 text-center">
//               <svg
//                 className="mx-auto h-12 w-12 text-gray-400"
//                 fill="none"
//                 viewBox="0 0 24 24"
//                 stroke="currentColor"
//                 aria-hidden="true"
//               >
//                 <path
//                   strokeLinecap="round"
//                   strokeLinejoin="round"
//                   strokeWidth="2"
//                   d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
//                 />
//               </svg>
//               <h3 className="mt-2 text-sm font-medium text-gray-900">No projects found</h3>
//               <p className="mt-1 text-sm text-gray-500">
//                 {activeTab === 'active'
//                   ? 'You currently have no active projects.'
//                   : activeTab === 'completed'
//                   ? 'You have no projects pending approval.'
//                   : activeTab === 'approved'
//                   ? 'You have no approved projects.'
//                   : 'You have no rejected projects.'}
//               </p>
//               <div className="mt-6">
//                 <button
//                   onClick={() => navigate('/create-request')}
//                   className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
//                 >
//                   <svg
//                     className="-ml-1 mr-2 h-5 w-5"
//                     xmlns="http://www.w3.org/2000/svg"
//                     viewBox="0 0 20 20"
//                     fill="currentColor"
//                     aria-hidden="true"
//                   >
//                     <path
//                       fillRule="evenodd"
//                       d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
//                       clipRule="evenodd"
//                     />
//                   </svg>
//                   New Service Request
//                 </button>
//               </div>
//             </div>
//           ) : (
//             <ul className="divide-y divide-gray-200">
//               {filteredProjects.map((project) => (
//                 <li key={project.id} className="p-4 hover:bg-gray-50 transition-colors">
//                   <div className="flex items-center justify-between">
//                     <div className="flex items-center space-x-4">
//                       <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${projectStatuses[project.status].color}`}>
//                         <span className="text-xs font-medium">
//                           {projectStatuses[project.status].label.charAt(0)}
//                         </span>
//                       </div>
//                       <div>
//                         <h3 className="text-lg font-medium text-gray-900">{project.title}</h3>
//                         <p className="text-sm text-gray-500">
//                           {project.serviceType} • {project.provider} • {project.budget}
//                         </p>
//                       </div>
//                     </div>
//                     <div className="flex space-x-2">
//                       <button
//                         onClick={() => viewProjectFiles(project)}
//                         className="px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
//                       >
//                         View Files
//                       </button>
//                       <button
//                         onClick={() => viewProjectDetails(project)}
//                         className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-md text-sm hover:bg-indigo-200 transition-colors"
//                       >
//                         View Details
//                       </button>
//                     </div>
//                   </div>
//                   <div className="mt-2 flex justify-between items-center">
//                     <div className="flex items-center space-x-2">
//                       <span className={`px-2 py-1 text-xs rounded-full ${projectStatuses[project.status].color}`}>
//                         {projectStatuses[project.status].label}
//                       </span>
//                       <span className="text-xs text-gray-500">
//                         Started: {project.startDate}
//                         {project.estimatedCompletion && ` • Est. Completion: ${project.estimatedCompletion}`}
//                       </span>
//                     </div>
//                     {project.completionDate && (
//                       <span className="text-xs text-gray-500">
//                         Completed: {project.completionDate}
//                       </span>
//                     )}
//                   </div>
//                 </li>
//               ))}
//             </ul>
//           )}
//         </div>
//       </main>

//       {/* Project Details Modal */}
//       {isViewingDetails && selectedProject && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//           <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
//             <div className="p-6">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h2 className="text-2xl font-bold text-gray-900">{selectedProject.title}</h2>
//                   <p className="text-sm text-gray-500 mt-1">
//                     {selectedProject.serviceType} • {selectedProject.provider} • {selectedProject.budget}
//                   </p>
//                 </div>
//                 <button
//                   onClick={() => {
//                     setIsViewingDetails(false);
//                     setSelectedProject(null);
//                   }}
//                   className="text-gray-400 hover:text-gray-500"
//                 >
//                   <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
//                   </svg>
//                 </button>
//               </div>

//               <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
//                 <div className="md:col-span-2">
//                   <div className="bg-gray-50 p-4 rounded-lg">
//                     <h3 className="text-lg font-medium text-gray-900 mb-3">Project Description</h3>
//                     <p className="text-gray-700">{selectedProject.description}</p>
//                   </div>

//                   <div className="mt-6">
//                     <h3 className="text-lg font-medium text-gray-900 mb-3">Project Updates</h3>
//                     <div className="space-y-4">
//                       {selectedProject.updates.map((update, index) => (
//                         <div
//                           key={index}
//                           className={`p-4 rounded-lg ${update.sender === 'customer' ? 'bg-indigo-50' : update.sender === 'system' ? 'bg-gray-100' : 'bg-white border border-gray-200'}`}
//                         >
//                           <div className="flex justify-between items-start">
//                             <div>
//                               <span className="text-sm font-medium">
//                                 {update.sender === 'customer' ? 'You' : update.sender === 'system' ? 'System' : selectedProject.provider}
//                               </span>
//                               <span className="text-xs text-gray-500 ml-2">{update.date}</span>
//                             </div>
//                             {update.sender === 'provider' && (
//                               <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">Provider</span>
//                             )}
//                           </div>
//                           <p className="mt-1 text-gray-700">{update.message}</p>
//                           {update.attachments.length > 0 && (
//                             <div className="mt-2">
//                               <h4 className="text-xs font-medium text-gray-500 mb-1">Attachments:</h4>
//                               <div className="flex flex-wrap gap-2">
//                                 {update.attachments.map((file, fileIndex) => (
//                                   <div
//                                     key={fileIndex}
//                                     className="flex items-center space-x-2 p-2 bg-white rounded border border-gray-200 text-xs"
//                                   >
//                                     {getFileIcon(file.type)}
//                                     <div>
//                                       <p className="font-medium truncate max-w-xs">{file.name}</p>
//                                       <p className="text-gray-500">{file.size}</p>
//                                     </div>
//                                   </div>
//                                 ))}
//                               </div>
//                             </div>
//                           )}
//                         </div>
//                       ))}
//                     </div>

//                     <div className="mt-6">
//                       <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
//                         Send Message to Provider
//                       </label>
//                       <div className="flex space-x-2">
//                         <input
//                           type="text"
//                           id="message"
//                           value={newMessage}
//                           onChange={(e) => setNewMessage(e.target.value)}
//                           placeholder="Type your message here..."
//                           className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
//                         />
//                         <button
//                           onClick={sendMessage}
//                           className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
//                         >
//                           Send
//                         </button>
//                       </div>
//                     </div>
//                   </div>
//                 </div>

//                 <div className="space-y-6">
//                   <div className="bg-white border border-gray-200 rounded-lg p-4">
//                     <h3 className="text-lg font-medium text-gray-900 mb-3">Project Details</h3>
//                     <div className="space-y-3">
//                       <div>
//                         <span className="text-sm text-gray-500">Status</span>
//                         <p className={`text-sm font-medium ${projectStatuses[selectedProject.status].color} px-2 py-1 rounded-full inline-block`}>
//                           {projectStatuses[selectedProject.status].label}
//                         </p>
//                       </div>
//                       <div>
//                         <span className="text-sm text-gray-500">Service Type</span>
//                         <p className="text-sm font-medium text-gray-900">{selectedProject.serviceType}</p>
//                       </div>
//                       <div>
//                         <span className="text-sm text-gray-500">Service Provider</span>
//                         <p className="text-sm font-medium text-gray-900">{selectedProject.provider}</p>
//                       </div>
//                       <div>
//                         <span className="text-sm text-gray-500">Location</span>
//                         <p className="text-sm font-medium text-gray-900">{selectedProject.location}</p>
//                       </div>
//                       <div>
//                         <span className="text-sm text-gray-500">Budget</span>
//                         <p className="text-sm font-medium text-gray-900">{selectedProject.budget}</p>
//                       </div>
//                       <div>
//                         <span className="text-sm text-gray-500">Start Date</span>
//                         <p className="text-sm font-medium text-gray-900">{selectedProject.startDate}</p>
//                       </div>
//                       {selectedProject.estimatedCompletion && (
//                         <div>
//                           <span className="text-sm text-gray-500">Estimated Completion</span>
//                           <p className="text-sm font-medium text-gray-900">{selectedProject.estimatedCompletion}</p>
//                         </div>
//                       )}
//                       {selectedProject.completionDate && (
//                         <div>
//                           <span className="text-sm text-gray-500">Actual Completion</span>
//                           <p className="text-sm font-medium text-gray-900">{selectedProject.completionDate}</p>
//                         </div>
//                       )}
//                       {selectedProject.approvalDate && (
//                         <div>
//                           <span className="text-sm text-gray-500">Approval Date</span>
//                           <p className="text-sm font-medium text-gray-900">{selectedProject.approvalDate}</p>
//                         </div>
//                       )}
//                     </div>
//                   </div>

//                   <div className="bg-white border border-gray-200 rounded-lg p-4">
//                     <h3 className="text-lg font-medium text-gray-900 mb-3">Project Files</h3>
//                     <div className="space-y-2">
//                       {selectedProject.files.map((file, index) => (
//                         <div
//                           key={index}
//                           className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded cursor-pointer"
//                           onClick={() => {
//                             // In a real app, this would open the file
//                             toast.info(`Opening ${file.name}`);
//                           }}
//                         >
//                           {getFileIcon(file.type)}
//                           <div className="flex-1 min-w-0">
//                             <p className="text-sm font-medium text-gray-900 truncate">{file.name}</p>
//                             <p className="text-xs text-gray-500">{file.size} • Uploaded {file.uploaded}</p>
//                           </div>
//                           <button
//                             onClick={(e) => {
//                               e.stopPropagation();
//                               toast.info(`Downloading ${file.name}`);
//                             }}
//                             className="text-gray-400 hover:text-indigo-600"
//                           >
//                             <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
//                             </svg>
//                           </button>
//                         </div>
//                       ))}
//                     </div>
//                   </div>

//                   {selectedProject.status === 'COMPLETED' && (
//                     <div className="bg-white border border-gray-200 rounded-lg p-4">
//                       <h3 className="text-lg font-medium text-gray-900 mb-3">Project Completion</h3>
//                       <p className="text-sm text-gray-700 mb-4">
//                         The service provider has marked this project as completed. Please review the work and either approve or reject it.
//                       </p>
//                       <div className="flex space-x-3">
//                         <button
//                           onClick={() => {
//                             setRejectionReason('');
//                             setIsRejecting(false);
//                             setIsApproving(true);
//                             setTimeout(approveProject, 1000);
//                           }}
//                           disabled={isApproving || isRejecting}
//                           className={`flex-1 px-4 py-2 rounded-md text-white ${isApproving ? 'bg-green-400' : 'bg-green-600 hover:bg-green-700'} transition-colors`}
//                         >
//                           {isApproving ? 'Approving...' : 'Approve Project'}
//                         </button>
//                         <button
//                           onClick={() => setIsRejecting(!isRejecting)}
//                           disabled={isApproving || isRejecting}
//                           className={`flex-1 px-4 py-2 rounded-md text-white ${isRejecting ? 'bg-red-400' : 'bg-red-600 hover:bg-red-700'} transition-colors`}
//                         >
//                           {isRejecting ? 'Cancel' : 'Reject Project'}
//                         </button>
//                       </div>
//                       {isRejecting && (
//                         <div className="mt-4">
//                           <label htmlFor="rejectionReason" className="block text-sm font-medium text-gray-700 mb-1">
//                             Reason for Rejection
//                           </label>
//                           <textarea
//                             id="rejectionReason"
//                             rows="3"
//                             value={rejectionReason}
//                             onChange={(e) => setRejectionReason(e.target.value)}
//                             className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-red-500 focus:border-red-500"
//                             placeholder="Please explain why you're rejecting this work..."
//                           ></textarea>
//                           <button
//                             onClick={rejectProject}
//                             disabled={!rejectionReason.trim()}
//                             className="mt-2 w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-red-300 transition-colors"
//                           >
//                             Submit Rejection
//                           </button>
//                         </div>
//                       )}
//                     </div>
//                   )}
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {/* Files Modal */}
//       {isViewingFiles && selectedProject && (
//         <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//           <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
//             <div className="p-6">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h2 className="text-2xl font-bold text-gray-900">Project Files</h2>
//                   <p className="text-sm text-gray-500 mt-1">{selectedProject.title}</p>
//                 </div>
//                 <button
//                   onClick={() => {
//                     setIsViewingFiles(false);
//                     setSelectedProject(null);
//                   }}
//                   className="text-gray-400 hover:text-gray-500"
//                 >
//                   <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
//                   </svg>
//                 </button>
//               </div>

//               <div className="mt-6">
//                 <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
//                   {selectedProject.files.map((file, index) => (
//                     <div
//                       key={index}
//                       className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
//                       onClick={() => {
//                         // In a real app, this would open the file
//                         toast.info(`Opening ${file.name}`);
//                       }}
//                     >
//                       <div className="flex flex-col items-center text-center">
//                         {getFileIcon(file.type)}
//                         <p className="mt-2 text-sm font-medium text-gray-900 truncate w-full">{file.name}</p>
//                         <p className="text-xs text-gray-500">{file.size}</p>
//                         <p className="text-xs text-gray-400 mt-1">Uploaded {file.uploaded}</p>
//                         <button
//                           onClick={(e) => {
//                             e.stopPropagation();
//                             toast.info(`Downloading ${file.name}`);
//                           }}
//                           className="mt-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
//                         >
//                           Download
//                         </button>
//                       </div>
//                     </div>
//                   ))}
//                 </div>

//                 {selectedProject.updates.some(update => update.attachments.length > 0) && (
//                   <>
//                     <h3 className="text-lg font-medium text-gray-900 mt-8 mb-4">Update Attachments</h3>
//                     <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
//                       {selectedProject.updates.map((update, updateIndex) =>
//                         update.attachments.map((file, fileIndex) => (
//                           <div
//                             key={`${updateIndex}-${fileIndex}`}
//                             className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
//                             onClick={() => {
//                               // In a real app, this would open the file
//                               toast.info(`Opening ${file.name}`);
//                             }}
//                           >
//                             <div className="flex flex-col items-center text-center">
//                               {getFileIcon(file.type)}
//                               <p className="mt-2 text-sm font-medium text-gray-900 truncate w-full">{file.name}</p>
//                               <p className="text-xs text-gray-500">{file.size}</p>
//                               <p className="text-xs text-gray-400 mt-1">Added {update.date}</p>
//                               <button
//                                 onClick={(e) => {
//                                   e.stopPropagation();
//                                   toast.info(`Downloading ${file.name}`);
//                                 }}
//                                 className="mt-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
//                               >
//                                 Download
//                               </button>
//                             </div>
//                           </div>
//                         ))
//                       )}
//                     </div>
//                   </>
//                 )}
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default CustomerDashboard;