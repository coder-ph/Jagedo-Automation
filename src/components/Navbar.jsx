// src/components/Navbar.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, getUser, clearAuthData } from '../logins/auth';
import { FaUser, FaSignOutAlt, FaBars, FaTimes } from 'react-icons/fa';

const Navbar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isAuth = isAuthenticated();
  const user = getUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuthData();
    navigate('/login');
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo Section */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link to="/" className="flex items-center">
                <img 
                  src="/images/Japageologo.webp" 
                  alt="Japageo Logo"
                  className="h-10 w-auto hover:opacity-80 transition-opacity"
                />
              </Link>
            </div>

            {/* Desktop Navigation Links */}
            {isAuth && (
              <div className="hidden md:ml-8 md:flex md:space-x-6">
                <Link
                  to="/customer-request"
                  className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-700 hover:text-indigo-600 hover:border-indigo-500 transition-all duration-200"
                  activeClassName="border-indigo-500 text-indigo-600"
                >
                  New Request
                </Link>
                <Link
                  to="/customer-dashboard"
                  className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-700 hover:text-indigo-600 hover:border-indigo-500 transition-all duration-200"
                  activeClassName="border-indigo-500 text-indigo-600"
                >
                  Dashboard
                </Link>
              </div>
            )}
          </div>

          {/* Desktop Auth Section */}
          <div className="hidden md:ml-6 md:flex md:items-center">
            {isAuth ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-indigo-100 p-1 rounded-full text-indigo-600">
                    <FaUser className="h-5 w-5" />
                  </div>
                  <span className="ml-2 text-sm font-medium text-gray-700">
                    {user?.name || 'User'}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
                >
                  <FaSignOutAlt className="h-4 w-4 mr-2" />
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-3">
                <Link
                  to="/login"
                  className="flex items-center px-4 py-2 border border-indigo-600 rounded-md shadow-sm text-sm font-medium text-indigo-600 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMobileMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-indigo-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 transition-colors duration-200"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {mobileMenuOpen ? (
                <FaTimes className="h-6 w-6" />
              ) : (
                <FaBars className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="pt-2 pb-3 space-y-1">
            {isAuth && (
              <>
                <Link
                  to="/customer-request"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 hover:border-indigo-500 transition-all duration-200"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  New Request
                </Link>
                <Link
                  to="/customer-dashboard"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 hover:border-indigo-500 transition-all duration-200"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
              </>
            )}
          </div>
          <div className="pt-4 pb-3 border-t border-gray-200">
            {isAuth ? (
              <div className="flex items-center px-4">
                <div className="flex-shrink-0">
                  <div className="bg-indigo-100 p-2 rounded-full text-indigo-600">
                    <FaUser className="h-5 w-5" />
                  </div>
                </div>
                <div className="ml-3">
                  <div className="text-sm font-medium text-gray-700">
                    {user?.name || 'User'}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-2 px-2">
                <Link
                  to="/login"
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 transition-colors duration-200"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </div>
            )}
            {isAuth && (
              <div className="mt-3 px-2">
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-white bg-red-600 hover:bg-red-700 transition-colors duration-200"
                >
                  <div className="flex items-center">
                    <FaSignOutAlt className="h-4 w-4 mr-2" />
                    Logout
                  </div>
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;