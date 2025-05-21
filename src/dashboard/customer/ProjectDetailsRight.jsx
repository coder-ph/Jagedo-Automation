// ProjectDetailsRight.jsx
import React from 'react';
import ProjectFilesSection from './ProjectFilesSection';

const ProjectDetailsRight = ({
  selectedProject,
  projectStatuses,
  isApproving,
  isRejecting,
  rejectionReason,
  approveProject,
  setIsRejecting,
  setRejectionReason,
  rejectProject
}) => {
  return (
    <div className="space-y-6">
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Project Details</h3>
        <div className="space-y-3">
          <div>
            <span className="text-sm text-gray-500">Status</span>
            <p className={`text-sm font-medium ${projectStatuses[selectedProject.status].color} px-2 py-1 rounded-full inline-block`}>
              {projectStatuses[selectedProject.status].label}
            </p>
          </div>
          <div>
            <span className="text-sm text-gray-500">Service Type</span>
            <p className="text-sm font-medium text-gray-900">{selectedProject.serviceType}</p>
          </div>
          <div>
            <span className="text-sm text-gray-500">Service Provider</span>
            <p className="text-sm font-medium text-gray-900">{selectedProject.provider}</p>
          </div>
          <div>
            <span className="text-sm text-gray-500">Location</span>
            <p className="text-sm font-medium text-gray-900">{selectedProject.location}</p>
          </div>
          <div>
            <span className="text-sm text-gray-500">Budget</span>
            <p className="text-sm font-medium text-gray-900">{selectedProject.budget}</p>
          </div>
          <div>
            <span className="text-sm text-gray-500">Start Date</span>
            <p className="text-sm font-medium text-gray-900">{selectedProject.startDate}</p>
          </div>
          {selectedProject.estimatedCompletion && (
            <div>
              <span className="text-sm text-gray-500">Estimated Completion</span>
              <p className="text-sm font-medium text-gray-900">{selectedProject.estimatedCompletion}</p>
            </div>
          )}
          {selectedProject.completionDate && (
            <div>
              <span className="text-sm text-gray-500">Actual Completion</span>
              <p className="text-sm font-medium text-gray-900">{selectedProject.completionDate}</p>
            </div>
          )}
          {selectedProject.approvalDate && (
            <div>
              <span className="text-sm text-gray-500">Approval Date</span>
              <p className="text-sm font-medium text-gray-900">{selectedProject.approvalDate}</p>
            </div>
          )}
        </div>
      </div>

      <ProjectFilesSection selectedProject={selectedProject} />

      {selectedProject.status === 'COMPLETED' && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-3">Project Completion</h3>
          <p className="text-sm text-gray-700 mb-4">
            The service provider has marked this project as completed. Please review the work and either approve or reject it.
          </p>
          <div className="flex space-x-3">
            <button
              onClick={() => {
                setRejectionReason('');
                setIsRejecting(false);
                setIsApproving(true);
                setTimeout(approveProject, 1000);
              }}
              disabled={isApproving || isRejecting}
              className={`flex-1 px-4 py-2 rounded-md text-white ${isApproving ? 'bg-green-400' : 'bg-green-600 hover:bg-green-700'} transition-colors`}
            >
              {isApproving ? 'Approving...' : 'Approve Project'}
            </button>
            <button
              onClick={() => setIsRejecting(!isRejecting)}
              disabled={isApproving || isRejecting}
              className={`flex-1 px-4 py-2 rounded-md text-white ${isRejecting ? 'bg-red-400' : 'bg-red-600 hover:bg-red-700'} transition-colors`}
            >
              {isRejecting ? 'Cancel' : 'Reject Project'}
            </button>
          </div>
          {isRejecting && (
            <div className="mt-4">
              <label htmlFor="rejectionReason" className="block text-sm font-medium text-gray-700 mb-1">
                Reason for Rejection
              </label>
              <textarea
                id="rejectionReason"
                rows="3"
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-red-500 focus:border-red-500"
                placeholder="Please explain why you're rejecting this work..."
              ></textarea>
              <button
                onClick={rejectProject}
                disabled={!rejectionReason.trim()}
                className="mt-2 w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-red-300 transition-colors"
              >
                Submit Rejection
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProjectDetailsRight;