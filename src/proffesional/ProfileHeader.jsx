// ProfileHeader.jsx
import React from 'react';
import { FaStar, FaMapMarkerAlt } from 'react-icons/fa';

const ProfileHeader = ({ name, title, location, rating, reviewCount }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex flex-col md:flex-row md:items-center">
        <div className="flex-shrink-0">
          <img
            className="h-24 w-24 rounded-full object-cover"
            src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
            alt="Profile"
          />
        </div>
        <div className="mt-4 md:mt-0 md:ml-6">
          <h1 className="text-2xl font-bold text-gray-900">{name}</h1>
          <p className="text-lg text-gray-600">{title}</p>
          <div className="mt-2 flex items-center">
            <FaMapMarkerAlt className="h-4 w-4 text-gray-400" />
            <span className="ml-1 text-gray-600">{location}</span>
          </div>
          <div className="mt-2 flex items-center">
            <div className="flex items-center">
              {[1, 2, 3, 4, 5].map((star) => (
                <FaStar
                  key={star}
                  className={`h-5 w-5 ${star <= Math.floor(rating) ? 'text-yellow-400' : 'text-gray-300'}`}
                />
              ))}
            </div>
            <span className="ml-2 text-gray-600">
              {rating} ({reviewCount} reviews)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileHeader;