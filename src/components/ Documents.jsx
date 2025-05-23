import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaFilePdf, FaFileWord, FaFileExcel, FaFileImage, FaDownload, FaSearch, FaFilter } from 'react-icons/fa';

const Documents = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const requestId = queryParams.get('request') || 'All Requests';

  // Mock data - replace with API calls
  const documents = [
    { id: 'DOC-001', name: 'Survey Report.pdf', type: 'pdf', size: '2.4 MB', date: '2023-06-15', request: 'JPG-1001' },
    { id: 'DOC-002', name: 'Soil Analysis.docx', type: 'word', size: '1.2 MB', date: '2023-06-10', request: 'JPG-1002' },
    { id: 'DOC-003', name: 'Topographic Map.jpg', type: 'image', size: '4.7 MB', date: '2023-05-28', request: 'JPG-1003' },
    { id: 'DOC-004', name: 'Boundary Coordinates.xlsx', type: 'excel', size: '0.8 MB', date: '2023-05-15', request: 'JPG-1004' },
    { id: 'DOC-005', name: 'Geotechnical Findings.pdf', type: 'pdf', size: '3.1 MB', date: '2023-04-30', request: 'JPG-1005' },
  ];

  const getFileIcon = (type) => {
    switch (type) {
      case 'pdf': return <FaFilePdf className="text-red-500 text-xl" />;
      case 'word': return <FaFileWord className="text-blue-500 text-xl" />;
      case 'excel': return <FaFileExcel className="text-green-500 text-xl" />;
      case 'image': return <FaFileImage className="text-yellow-500 text-xl" />;
      default: return <FaFilePdf className="text-gray-500 text-xl" />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
          <p className="mt-1 text-sm text-gray-600">
            {requestId !== 'All Requests' ? `Documents for request ${requestId}` : 'All your documents'}
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex space-x-3">
          <div className="relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaSearch className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 pr-12 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="Search documents..."
            />
          </div>
          <button className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <FaFilter className="mr-2" />
            Filter
          </button>
        </div>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <ul className="divide-y divide-gray-200">
          {documents
            .filter(doc => requestId === 'All Requests' || doc.request === requestId)
            .map((document) => (
              <li key={document.id} className="hover:bg-gray-50 transition-colors duration-150">
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 mr-4">
                        {getFileIcon(document.type)}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-indigo-600 truncate">
                          {document.name}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          Request: {document.request} • {document.size} • {document.date}
                        </p>
                      </div>
                    </div>
                    <div className="ml-4 flex-shrink-0 flex">
                      <button className="ml-2 inline-flex items-center px-3 py-1 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        <FaDownload className="mr-1" />
                        Download
                      </button>
                    </div>
                  </div>
                </div>
              </li>
            ))}
        </ul>
        {documents.filter(doc => requestId === 'All Requests' || doc.request === requestId).length === 0 && (
          <div className="px-4 py-12 text-center">
            <p className="text-gray-500">No documents found</p>
          </div>
        )}
        <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
          <div className="flex-1 flex justify-between sm:hidden">
            <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Next
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing <span className="font-medium">1</span> to <span className="font-medium">5</span> of{' '}
                <span className="font-medium">12</span> results
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span className="sr-only">Previous</span>
                  &larr;
                </button>
                <button aria-current="page" className="z-10 bg-indigo-50 border-indigo-500 text-indigo-600 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  1
                </button>
                <button className="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  2
                </button>
                <button className="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  3
                </button>
                <button className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span className="sr-only">Next</span>
                  &rarr;
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Documents;