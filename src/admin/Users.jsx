// src/pages/Users.jsx
import { useState, useEffect } from 'react';
import { fetchUsers, updateUser, deleteUser } from '../services/api';
import UserTable from '../components/UserTable';
import UserModal from '../components/UserModal';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await fetchUsers();
        setUsers(data);
      } catch (error) {
        console.error('Failed to load users:', error);
      } finally {
        setLoading(false);
      }
    };
    loadUsers();
  }, []);

  const handleEdit = (user) => {
    setCurrentUser(user);
    setIsModalOpen(true);
  };

  const handleDelete = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await deleteUser(userId);
        setUsers(users.filter(user => user.id !== userId));
      } catch (error) {
        console.error('Failed to delete user:', error);
      }
    }
  };

  const handleSave = async (userData) => {
    try {
      const updatedUser = await updateUser(userData);
      if (currentUser) {
        setUsers(users.map(u => u.id === updatedUser.id ? updatedUser : u));
      }
      setIsModalOpen(false);
    } catch (error) {
      console.error('Failed to save user:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">User Management</h1>
        <button
          onClick={() => {
            setCurrentUser(null);
            setIsModalOpen(true);
          }}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          Add New User
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">Loading users...</div>
      ) : (
        <UserTable users={users} onEdit={handleEdit} onDelete={handleDelete} />
      )}

      <UserModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        user={currentUser}
        onSave={handleSave}
      />
    </div>
  );
}