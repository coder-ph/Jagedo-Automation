// src/components/AdminLayout.jsx
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return null;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-indigo-700 text-white p-4">
        <div className="flex items-center space-x-2 mb-8">
          <h1 className="text-xl font-bold">BidPlatform Admin</h1>
        </div>
        
        <nav>
          <ul className="space-y-2">
            <li>
              <Link to="/" className="flex items-center p-2 rounded hover:bg-indigo-600">
                <span className="ml-2">Dashboard</span>
              </Link>
            </li>
            <li>
              <Link to="/users" className="flex items-center p-2 rounded hover:bg-indigo-600">
                <span className="ml-2">Users</span>
              </Link>
            </li>
            <li>
              <Link to="/projects" className="flex items-center p-2 rounded hover:bg-indigo-600">
                <span className="ml-2">Projects</span>
              </Link>
            </li>
            <li>
              <Link to="/bids" className="flex items-center p-2 rounded hover:bg-indigo-600">
                <span className="ml-2">Bids</span>
              </Link>
            </li>
            <li>
              <Link to="/settings" className="flex items-center p-2 rounded hover:bg-indigo-600">
                <span className="ml-2">Settings</span>
              </Link>
            </li>
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Header */}
        <header className="bg-white shadow-sm p-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-800">Admin Dashboard</h2>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">{user.email}</span>
            <button 
              onClick={handleLogout}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Content */}
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}