// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import authService from '../services/authService';

// Create a context for authentication
const AuthContext = createContext(null);

/**
 * Provides authentication state and functions to the application.
 * Manages user login, logout, registration, and user data persistence in localStorage.
 */
export const AuthProvider = ({ children }) => {
  console.log('AuthProvider: Component rendered');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null); // Stores user object { id, username, email, role }
  const [authLoading, setAuthLoading] = useState(true);
  const [authError, setAuthError] = useState(null);

  // On initial load, try to retrieve auth state from localStorage
  useEffect(() => {
    try {
      const storedAuth = localStorage.getItem('quiz_isAuthenticated');
      const storedUser = localStorage.getItem('quiz_user');

      if (storedAuth === 'true' && storedUser) {
        setIsAuthenticated(true);
        setUser(JSON.parse(storedUser));
      }
    } catch (error) {
      console.error("Failed to parse stored authentication data:", error);
      // Clear potentially corrupt storage
      localStorage.removeItem('quiz_isAuthenticated');
      localStorage.removeItem('quiz_user');
    } finally {
      setAuthLoading(false);
    }
  }, []);

  // Use real backend login
  const login = async (username, password) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      console.log('AuthContext: Attempting login for user:', username);
      const userData = await authService.login(username, password);
      console.log('AuthContext: Login successful, user data:', userData);
      setIsAuthenticated(true);
      setUser(userData);
      // Store in localStorage for persistence
      localStorage.setItem('quiz_isAuthenticated', 'true');
      localStorage.setItem('quiz_user', JSON.stringify(userData));
      return true;
    } catch (err) {
      console.error('AuthContext: Login failed:', err);
      setAuthError(err.message || 'Login failed. Please try again.');
      setIsAuthenticated(false);
      setUser(null);
      return false;
    } finally {
      setAuthLoading(false);
    }
  };

  // Use real backend registration
  const register = async (username, email, password, password2) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      console.log('AuthContext: Attempting registration for user:', username);
      const userData = await authService.register(username, email, password, password2);
      console.log('AuthContext: Registration successful, user data:', userData);
      setIsAuthenticated(true);
      setUser(userData);
      // Store in localStorage for persistence
      localStorage.setItem('quiz_isAuthenticated', 'true');
      localStorage.setItem('quiz_user', JSON.stringify(userData));
      return true;
    } catch (err) {
      console.error('AuthContext: Registration failed:', err);
      setAuthError(err.message || 'Registration failed. Please try again.');
      setIsAuthenticated(false);
      setUser(null);
      return false;
    } finally {
      setAuthLoading(false);
    }
  };

  // Use real backend logout
  const logout = () => {
    console.log('AuthContext: Logging out user');
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
    setAuthError(null);
    // Clear localStorage
    localStorage.removeItem('quiz_isAuthenticated');
    localStorage.removeItem('quiz_user');
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      authLoading,
      authError,
      login,
      register,
      logout,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to easily consume the AuthContext.
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};