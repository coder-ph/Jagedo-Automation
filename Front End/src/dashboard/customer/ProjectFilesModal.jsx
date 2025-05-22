// ProjectFilesModal.jsx
import React from 'react';

const ProjectFilesModal = ({ selectedProject, setIsViewingFiles, setSelectedProject }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Project Files</h2>
              <p className="text-sm text-gray-500 mt-1">{selectedProject.title}</p>
            </div>
            <button
              onClick={() => {
                setIsViewingFiles(false);
                setSelectedProject(null);
              }}
              className="text-gray-400 hover:text-gray-500"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mt-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {selectedProject.files.map((file, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  onClick={() => {
                    // In a real app, this would open the file
                    toast.info(`Opening ${file.name}`);
                  }}
                >
                  <div className="flex flex-col items-center text-center">
                    {getFileIcon(file.type)}
                    <p className="mt-2 text-sm font-medium text-gray-900 truncate w-full">{file.name}</p>
                    <p className="text-xs text-gray-500">{file.size}</p>
                    <p className="text-xs text-gray-400 mt-1">Uploaded {file.uploaded}</p>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toast.info(`Downloading ${file.name}`);
                      }}
                      className="mt-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
                    >
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {selectedProject.updates.some(update => update.attachments.length > 0) && (
              <>
                <h3 className="text-lg font-medium text-gray-900 mt-8 mb-4">Update Attachments</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {selectedProject.updates.map((update, updateIndex) =>
                    update.attachments.map((file, fileIndex) => (
                      <div
                        key={`${updateIndex}-${fileIndex}`}
                        className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                        onClick={() => {
                          // In a real app, this would open the file
                          toast.info(`Opening ${file.name}`);
                        }}
                      >
                        <div className="flex flex-col items-center text-center">
                          {getFileIcon(file.type)}
                          <p className="mt-2 text-sm font-medium text-gray-900 truncate w-full">{file.name}</p>
                          <p className="text-xs text-gray-500">{file.size}</p>
                          <p className="text-xs text-gray-400 mt-1">Added {update.date}</p>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              toast.info(`Downloading ${file.name}`);
                            }}
                            className="mt-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-md text-sm hover:bg-gray-200 transition-colors"
                          >
                            Download
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const getFileIcon = (fileType) => {
  switch (fileType) {
    case 'pdf':
      return (
        <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
        </svg>
      );
    case 'image':
      return (
        <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      );
    default:
      return (
        <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
      );
  }
};

export default ProjectFilesModal;