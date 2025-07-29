// src/components/admin/UserTable.js
import React from 'react';
import Button from '../common/Button';
import './UserTable.css';

/**
 * Displays a table of users for administrative management.
 * @param {object} props - The component props.
 * @param {Array<object>} props.users - An array of user objects.
 * @param {function} [props.onEditUser] - Callback for editing a user's role or details.
 * @param {function} [props.onDeleteUser] - Callback for deleting a user.
 * @param {boolean} [props.isLoading=false] - Indicates if the table data is loading.
 * @param {string} [props.error] - Error message to display if fetching users failed.
 */
const UserTable = ({ users, onEditUser, onDeleteUser, isLoading = false, error }) => {
  if (isLoading) {
    return <p className="user-table-info">Loading users...</p>; // Or use a LoadingSpinner
  }

  if (error) {
    return <p className="user-table-info error-message">{error}</p>;
  }

  if (!users || users.length === 0) {
    return <p className="user-table-info">No users found.</p>;
  }

  return (
    <div className="user-table-container">
      <h3>Manage Users</h3>
      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td className="user-actions">
                {onEditUser && (
                  <Button onClick={() => onEditUser(user.id)} variant="secondary" className="action-btn">
                    Edit
                  </Button>
                )}
                {onDeleteUser && (
                  <Button onClick={() => onDeleteUser(user.id)} variant="danger" className="action-btn">
                    Delete
                  </Button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;