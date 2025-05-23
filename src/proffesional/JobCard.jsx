// JobCard.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { FaMoneyBillWave, FaClock, FaMapMarkerAlt } from 'react-icons/fa';

const JobCard = ({ job }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">{job.title}</h3>
            <p className="mt-1 text-sm text-gray-500">{job.serviceType}</p>
          </div>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            {job.status}
          </span>
        </div>
        
        <p className="mt-3 text-sm text-gray-600">{job.description}</p>
        
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center">
            <FaMoneyBillWave className="flex-shrink-0 h-5 w-5 text-gray-400" />
            <span className="ml-2 text-sm text-gray-600">{job.budget}</span>
          </div>
          <div className="flex items-center">
            <FaClock className="flex-shrink-0 h-5 w-5 text-gray-400" />
            <span className="ml-2 text-sm text-gray-600">Deadline: {job.deadline}</span>
          </div>
          <div className="flex items-center">
            <FaMapMarkerAlt className="flex-shrink-0 h-5 w-5 text-gray-400" />
            <span className="ml-2 text-sm text-gray-600">{job.location}</span>
          </div>
        </div>
        
        <div className="mt-6 flex justify-end">
          <Link
            to={`/professional-dashboard/jobs/${job.id}`}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
};

export default JobCard;