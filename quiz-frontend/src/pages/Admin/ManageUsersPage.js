// src/pages/Admin/ManageUsersPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import UserTable from '../../components/admin/UserTable';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Modal from '../../components/common/Modal';
import InputField from '../../components/common/InputField';
import './AdminPages.css';

// Dummy user data
let adminDummyUsers = [
  { id: 1, username: 'user', email: 'user@example.com', role: 'user' },
  { id: 2, username: 'admin', email: 'admin@example.com', role: 'admin' },
  { id: 3, username: 'newuser', email: 'newuser@example.com', role: 'user' },
];

/**
 * Admin page for managing users (view, edit role, delete).
 */
const ManageUsersPage = () => {
  const { user: currentUser, authLoading } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState(null); // User object being edited
  const [newRole, setNewRole] = useState('');
  const [editError, setEditError] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      if (authLoading) {
        setLoading(false);
        return;
      }
      if (!currentUser || currentUser.role !== 'admin') {
        setError('Access Denied: You must be an administrator to view this page.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay
        setUsers(adminDummyUsers);
      } catch (err) {
        setError('Failed to load users. Please try again.');
        console.error('Error fetching users:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, [currentUser, authLoading]);

  const handleEditUser = (userId) => {
    const userToEdit = users.find(u => u.id === userId);
    if (userToEdit) {
      setEditingUser(userToEdit);
      setNewRole(userToEdit.role);
      setEditError('');
      setIsEditModalOpen(true);
    }
  };

  const handleSaveRole = async () => {
    if (!editingUser || !newRole) {
      setEditError('Role cannot be empty.');
      return;
    }
    if (editingUser.role === newRole) {
        setEditError('No change detected.');
        return;
    }
    if (editingUser.id === currentUser.id && newRole !== 'admin') {
        setEditError('You cannot demote yourself from admin role.');
        return;
    }

    setLoading(true); // Can use a more granular loading for the modal itself
    setEditError('');
    try {
      await new Promise(resolve => setTimeout(resolve, 600));
      adminDummyUsers = adminDummyUsers.map(u =>
        u.id === editingUser.id ? { ...u, role: newRole } : u
      );
      setUsers(adminDummyUsers);
      setIsEditModalOpen(false);
      setEditingUser(null);
      alert(`User ${editingUser.username}'s role updated to ${newRole}.`);
    } catch (err) {
      setEditError('Failed to update role. Please try again.');
      console.error('Update role error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (userId === currentUser.id) {
        alert('You cannot delete your own account!');
        return;
    }
    if (window.confirm('Are you sure you want to delete this user?')) {
      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 500));
        adminDummyUsers = adminDummyUsers.filter(u => u.id !== userId);
        setUsers(adminDummyUsers);
        alert('User deleted successfully!');
      } catch (err) {
        setError('Failed to delete user.');
        console.error('Delete user error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  if (authLoading || loading) {
    return (
      <div className="admin-page-container loading-state">
        <LoadingSpinner />
        <p>Loading users...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/admin')} variant="primary">
          Back to Admin Dashboard
        </Button>
      </div>
    );
  }

  if (!currentUser || currentUser.role !== 'admin') {
    return (
      <div className="admin-page-container error-state">
        <p className="error-message">Access Denied: You must be an administrator to view this page.</p>
        <Button onClick={() => navigate('/')} variant="primary">
          Go to Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div className="admin-page-container">
      <h1 className="admin-page-title">Manage Users</h1>

      <UserTable
        users={users}
        onEditUser={handleEditUser}
        onDeleteUser={handleDeleteUser}
        isLoading={loading}
        error={error}
      />

      <Modal isOpen={isEditModalOpen} onClose={() => { setIsEditModalOpen(false); setEditingUser(null); setEditError(''); }} title={`Edit User: ${editingUser?.username || ''}`}>
        {editingUser && (
          <div className="edit-user-modal-content">
            {editError && <p className="form-error-message">{editError}</p>}
            <InputField
              label="Username"
              type="text"
              name="username"
              value={editingUser.username}
              disabled // Username usually not editable through simple role change
            />
            <InputField
              label="Email"
              type="email"
              name="email"
              value={editingUser.email}
              disabled // Email usually not editable here
            />
            <div className="form-group">
              <label htmlFor="userRole">Role</label>
              <select
                id="userRole"
                name="userRole"
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}
                className="select-field"
                disabled={editingUser.id === currentUser.id && newRole === 'admin'} // Cannot demote self
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <Button onClick={handleSaveRole} disabled={loading}>
              {loading ? 'Saving...' : 'Save Role'}
            </Button>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ManageUsersPage;