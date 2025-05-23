import React from 'react';
import { FaStar, FaMapMarkerAlt, FaAward, FaBriefcase } from 'react-icons/fa';

const ProfileHeader = ({ 
  name, 
  title, 
  location, 
  rating = 0, 
  reviewCount = 0,
  yearsExperience,
  specialties = []
}) => {
  // Calculate full and partial stars for more precise ratings
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

  return (
    <div className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">
      <div className="relative">
        {/* Profile background banner */}
        <div className="h-32 bg-gradient-to-r from-green-600 to-green-800"></div>
        
        {/* Profile content */}
        <div className="px-6 pb-6">
          <div className="flex flex-col md:flex-row md:items-end -mt-16 relative z-10">
            {/* Profile picture with border */}
            <div className="flex-shrink-0">
              <div className="h-32 w-32 rounded-full border-4 border-white bg-white shadow-md overflow-hidden">
                <img
                  className="h-full w-full object-cover"
                  src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                  alt={`${name}'s profile`}
                />
              </div>
            </div>

            {/* Profile details */}
            <div className="mt-4 md:mt-0 md:ml-6 flex-1">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h1 className="text-2xl md:text-3xl font-bold text-gray-900">{name}</h1>
                  <p className="text-lg text-gray-700 font-medium">{title}</p>
                </div>
                
                {/* Verified badge for Kenyan professionals */}
                <div className="mt-2 md:mt-0 flex items-center bg-green-50 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                  <FaAward className="mr-1" />
                  <span>Verified Professional</span>
                </div>
              </div>

              {/* Location and experience */}
              <div className="mt-3 flex flex-wrap items-center gap-y-2 gap-x-4">
                <div className="flex items-center text-gray-600">
                  <FaMapMarkerAlt className="flex-shrink-0 h-4 w-4 text-green-600" />
                  <span className="ml-1">{location || 'Nairobi, Kenya'}</span>
                </div>
                
                {yearsExperience && (
                  <div className="flex items-center text-gray-600">
                    <FaBriefcase className="flex-shrink-0 h-4 w-4 text-green-600" />
                    <span className="ml-1">{yearsExperience}+ years experience</span>
                  </div>
                )}
              </div>

              {/* Rating with improved star display */}
              <div className="mt-3 flex flex-wrap items-center gap-y-2 gap-x-4">
                <div className="flex items-center">
                  <div className="flex items-center">
                    {[...Array(fullStars)].map((_, i) => (
                      <FaStar key={`full-${i}`} className="h-5 w-5 text-yellow-400" />
                    ))}
                    {hasHalfStar && (
                      <div className="relative h-5 w-5">
                        <FaStar className="absolute h-5 w-5 text-gray-300" />
                        <FaStar className="absolute h-5 w-5 text-yellow-400" style={{ clipPath: 'inset(0 50% 0 0)' }} />
                      </div>
                    )}
                    {[...Array(emptyStars)].map((_, i) => (
                      <FaStar key={`empty-${i}`} className="h-5 w-5 text-gray-300" />
                    ))}
                  </div>
                  <span className="ml-2 text-gray-700 font-medium">
                    {rating.toFixed(1)} <span className="text-gray-500 font-normal">({reviewCount} reviews)</span>
                  </span>
                </div>
              </div>

              {/* Specialties chips */}
              {specialties.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {specialties.map((specialty, index) => (
                    <span 
                      key={index}
                      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileHeader;