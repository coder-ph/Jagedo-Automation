// BidList.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { FaMoneyBillWave, FaClock, FaUser, FaCalendarAlt } from 'react-icons/fa';

const BidList = ({ bids }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'accepted': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'pending': return 'Pending Review';
      case 'accepted': return 'Accepted';
      case 'rejected': return 'Not Selected';
      default: return status;
    }
  };

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      {bids.length === 0 ? (
        <div className="p-6 text-center">
          <p className="text-gray-500">No bids found for this status</p>
        </div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {bids.map((bid) => (
            <li key={bid.id}>
              <Link 
                to={`/professional-dashboard/bids/${bid.id}`} 
                className="block hover:bg-gray-50"
              >
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-indigo-600 truncate">{bid.jobTitle}</h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(bid.status)}`}>
                      {getStatusLabel(bid.status)}
                    </span>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex">
                      <div className="flex items-center text-sm text-gray-500 mr-4">
                        <FaUser className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                        <p>{bid.client}</p>
                      </div>
                      <div className="flex items-center text-sm text-gray-500 mt-2 sm:mt-0">
                        <FaMoneyBillWave className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                        <p>{bid.proposedAmount}</p>
                      </div>
                    </div>
                    <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                      <FaCalendarAlt className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                      <p>
                        Submitted on <time dateTime={bid.submittedDate}>{bid.submittedDate}</time>
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 flex items-center text-sm text-gray-500">
                    <FaClock className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                    <p>Proposed timeline: {bid.proposedTimeline}</p>
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BidList;