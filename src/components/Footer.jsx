import { Link } from 'react-router-dom';
import { FaFacebook, FaTwitter, FaLinkedin, FaInstagram, FaMapMarkerAlt, FaPhone, FaEnvelope } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-b from-gray-800 to-gray-900 text-white pt-12 pb-8">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Company Info */}
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center mb-4">
              <img 
                src="/images/Japageologo.webp" 
                alt="Jagedo Logo" 
                className="h-10 w-auto"
              />
              <span className="ml-2 text-xl font-bold">JAGEDO</span>
            </Link>
            <p className="text-gray-300 mb-4">
              Empowering your digital transformation with innovative solutions and cutting-edge technology.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-indigo-400 transition duration-300">
                <FaFacebook size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition duration-300">
                <FaTwitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-500 transition duration-300">
                <FaLinkedin size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-pink-500 transition duration-300">
                <FaInstagram size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-indigo-300">Explore</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-gray-300 hover:text-indigo-400 transition duration-300 flex items-center">
                  <span className="w-1 h-1 bg-indigo-400 rounded-full mr-2"></span>
                  Home
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-300 hover:text-indigo-400 transition duration-300 flex items-center">
                  <span className="w-1 h-1 bg-indigo-400 rounded-full mr-2"></span>
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-300 hover:text-indigo-400 transition duration-300 flex items-center">
                  <span className="w-1 h-1 bg-indigo-400 rounded-full mr-2"></span>
                  Services
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-300 hover:text-indigo-400 transition duration-300 flex items-center">
                  <span className="w-1 h-1 bg-indigo-400 rounded-full mr-2"></span>
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-indigo-300">Get in Touch</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start">
                <FaMapMarkerAlt className="mt-1 mr-2 text-indigo-400 flex-shrink-0" />
                123 Business Avenue, Suite 456<br />
                San Francisco, CA 94107
              </li>
              <li className="flex items-center">
                <FaPhone className="mr-2 text-indigo-400" />
                +1 (555) 123-4567
              </li>
              <li className="flex items-center">
                <FaEnvelope className="mr-2 text-indigo-400" />
                info@jagedo.com
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-lg font-semibold mb-4 text-indigo-300">Services</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="hover:text-indigo-400 transition duration-300">Web Development</li>
              <li className="hover:text-indigo-400 transition duration-300">Digital Marketing</li>
              <li className="hover:text-indigo-400 transition duration-300">Cloud Solutions</li>
              <li className="hover:text-indigo-400 transition duration-300">Data Analytics</li>
              <li className="hover:text-indigo-400 transition duration-300">UI/UX Design</li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-700 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm mb-2 md:mb-0">
            © {new Date().getFullYear()} Jagedo. All rights reserved.
          </p>
          <div className="flex space-x-4">
            <Link to="/privacy" className="text-gray-400 hover:text-indigo-400 text-sm transition duration-300">
              Privacy Policy
            </Link>
            <Link to="/terms" className="text-gray-400 hover:text-indigo-400 text-sm transition duration-300">
              Terms of Service
            </Link>
            <Link to="/cookies" className="text-gray-400 hover:text-indigo-400 text-sm transition duration-300">
              Cookie Policy
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;