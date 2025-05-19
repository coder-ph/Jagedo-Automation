import { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const mobileMenuRef = useRef(null);
  const location = useLocation();

  useEffect(() => {
    setIsOpen(false);
  }, [location]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (mobileMenuRef.current && !mobileMenuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogoClick = (e) => {
    if (location.pathname === '/') {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <nav className={`fixed w-full z-50 transition-all duration-500 ${isScrolled ? 'bg-white/95 backdrop-blur-md shadow-md py-0' : 'bg-white/80 backdrop-blur-sm py-2'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo with enhanced styling */}
          <div className="flex-shrink-0 flex items-center">
            <Link 
              to="/" 
              onClick={handleLogoClick}
              className="flex items-center group"
              aria-label="Home"
            >
              <img 
                src="/images/Japageologo.webp" 
                alt="Japageo Logo" 
                className={`w-auto transition-all duration-500 ${isScrolled ? 'h-14' : 'h-16'} group-hover:opacity-90`} 
              />
            
            </Link>
          </div>

          {/* Desktop Navigation - Premium styling */}
          <div className="hidden md:flex items-center space-x-10">
            <div className="flex space-x-8">
              <NavLink to="/">Home</NavLink>
              <NavLink to="/about">About</NavLink>
              <NavLink to="/services">Services</NavLink>
              <NavLink to="/contact">Contact</NavLink>
            </div>
            <div className="ml-8 flex items-center space-x-4">
              <Link 
                to="/login" 
                className="relative px-5 py-2.5 rounded-lg text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 overflow-hidden group"
              >
                <span className="relative z-10">Login</span>
                <span className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
              </Link>
              <Link 
                to="/register" 
                className="px-5 py-2.5 rounded-lg text-sm font-medium text-indigo-600 bg-white hover:bg-gray-50 transition-all duration-300 border-2 border-indigo-600 shadow-sm hover:shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Register
              </Link>
            </div>
          </div>

          {/* Mobile menu button - Enhanced design */}
          <div className="md:hidden flex items-center">
            <button 
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-3 rounded-full text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 focus:outline-none transition-all duration-300"
              aria-expanded={isOpen}
              aria-label={isOpen ? "Close menu" : "Open menu"}
            >
              <span className="sr-only">{isOpen ? "Close menu" : "Open menu"}</span>
              <div className={`w-6 flex flex-col items-center transition-all duration-300 ${isOpen ? 'gap-0' : 'gap-1.5'}`}>
                <span className={`h-0.5 w-6 bg-current rounded-full transition-all duration-300 ${isOpen ? 'rotate-45 translate-y-0.5' : ''}`}></span>
                <span className={`h-0.5 w-6 bg-current rounded-full transition-all duration-300 ${isOpen ? 'opacity-0' : 'opacity-100'}`}></span>
                <span className={`h-0.5 w-6 bg-current rounded-full transition-all duration-300 ${isOpen ? '-rotate-45 -translate-y-0.5' : ''}`}></span>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu - Premium styling */}
      <div 
        ref={mobileMenuRef}
        className={`md:hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${isOpen ? 'opacity-100 max-h-screen' : 'opacity-0 max-h-0 overflow-hidden'}`}
      >
        <div className="pt-4 pb-6 space-y-2 bg-white/95 backdrop-blur-lg shadow-xl">
          <MobileNavLink to="/">Home</MobileNavLink>
          <MobileNavLink to="/about">About</MobileNavLink>
          <MobileNavLink to="/services">Services</MobileNavLink>
          <MobileNavLink to="/contact">Contact</MobileNavLink>
          <div className="mt-6 pt-6 border-t border-gray-100 px-4">
            <Link 
              to="/login" 
              className="block w-full text-center px-4 py-3 text-base font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-lg shadow-md transition-all duration-300 mb-3"
            >
              Login
            </Link>
            <Link 
              to="/register" 
              className="block w-full text-center px-4 py-3 text-base font-medium text-indigo-600 bg-white hover:bg-gray-50 rounded-lg border-2 border-indigo-600 shadow-sm transition-all duration-300"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

// Enhanced NavLink component for desktop
const NavLink = ({ to, children }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link
      to={to}
      className={`relative px-1 py-2 text-sm font-medium transition-all duration-300 group ${
        isActive ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-500'
      }`}
    >
      {children}
      <span className={`absolute bottom-0 left-0 h-0.5 bg-indigo-600 transition-all duration-500 ${isActive ? 'w-full' : 'w-0 group-hover:w-full'}`}></span>
    </Link>
  );
};

// Enhanced MobileNavLink component
const MobileNavLink = ({ to, children }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link
      to={to}
      className={`block px-6 py-3 text-lg font-medium transition-all duration-300 mx-2 rounded-lg ${
        isActive
          ? 'bg-indigo-50 text-indigo-600'
          : 'text-gray-700 hover:bg-gray-100 hover:text-indigo-600'
      }`}
    >
      {children}
    </Link>
  );
};

export default Navbar;