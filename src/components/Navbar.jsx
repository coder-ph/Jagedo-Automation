import { useState } from 'react';
import { Link } from 'react-router-dom'; // or your preferred routing solution
import logo from './path-to-your-logo/logo.png'; // update this path to your actual logo file

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between">
          {/* Logo and brand name */}
          <div className="flex space-x-4">
            <div>
              <Link to="/" className="flex items-center py-5 px-2 text-gray-700 hover:text-gray-900">
                <img 
                  src={logo} 
                  alt="Company Logo" 
                  className="h-8 w-auto mr-2" // Adjust height as needed
                />
                <span className="font-bold text-xl text-indigo-600">Jagedo</span>
              </Link>
            </div>
          </div>

          {/* Primary nav */}
          <div className="hidden md:flex items-center space-x-1">
            <Link to="/" className="py-5 px-3 text-gray-700 hover:text-gray-900">Home</Link>
            <Link to="/about" className="py-5 px-3 text-gray-700 hover:text-gray-900">About</Link>
            <Link to="/services" className="py-5 px-3 text-gray-700 hover:text-gray-900">Services</Link>
            <Link to="/contact" className="py-5 px-3 text-gray-700 hover:text-gray-900">Contact</Link>
          </div>

          {/* Secondary nav */}
          <div className="hidden md:flex items-center space-x-1">
            <Link to="/login" className="py-2 px-3 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition duration-300">Login</Link>
            <Link to="/register" className="py-2 px-3 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition duration-300">Register</Link>
          </div>

          {/* Mobile button */}
          <div className="md:hidden flex items-center">
            <button 
              onClick={() => setIsOpen(!isOpen)}
              className="mobile-menu-button p-2 focus:outline-none"
            >
              <svg 
                className="w-6 h-6 text-gray-700" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className={`md:hidden ${isOpen ? 'block' : 'hidden'}`}>
        <Link to="/" className="block py-2 px-4 text-sm hover:bg-gray-200">Home</Link>
        <Link to="/about" className="block py-2 px-4 text-sm hover:bg-gray-200">About</Link>
        <Link to="/services" className="block py-2 px-4 text-sm hover:bg-gray-200">Services</Link>
        <Link to="/contact" className="block py-2 px-4 text-sm hover:bg-gray-200">Contact</Link>
        <div className="border-t border-gray-200 pt-2 pb-3">
          <Link to="/login" className="block py-2 px-4 text-sm bg-indigo-600 text-white rounded mx-2 mb-2 text-center">Login</Link>
          <Link to="/register" className="block py-2 px-4 text-sm bg-gray-200 text-gray-800 rounded mx-2 text-center">Register</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;