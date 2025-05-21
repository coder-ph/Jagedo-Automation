// CustomerDashboard.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DashboardHeader from './DashboardHeader';
import ProjectsTabs from './ProjectsTabs';
import ProjectsList from './ProjectsList';
import ProjectDetailsModal from './ProjectDetailsModal';
import ProjectFilesModal from './ProjectFilesModal';

const projectStatuses = {
  PENDING: { label: 'Pending', color: 'bg-yellow-100 text-yellow-800' },
  IN_PROGRESS: { label: 'In Progress', color: 'bg-blue-100 text-blue-800' },
  COMPLETED: { label: 'Completed', color: 'bg-green-100 text-green-800' },
  APPROVED: { label: 'Approved', color: 'bg-purple-100 text-purple-800' },
  REJECTED: { label: 'Rejected', color: 'bg-red-100 text-red-800' }
};

const CustomerDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('active');
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [isViewingDetails, setIsViewingDetails] = useState(false);
  const [isViewingFiles, setIsViewingFiles] = useState(false);
  const [newMessage, setNewMessage] = useState('');
  const [isApproving, setIsApproving] = useState(false);
  const [isRejecting, setIsRejecting] = useState(false);
  const [rejectionReason, setRejectionReason] = useState('');

  useEffect(() => {
    // Mock data - in a real app, this would come from an API
    const mockProjects = [
      // ... (same mock data as before)
    ];
    setProjects(mockProjects);
  }, []);

  const filteredProjects = projects.filter(project => {
    if (activeTab === 'active') {
      return project.status !== 'COMPLETED' && project.status !== 'APPROVED' && project.status !== 'REJECTED';
    } else if (activeTab === 'completed') {
      return project.status === 'COMPLETED';
    } else if (activeTab === 'approved') {
      return project.status === 'APPROVED';
    } else if (activeTab === 'rejected') {
      return project.status === 'REJECTED';
    }
    return true;
  });

  const viewProjectDetails = (project) => {
    setSelectedProject(project);
    setIsViewingDetails(true);
  };

  const viewProjectFiles = (project) => {
    setSelectedProject(project);
    setIsViewingFiles(true);
  };

  const sendMessage = () => {
    if (!newMessage.trim()) return;
    
    const updatedProject = {
      ...selectedProject,
      updates: [
        ...selectedProject.updates,
        {
          date: new Date().toISOString().split('T')[0],
          message: newMessage,
          sender: 'customer',
          attachments: []
        }
      ]
    };
    
    setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
    setSelectedProject(updatedProject);
    setNewMessage('');
    toast.success('Message sent successfully!');
  };

  const approveProject = () => {
    setIsApproving(true);
    setTimeout(() => {
      const updatedProject = {
        ...selectedProject,
        status: 'APPROVED',
        approvalDate: new Date().toISOString().split('T')[0],
        updates: [
          ...selectedProject.updates,
          {
            date: new Date().toISOString().split('T')[0],
            message: 'Customer approved the completed work.',
            sender: 'system',
            attachments: []
          }
        ]
      };
      
      setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
      setSelectedProject(updatedProject);
      setIsApproving(false);
      setIsViewingDetails(false);
      toast.success('Project approved successfully!');
    }, 1000);
  };

  const rejectProject = () => {
    if (!rejectionReason.trim()) {
      toast.error('Please provide a reason for rejection');
      return;
    }
    
    setIsRejecting(true);
    setTimeout(() => {
      const updatedProject = {
        ...selectedProject,
        status: 'REJECTED',
        updates: [
          ...selectedProject.updates,
          {
            date: new Date().toISOString().split('T')[0],
            message: `Customer rejected the completed work. Reason: ${rejectionReason}`,
            sender: 'system',
            attachments: []
          }
        ]
      };
      
      setProjects(projects.map(p => p.id === updatedProject.id ? updatedProject : p));
      setSelectedProject(updatedProject);
      setIsRejecting(false);
      setRejectionReason('');
      setIsViewingDetails(false);
      toast.success('Project rejected. The service provider has been notified.');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <ToastContainer position="top-center" autoClose={3000} />
      
      <DashboardHeader navigate={navigate} />
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <ProjectsTabs activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <ProjectsList 
          filteredProjects={filteredProjects} 
          activeTab={activeTab} 
          projectStatuses={projectStatuses} 
          viewProjectDetails={viewProjectDetails} 
          viewProjectFiles={viewProjectFiles} 
          navigate={navigate}
        />
      </main>

      {isViewingDetails && selectedProject && (
        <ProjectDetailsModal
          selectedProject={selectedProject}
          projectStatuses={projectStatuses}
          isApproving={isApproving}
          isRejecting={isRejecting}
          rejectionReason={rejectionReason}
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          sendMessage={sendMessage}
          approveProject={approveProject}
          setIsRejecting={setIsRejecting}
          setRejectionReason={setRejectionReason}
          rejectProject={rejectProject}
          setIsViewingDetails={setIsViewingDetails}
          setSelectedProject={setSelectedProject}
        />
      )}

      {isViewingFiles && selectedProject && (
        <ProjectFilesModal
          selectedProject={selectedProject}
          setIsViewingFiles={setIsViewingFiles}
          setSelectedProject={setSelectedProject}
        />
      )}
    </div>
  );
};

export default CustomerDashboard;