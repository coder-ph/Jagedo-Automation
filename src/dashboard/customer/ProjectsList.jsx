// ProjectsList.jsx
import React from 'react';
import EmptyState from './EmptyState';

const ProjectsList = ({ filteredProjects, activeTab, projectStatuses, viewProjectDetails, viewProjectFiles, navigate }) => {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      {filteredProjects.length === 0 ? (
        <EmptyState activeTab={activeTab} navigate={navigate} />
      ) : (
        <ul className="divide-y divide-gray-200">
          {filteredProjects.map((project) => (
            <li key={project.id} className="p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${projectStatuses[project.status].color}`}>
                    <span className="text-xs font-medium">
                      {projectStatuses[project.status].label.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">{project.title}</h3>
                    <p className="text-sm text-gray-500">
                      {project.serviceType} • {project.provider} • {project.budget}
                    </p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => viewProjectFiles(project)}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
                  >
                    View Files
                  </button>
                  <button
                    onClick={() => viewProjectDetails(project)}
                    className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-md text-sm hover:bg-indigo-200 transition-colors"
                  >
                    View Details
                  </button>
                </div>
              </div>
              <div className="mt-2 flex justify-between items-center">
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs rounded-full ${projectStatuses[project.status].color}`}>
                    {projectStatuses[project.status].label}
                  </span>
                  <span className="text-xs text-gray-500">
                    Started: {project.startDate}
                    {project.estimatedCompletion && ` • Est. Completion: ${project.estimatedCompletion}`}
                  </span>
                </div>
                {project.completionDate && (
                  <span className="text-xs text-gray-500">
                    Completed: {project.completionDate}
                  </span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ProjectsList;