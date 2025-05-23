import React from 'react';
import { useParams } from 'react-router-dom';
import { FaFilePdf, FaFileWord, FaFileExcel, FaFileImage, FaDownload, FaMapMarkerAlt, FaCalendarAlt, FaUser, FaPhone, FaEnvelope } from 'react-icons/fa';

const RequestDetail = () => {
  const { id } = useParams();

  // Mock data - replace with API call using the id
  const request = {
    id: id || 'JPG-1001',
    type: 'Land Survey',
    status: 'In Progress',
    date: '2023-06-15',
    priority: 'High',
    location: '123 Main St, Downtown Area',
    client: {
      name: 'John Smith',
      email: 'john.smith@example.com',
      phone: '(555) 123-4567'
    },
    description: 'Detailed land survey required for new construction project. Need boundary lines, elevation data, and existing structures marked.',
    documents: [
      { id: 'DOC-101', name: 'Initial_Specs.pdf', type: 'pdf', size: '1.2 MB', date: '2023-06-10' },
      { id: 'DOC-102', name: 'Site_Photos.zip', type: 'image', size: '4.5 MB', date: '2023-06-12' },
      { id: 'DOC-103', name: 'Client_Requirements.docx', type: 'word', size: '0.8 MB', date: '2023-06-14' },
    ],
    updates: [
      { date: '2023-06-15 09:30', status: 'Submitted', message: 'Request submitted by client' },
      { date: '2023-06-16 14:15', status: 'Review', message: 'Request under review by survey team' },
      { date: '2023-06-17 11:00', status: 'Approved', message: 'Request approved, scheduled for June 20' },
    ]
  };

  const getFileIcon = (type) => {
    switch (type) {
      case 'pdf': return <FaFilePdf className="text-red-500" />;
      case 'word': return <FaFileWord className="text-blue-500" />;
      case 'excel': return <FaFileExcel className="text-green-500" />;
      case 'image': return <FaFileImage className="text-yellow-500" />;
      default: return <FaFilePdf className="text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Submitted': return 'bg-gray-100 text-gray-800';
      case 'Review': return 'bg-blue-100 text-blue-800';
      case 'Approved': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-yellow-100 text-yellow-800';
      case 'Completed': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Request #{request.id}</h1>
          <p className="mt-1 text-sm text-gray-600">{request.type} service</p>
        </div>
        <div className="mt-4 md:mt-0">
          <span className={`px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${getStatusColor(request.status)}`}>
            {request.status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Request Details */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Request Details</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <p className="text-sm font-medium text-gray-500">Request Type</p>
                  <p className="mt-1 text-sm text-gray-900">{request.type}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">Priority</p>
                  <p className="mt-1 text-sm text-gray-900">{request.priority}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">Date Submitted</p>
                  <p className="mt-1 text-sm text-gray-900">{request.date}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500">Location</p>
                  <div className="mt-1 flex items-center text-sm text-gray-900">
                    <FaMapMarkerAlt className="mr-1 text-gray-400" />
                    {request.location}
                  </div>
                </div>
              </div>
              <div className="mt-6">
                <p className="text-sm font-medium text-gray-500">Description</p>
                <p className="mt-1 text-sm text-gray-900 whitespace-pre-line">{request.description}</p>
              </div>
            </div>
          </div>

          {/* Documents */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Documents</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <ul className="divide-y divide-gray-200">
                {request.documents.map((document) => (
                  <li key={document.id} className="py-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 mr-4">
                          {getFileIcon(document.type)}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{document.name}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            {document.size} • Uploaded {document.date}
                          </p>
                        </div>
                      </div>
                      <button className="ml-4 inline-flex items-center px-3 py-1 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        <FaDownload className="mr-1" />
                        Download
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
              {request.documents.length === 0 && (
                <p className="text-sm text-gray-500">No documents attached to this request</p>
              )}
            </div>
          </div>

          {/* Updates */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Updates</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="flow-root">
                <ul className="-mb-8">
                  {request.updates.map((update, updateIdx) => (
                    <li key={updateIdx}>
                      <div className="relative pb-8">
                        {updateIdx !== request.updates.length - 1 ? (
                          <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                        ) : null}
                        <div className="relative flex space-x-3">
                          <div>
                            <span className={`h-8 w-8 rounded-full flex items-center justify-center ${getStatusColor(update.status)}`}>
                              <span className="text-xs font-medium">{update.status.charAt(0)}</span>
                            </span>
                          </div>
                          <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                            <div>
                              <p className="text-sm text-gray-800">
                                {update.message}
                              </p>
                            </div>
                            <div className="text-right text-sm whitespace-nowrap text-gray-500">
                              <time dateTime={update.date}>{update.date}</time>
                            </div>
                          </div>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Client Information */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Client Information</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-indigo-100 p-3 rounded-full text-indigo-600">
                  <FaUser className="h-5 w-5" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-900">{request.client.name}</p>
                </div>
              </div>
              <div className="mt-4 space-y-2">
                <div className="flex items-center text-sm text-gray-500">
                  <FaEnvelope className="mr-2 text-gray-400" />
                  {request.client.email}
                </div>
                <div className="flex items-center text-sm text-gray-500">
                  <FaPhone className="mr-2 text-gray-400" />
                  {request.client.phone}
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Actions</h3>
            </div>
            <div className="px-4 py-5 sm:p-6 space-y-4">
              <button className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Upload Document
              </button>
              <button className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Send Message
              </button>
              {request.status !== 'Completed' && (
                <button className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                  Cancel Request
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RequestDetail;