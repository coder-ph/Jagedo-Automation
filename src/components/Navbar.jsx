import { useState } from 'react';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="font-bold text-xl">Jagedo</div>
        <div className="hidden md:flex space-x-6">
          <a href="#" className="hover:text-blue-200">Home</a>
          <a href="#" className="hover:text-blue-200">About</a>
          <a href="#" className="hover:text-blue-200">Services</a>
          <a href="#" className="hover:text-blue-200">Contact</a>
        </div>
        <div className="hidden md:flex space-x-4">
          <button className="bg-white text-blue-600 px-4 py-2 rounded hover:bg-blue-100">
            Login
          </button>
          <button className="border border-white px-4 py-2 rounded hover:bg-blue-500">
            Register
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;