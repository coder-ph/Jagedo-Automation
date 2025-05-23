// ProfileDetails.jsx
import React from 'react';

const ProfileDetails = ({ bio, services, experience, certifications }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="space-y-6">
        <div>
          <h2 className="text-lg font-medium text-gray-900 mb-2">About Me</h2>
          <p className="text-gray-600">{bio}</p>
        </div>
        
        <div>
          <h2 className="text-lg font-medium text-gray-900 mb-2">Services Offered</h2>
          <div className="flex flex-wrap gap-2">
            {services.map((service, index) => (
              <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
                {service}
              </span>
            ))}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">Experience</h2>
            <p className="text-gray-600">{experience}</p>
          </div>
          
          <div>
            <h2 className="text-lg font-medium text-gray-900 mb-2">Certifications</h2>
            <ul className="list-disc list-inside text-gray-600">
              {certifications.map((cert, index) => (
                <li key={index}>{cert}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileDetails;