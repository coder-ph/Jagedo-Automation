// ProfessionalSidebar.jsx
import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  FaHome, 
  FaBriefcase, 
  FaFileAlt, 
  FaChartLine, 
  FaUser, 
  FaCog,
  FaSignOutAlt
} from 'react-icons/fa';

const ProfessionalSidebar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/professional-dashboard', icon: <FaHome />, label: 'Overview' },
    { path: '/professional-dashboard/jobs', icon: <FaBriefcase />, label: 'Job Listings' },
    { path: '/professional-dashboard/bids', icon: <FaFileAlt />, label: 'My Bids' },
    { path: '/professional-dashboard/analytics', icon: <FaChartLine />, label: 'Analytics' },
    { path: '/professional-dashboard/profile', icon: <FaUser />, label: 'Profile' },
    { path: '/professional-dashboard/settings', icon: <FaCog />, label: 'Settings' },
  ];

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64 bg-indigo-700 text-white">
        <div className="flex items-center justify-center h-16 px-4 bg-indigo-800">
          <h1 className="text-xl font-bold">ProConnect</h1>
        </div>
        
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto">
          <nav className="flex-1 px-2 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={`flex items-center px-4 py-3 text-sm font-medium rounded-md transition-colors ${
                  location.pathname === item.path
                    ? 'bg-indigo-800 text-white'
                    : 'text-indigo-100 hover:bg-indigo-600 hover:bg-opacity-75'
                }`}
              >
                <span className="mr-3 text-lg">{item.icon}</span>
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
        
        <div className="px-4 py-4 border-t border-indigo-800">
          <button className="flex items-center w-full px-4 py-3 text-sm font-medium text-indigo-100 hover:bg-indigo-600 hover:bg-opacity-75 rounded-md transition-colors">
            <span className="mr-3 text-lg"><FaSignOutAlt /></span>
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalSidebar;