// src/services/authService.js

import api from './api'; // Uses the configured axios instance

// ✅ Keys for localStorage
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_STORAGE_KEY = 'quiz_user';
const IS_AUTH_STORAGE_KEY = 'quiz_isAuthenticated';

/**
 * Save auth data to localStorage.
 * @param {string} accessToken - JWT access token.
 * @param {string} refreshToken - JWT refresh token.
 * @param {object} user - User data object.
 */
const setAuthData = (accessToken, refreshToken, user) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
  localStorage.setItem(IS_AUTH_STORAGE_KEY, 'true');
};

/**
 * Remove auth data from localStorage.
 */
const clearAuthData = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
  localStorage.removeItem(IS_AUTH_STORAGE_KEY);
};

/**
 * Get access token from localStorage.
 */
const getAuthToken = () => localStorage.getItem(ACCESS_TOKEN_KEY);

/**
 * Get stored user object from localStorage.
 */
const getUserData = () => {
  const userData = localStorage.getItem(USER_STORAGE_KEY);
  return userData ? JSON.parse(userData) : null;
};

/**
 * Check if user is authenticated.
 */
const isAuthenticated = () => {
  return localStorage.getItem(IS_AUTH_STORAGE_KEY) === 'true' && !!getAuthToken();
};

/**
 * Handle login: calls backend, stores tokens and user.
 */
const login = async (username, password) => {
  try {
    const response = await api.post('/api/auth/login/', { username, password });

    console.log('Login response:', response.data);

    // Handle both response formats (with and without user field)
    const { access, refresh, user } = response.data;
    
    // If user field is not in response, create user object from available data
    const userData = user || {
      id: response.data.id || null,
      username: response.data.username || username,
      email: response.data.email || '',
      role: response.data.role || 'user',
      date_joined: response.data.date_joined || new Date().toISOString(),
      last_login: response.data.last_login || new Date().toISOString(),
    };

    setAuthData(access, refresh, userData);

    return userData;
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

/**
 * Handle registration: registers and logs in.
 */
const register = async (username, email, password, password2) => {
  try {
    console.log('Registering with data:', { username, email, password, password2 });
    
    const response = await api.post('/api/auth/register/', {
      username,
      email,
      password,
      password2: password2 || password, // Use password2 if provided, otherwise use password
    });

    console.log('Registration response:', response.data);

    // Backend returns 'token' and 'refresh_token' instead of 'access' and 'refresh'
    const { token: access, refresh_token: refresh, user } = response.data;
    
    // If user field is not in response, create user object from available data
    const userData = user || {
      id: response.data.id || null,
      username: response.data.username || username,
      email: response.data.email || email,
      role: response.data.role || 'student',
      date_joined: response.data.date_joined || new Date().toISOString(),
      last_login: response.data.last_login || new Date().toISOString(),
    };
    
    setAuthData(access, refresh, userData);

    return userData;
  } catch (error) {
    console.error('Register error:', error.response?.data || error.message);
    
    // Provide more specific error messages
    if (error.response?.data?.username) {
      throw new Error(`Username error: ${error.response.data.username[0]}`);
    } else if (error.response?.data?.email) {
      throw new Error(`Email error: ${error.response.data.email[0]}`);
    } else if (error.response?.data?.password) {
      throw new Error(`Password error: ${error.response.data.password[0]}`);
    } else if (error.response?.data?.password2) {
      throw new Error(`Password confirmation error: ${error.response.data.password2[0]}`);
    } else {
      throw new Error(error.response?.data?.detail || 'Registration failed. Please try again.');
    }
  }
};

/**
 * Logout: clears tokens and user data.
 */
const logout = () => {
  clearAuthData();
  // Optional: send logout request to backend if refresh token is blacklisted
  // return api.post('/auth/logout', { refresh_token: getRefreshToken() });
};

/**
 * Optional: Get refresh token if needed elsewhere
 */
const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN_KEY);

const authService = {
  login,
  register,
  logout,
  getAuthToken,
  getRefreshToken,
  getUserData,
  isAuthenticated,
};

export default authService;
