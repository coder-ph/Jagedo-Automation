// ProjectDetailsLeft.jsx
import React from 'react';

const ProjectDetailsLeft = ({ selectedProject, newMessage, setNewMessage, sendMessage }) => {
  return (
    <div className="md:col-span-2">
      <div className="bg-gray-50 p-4 rounded-lg">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Project Description</h3>
        <p className="text-gray-700">{selectedProject.description}</p>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Project Updates</h3>
        <div className="space-y-4">
          {selectedProject.updates.map((update, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg ${update.sender === 'customer' ? 'bg-indigo-50' : update.sender === 'system' ? 'bg-gray-100' : 'bg-white border border-gray-200'}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-sm font-medium">
                    {update.sender === 'customer' ? 'You' : update.sender === 'system' ? 'System' : selectedProject.provider}
                  </span>
                  <span className="text-xs text-gray-500 ml-2">{update.date}</span>
                </div>
                {update.sender === 'provider' && (
                  <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">Provider</span>
                )}
              </div>
              <p className="mt-1 text-gray-700">{update.message}</p>
              {update.attachments.length > 0 && (
                <div className="mt-2">
                  <h4 className="text-xs font-medium text-gray-500 mb-1">Attachments:</h4>
                  <div className="flex flex-wrap gap-2">
                    {update.attachments.map((file, fileIndex) => (
                      <div
                        key={fileIndex}
                        className="flex items-center space-x-2 p-2 bg-white rounded border border-gray-200 text-xs"
                      >
                        {getFileIcon(file.type)}
                        <div>
                          <p className="font-medium truncate max-w-xs">{file.name}</p>
                          <p className="text-gray-500">{file.size}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-6">
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
            Send Message to Provider
          </label>
          <div className="flex space-x-2">
            <input
              type="text"
              id="message"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            />
            <button
              onClick={sendMessage}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
            >
              Send
            </button>
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

export default ProjectDetailsLeft;