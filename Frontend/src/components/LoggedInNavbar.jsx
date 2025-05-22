import { Link } from 'react-router-dom';
import { useAuth } from '../logins/AuthContext';

const LoggedInNavbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between">
          <div className="flex space-x-7">
            <Link to="/logged-in-navbar" className="flex items-center py-4 px-2">
              <span className="font-semibold text-gray-500 text-lg">Dashboard</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            {user && (
              <span className="py-4 px-2 text-gray-500 font-semibold">
                Welcome, {user.name}
              </span>
            )}
            <Link to="/logged-in-navbar/projects" className="py-4 px-2 text-gray-500 font-semibold hover:text-indigo-600 transition">
              Projects
            </Link>
            <button
              onClick={logout}
              className="py-2 px-4 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default LoggedInNavbar;
