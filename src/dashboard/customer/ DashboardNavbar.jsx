import React from 'react';
import { Link } from 'react-router-dom';

const DashboardNavbar = ({ onLogout, userRole, userName }) => {
  const getDashboardTitle = () => {
    switch(userRole) {
      case 'customer': return 'Customer Dashboard';
      case 'professional': return 'Professional Dashboard';
      case 'fundi': return 'Fundi Dashboard';
      case 'hardware': return 'Hardware Dashboard';
      case 'contractor': return 'Contractor Dashboard';
      default: return 'Dashboard';
    }
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link to={`/${userRole}-dashboard`} className="flex items-center">
            <img 
              src="/logo.png" 
              alt="Company Logo" 
              className="h-8 w-auto mr-2"
            />
            <span className="text-xl font-bold text-gray-900">{getDashboardTitle()}</span>
          </Link>
        </div>
        
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600 hidden sm:inline">
            Welcome, {userName || 'User'}
          </span>
          
          {userRole === 'customer' && (
            <Link 
              to="/customer-request"
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors text-sm"
            >
              + New Request
            </Link>
          )}
          
          <button
            onClick={onLogout}
            className="px-4 py-2 text-gray-700 hover:text-gray-900 transition-colors text-sm"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default DashboardNavbar;

