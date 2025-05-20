import React, { useState, useEffect } from 'react';

const CreativeNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed w-full z-50 transition-all duration-500 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-lg py-2' : 'bg-transparent py-4'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          {/* Animated Logo with Text */}
          <div className="flex items-center space-x-2">
            <a href="#" className="flex items-center group">
              <div className="relative">
                <img
                  src="/images/Japageologo.webp"
                  alt="Jafredo Logo"
                  className={`h-14 w-auto transition-all duration-500 ${scrolled ? 'h-12' : 'h-14'} group-hover:rotate-[15deg]`}
                />
                <div className={`absolute -inset-2 rounded-full bg-indigo-100/30 mix-blend-multiply group-hover:opacity-100 opacity-0 transition-opacity duration-300 ${scrolled ? 'scale-90' : 'scale-100'}`}></div>
              </div>
            
            </a>
          </div>

          {/* Desktop Navigation with Animated Underline */}
          <div className="hidden md:flex items-center space-x-8">
            <div className="flex space-x-1">
              <a href="#" className="relative px-3 py-2 text-sm font-medium text-gray-700 hover:text-indigo-600 group">
                Login
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-indigo-600 transition-all duration-300 group-hover:w-full"></span>
              </a>
            </div>
            
            <div className="relative group">
              <a 
                href="#"
                className="relative z-10 px-6 py-2.5 text-sm font-semibold text-white rounded-full overflow-hidden"
              >
                <span className="relative z-10">Sign Up</span>
                <span className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full transition-all duration-500 group-hover:from-indigo-600 group-hover:to-purple-700"></span>
                <span className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-700 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
              </a>
              <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-indigo-400 to-purple-500 blur opacity-75 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
          </div>

          {/* Animated Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="relative p-2 rounded-full focus:outline-none group"
              aria-expanded={isMenuOpen}
            >
              <div className="relative flex flex-col items-center justify-center w-8 h-8">
                <span className={`absolute block w-6 h-0.5 bg-gray-700 transition-all duration-300 ${isMenuOpen ? 'rotate-45 translate-y-0' : '-translate-y-2'}`}></span>
                <span className={`absolute block w-6 h-0.5 bg-gray-700 transition-all duration-300 ${isMenuOpen ? 'opacity-0' : 'opacity-100'}`}></span>
                <span className={`absolute block w-6 h-0.5 bg-gray-700 transition-all duration-300 ${isMenuOpen ? '-rotate-45 translate-y-0' : 'translate-y-2'}`}></span>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Glass Morphism Mobile Menu */}
      <div className={`md:hidden transition-all duration-500 ease-in-out overflow-hidden ${isMenuOpen ? 'max-h-48 opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="bg-white/90 backdrop-blur-md border-t border-gray-100 shadow-xl">
          <div className="px-2 pt-2 pb-4 space-y-2">
            <a
              href="#"
              className="block px-4 py-3 mx-2 rounded-lg text-base font-medium text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors duration-300"
            >
              Login
            </a>
            <a
              href="#"
              className="block px-4 py-3 mx-2 rounded-lg text-base font-medium text-white bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 transition-all duration-300 shadow-md"
            >
              Sign Up
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default CreativeNavbar;