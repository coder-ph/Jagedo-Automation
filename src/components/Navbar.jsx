import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between">
          {/* Logo/Brand */}
          <div className="flex items-center py-4">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">Jaggedo</span>
            </Link>
          </div>
          
          {/* Primary Nav */}
          <div className="hidden md:flex items-center space-x-1">
            <Link to="/dashboard" className="px-3 py-2 text-gray-700 hover:text-blue-600">
              Dashboard
            </Link>
            <Link to="/projects" className="px-3 py-2 text-gray-700 hover:text-blue-600">
              Projects
            </Link>
            <Link to="/team" className="px-3 py-2 text-gray-700 hover:text-blue-600">
              Team
            </Link>
          </div>
          
          {/* Secondary Nav */}
          <div className="hidden md:flex items-center space-x-3">
            <button className="px-3 py-2 text-gray-700 hover:text-blue-600">
              Notifications
            </button>
            <div className="relative">
              <button className="flex items-center text-gray-700 hover:text-blue-600">
                <span className="mr-1">User</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </div>
          
          {/* Mobile button */}
          <div className="md:hidden flex items-center">
            <button className="mobile-menu-button">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      <div className="mobile-menu hidden md:hidden">
        <Link to="/dashboard" className="block px-2 py-4 text-sm hover:bg-gray-200">
          Dashboard
        </Link>
        <Link to="/projects" className="block px-2 py-4 text-sm hover:bg-gray-200">
          Projects
        </Link>
        <Link to="/team" className="block px-2 py-4 text-sm hover:bg-gray-200">
          Team
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;