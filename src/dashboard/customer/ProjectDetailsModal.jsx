// ProjectDetailsModal.jsx
import React from 'react';
import ProjectDetailsLeft from './ProjectDetailsLeft';
import ProjectDetailsRight from './ProjectDetailsRight';

const ProjectDetailsModal = ({
  selectedProject,
  projectStatuses,
  isApproving,
  isRejecting,
  rejectionReason,
  newMessage,
  setNewMessage,
  sendMessage,
  approveProject,
  setIsRejecting,
  setRejectionReason,
  rejectProject,
  setIsViewingDetails,
  setSelectedProject
}) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{selectedProject.title}</h2>
              <p className="text-sm text-gray-500 mt-1">
                {selectedProject.serviceType} • {selectedProject.provider} • {selectedProject.budget}
              </p>
            </div>
            <button
              onClick={() => {
                setIsViewingDetails(false);
                setSelectedProject(null);
              }}
              className="text-gray-400 hover:text-gray-500"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <ProjectDetailsLeft 
              selectedProject={selectedProject} 
              newMessage={newMessage} 
              setNewMessage={setNewMessage} 
              sendMessage={sendMessage} 
            />
            
            <ProjectDetailsRight 
              selectedProject={selectedProject} 
              projectStatuses={projectStatuses} 
              isApproving={isApproving} 
              isRejecting={isRejecting} 
              rejectionReason={rejectionReason} 
              approveProject={approveProject} 
              setIsRejecting={setIsRejecting} 
              setRejectionReason={setRejectionReason} 
              rejectProject={rejectProject} 
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailsModal;