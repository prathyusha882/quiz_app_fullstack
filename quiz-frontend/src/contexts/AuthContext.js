// src/contexts/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

// Create a context for authentication
const AuthContext = createContext(null);

/**
 * Provides authentication state and functions to the application.
 * Manages user login, logout, registration, and user data persistence in localStorage.
 */
export const AuthProvider = ({ children }) => {
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

  /**
   * Simulates a login API call.
   * In a real application, this would involve sending credentials to a backend
   * and receiving a token/user data.
   */
  const login = async (username, password) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));

      // Dummy authentication logic
      if (username === 'user' && password === 'password') {
        const userData = { id: 1, username: 'user', email: 'user@example.com', role: 'user' };
        setIsAuthenticated(true);
        setUser(userData);
        localStorage.setItem('quiz_isAuthenticated', 'true');
        localStorage.setItem('quiz_user', JSON.stringify(userData));
        return true;
      } else if (username === 'admin' && password === 'adminpass') {
        const userData = { id: 2, username: 'admin', email: 'admin@example.com', role: 'admin' };
        setIsAuthenticated(true);
        setUser(userData);
        localStorage.setItem('quiz_isAuthenticated', 'true');
        localStorage.setItem('quiz_user', JSON.stringify(userData));
        return true;
      } else {
        setAuthError('Invalid username or password.');
        return false;
      }
    } catch (err) {
      setAuthError('Login failed. Please try again.');
      console.error('Login error:', err);
      return false;
    } finally {
      setAuthLoading(false);
    }
  };

  /**
   * Simulates a user registration API call.
   * In a real app, this sends new user data to the backend.
   */
  const register = async (username, email, password) => {
    setAuthLoading(true);
    setAuthError(null);
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));

      // Dummy registration logic: success if email not 'taken@example.com'
      if (email === 'taken@example.com') {
        setAuthError('Email already registered.');
        return false;
      }

      // After successful registration, automatically log them in (optional)
      const userData = { id: Date.now(), username, email, role: 'user' }; // Assign default 'user' role
      setIsAuthenticated(true);
      setUser(userData);
      localStorage.setItem('quiz_isAuthenticated', 'true');
      localStorage.setItem('quiz_user', JSON.stringify(userData));
      return true;
    } catch (err) {
      setAuthError('Registration failed. Please try again.');
      console.error('Registration error:', err);
      return false;
    } finally {
      setAuthLoading(false);
    }
  };

  /**
   * Logs out the current user, clears state and localStorage.
   */
  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
    localStorage.removeItem('quiz_isAuthenticated');
    localStorage.removeItem('quiz_user');
    setAuthError(null); // Clear any previous errors on logout
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
      // You can add more like: checkAuthStatus, updateUserProfile
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