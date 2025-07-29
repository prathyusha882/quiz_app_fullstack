// src/services/authService.js
import api from './api'; // Import the configured axios instance

const AUTH_STORAGE_KEY = 'quiz_authToken';
const USER_STORAGE_KEY = 'quiz_user';
const IS_AUTH_STORAGE_KEY = 'quiz_isAuthenticated';

/**
 * Stores authentication token and user data in localStorage.
 * @param {string} token - JWT or session token.
 * @param {object} user - User object (e.g., { id, username, email, role }).
 */
const setAuthData = (token, user) => {
  localStorage.setItem(AUTH_STORAGE_KEY, token);
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
  localStorage.setItem(IS_AUTH_STORAGE_KEY, 'true');
};

/**
 * Clears authentication token and user data from localStorage.
 */
const clearAuthData = () => {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
  localStorage.removeItem(IS_AUTH_STORAGE_KEY);
};

/**
 * Retrieves authentication token from localStorage.
 * @returns {string | null} The authentication token or null if not found.
 */
const getAuthToken = () => {
  return localStorage.getItem(AUTH_STORAGE_KEY);
};

/**
 * Retrieves user data from localStorage.
 * @returns {object | null} The user object or null if not found/parsed.
 */
const getUserData = () => {
  const userData = localStorage.getItem(USER_STORAGE_KEY);
  return userData ? JSON.parse(userData) : null;
};

/**
 * Checks if the user is authenticated based on localStorage.
 * @returns {boolean} True if authenticated, false otherwise.
 */
const isAuthenticated = () => {
  return localStorage.getItem(IS_AUTH_STORAGE_KEY) === 'true' && !!getAuthToken();
};

/**
 * Handles user login.
 * @param {string} username - User's username.
 * @param {string} password - User's password.
 * @returns {Promise<object>} A promise that resolves with user data on success.
 */
const login = async (username, password) => {
  try {
    // In a real app, replace with actual API endpoint
    const response = await api.post('/auth/login', { username, password });
    const { token, user } = response.data; // Assuming API returns token and user object
    setAuthData(token, user);
    return user;
  } catch (error) {
    console.error('Login service error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Login failed');
  }
};

/**
 * Handles user registration.
 * @param {string} username - New user's username.
 * @param {string} email - New user's email.
 * @param {string} password - New user's password.
 * @returns {Promise<object>} A promise that resolves with user data on success.
 */
const register = async (username, email, password) => {
  try {
    // In a real app, replace with actual API endpoint
    const response = await api.post('/auth/register', { username, email, password });
    const { token, user } = response.data; // Assuming API returns token and user object
    setAuthData(token, user); // Log in immediately after registration
    return user;
  } catch (error) {
    console.error('Register service error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Registration failed');
  }
};

/**
 * Handles user logout.
 */
const logout = () => {
  clearAuthData();
  // Optionally, send a request to backend to invalidate token
  // api.post('/auth/logout');
};

const authService = {
  login,
  register,
  logout,
  getAuthToken,
  getUserData,
  isAuthenticated,
};

export default authService;