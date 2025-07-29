// src/services/userService.js
import api from './api';

/**
 * Fetches all users (admin only).
 * @returns {Promise<Array<object>>} A promise that resolves with an array of user objects.
 */
const getAllUsers = async () => {
  try {
    const response = await api.get('/admin/users'); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error('Error fetching all users:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch users');
  }
};

/**
 * Updates a user's role (admin only).
 * @param {string} userId - The ID of the user to update.
 * @param {string} newRole - The new role for the user ('user' or 'admin').
 * @returns {Promise<object>} A promise that resolves with the updated user object.
 */
const updateUserRole = async (userId, newRole) => {
  try {
    const response = await api.put(`/admin/users/${userId}/role`, { role: newRole }); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error(`Error updating user ${userId} role:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to update user role');
  }
};

/**
 * Deletes a user (admin only).
 * @param {string} userId - The ID of the user to delete.
 * @returns {Promise<void>} A promise that resolves on successful deletion.
 */
const deleteUser = async (userId) => {
  try {
    await api.delete(`/admin/users/${userId}`); // Admin endpoint
  } catch (error) {
    console.error(`Error deleting user ${userId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to delete user');
  }
};

// You might add functions for getting a single user's profile, updating own profile etc.
const userService = {
  getAllUsers,
  updateUserRole,
  deleteUser,
};

export default userService;