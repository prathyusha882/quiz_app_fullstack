// src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is logged in on app start
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  // Login function
  const login = async (username, password) => {
    try {
      setError(null);
      const response = await authService.login(username, password);
      const { access, refresh, user: userData } = response;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      setUser(userData);
      
      return true;
    } catch (error) {
      setError(error.message || 'Login failed');
      return false;
    }
  };

  // OAuth login function
  const oauthLogin = async (provider) => {
    try {
      setError(null);
      const response = await authService.oauthLogin(provider);
      return response;
    } catch (error) {
      setError(error.message || 'OAuth login failed');
      return { success: false, error: error.message };
    }
  };

  // Register function
  const register = async (username, email, password, confirmPassword) => {
    try {
      setError(null);
      const userData = {
        username,
        email,
        password,
        confirm_password: confirmPassword
      };
      const response = await authService.register(userData);
      const { access, refresh, user: newUser } = response;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      setUser(newUser);
      
      return true;
    } catch (error) {
      setError(error.message || 'Registration failed');
      return false;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  // Refresh token function
  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) {
        throw new Error('No refresh token');
      }

      const response = await authService.refreshToken(refresh);
      const { access } = response;
      
      localStorage.setItem('access_token', access);
      return access;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      throw error;
    }
  };

  // Update user profile
  const updateProfile = async (userData) => {
    try {
      setError(null);
      const updatedUser = await authService.updateProfile(userData);
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      setError(error.message || 'Profile update failed');
      return { success: false, error: error.message };
    }
  };

  // Change password
  const changePassword = async (oldPassword, newPassword) => {
    try {
      setError(null);
      await authService.changePassword(oldPassword, newPassword);
      return { success: true };
    } catch (error) {
      setError(error.message || 'Password change failed');
      return { success: false, error: error.message };
    }
  };

  // Forgot password
  const forgotPassword = async (email) => {
    try {
      setError(null);
      await authService.forgotPassword(email);
      return { success: true };
    } catch (error) {
      setError(error.message || 'Password reset failed');
      return { success: false, error: error.message };
    }
  };

  // Reset password
  const resetPassword = async (token, newPassword) => {
    try {
      setError(null);
      await authService.resetPassword(token, newPassword);
      return { success: true };
    } catch (error) {
      setError(error.message || 'Password reset failed');
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    oauthLogin,
    register,
    logout,
    refreshToken,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    clearError: () => setError(null)
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};