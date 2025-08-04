// src/services/authService.js

import api from './api';

class AuthService {
  // Login with username and password
  async login(username, password) {
    try {
      const response = await api.post('/api/auth/login/', {
        username,
        password
      });
      
      const { access, refresh, user } = response.data;
      
      // Set default authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      return { access, refresh, user };
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  }

  // OAuth login
  async oauthLogin(provider) {
    try {
      const response = await api.get(`/api/auth/oauth/${provider}/redirect/`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'OAuth login failed');
    }
  }

  // Register new user
  async register(userData) {
    try {
      const response = await api.post('/api/auth/register/', userData);
      
      const { access, refresh, user } = response.data;
      
      // Set default authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      return { access, refresh, user };
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  }

  // Logout
  async logout() {
    try {
      await api.post('/api/auth/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Remove authorization header
      delete api.defaults.headers.common['Authorization'];
    }
  }

  // Refresh token
  async refreshToken(refresh) {
    try {
      const response = await api.post('/api/auth/token/refresh/', {
        refresh
      });
      
      const { access } = response.data;
      
      // Update authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      return { access };
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Token refresh failed');
    }
  }

  // Get current user
  async getCurrentUser() {
    try {
      const response = await api.get('/api/auth/profile/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get user data');
    }
  }

  // Update user profile
  async updateProfile(userData) {
    try {
      const response = await api.put('/api/auth/profile/update/', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Profile update failed');
    }
  }

  // Change password
  async changePassword(oldPassword, newPassword) {
    try {
      await api.post('/api/auth/change-password/', {
        old_password: oldPassword,
        new_password: newPassword
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Password change failed');
    }
  }

  // Forgot password
  async forgotPassword(email) {
    try {
      await api.post('/api/auth/reset-password/', {
        email
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Password reset failed');
    }
  }

  // Reset password
  async resetPassword(token, newPassword) {
    try {
      await api.post('/api/auth/reset-password/confirm/', {
        token,
        new_password: newPassword
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Password reset failed');
    }
  }

  // Verify email
  async verifyEmail(token) {
    try {
      await api.post('/api/auth/verify-email/', {
        token
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Email verification failed');
    }
  }

  // Resend verification email
  async resendVerification(email) {
    try {
      await api.post('/api/auth/resend-verification/', {
        email
      });
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to resend verification');
    }
  }

  // Get user statistics
  async getUserStats() {
    try {
      const response = await api.get('/api/auth/stats/');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get user stats');
    }
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  // Get stored token
  getToken() {
    return localStorage.getItem('access_token');
  }

  // Set token
  setToken(token) {
    localStorage.setItem('access_token', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  // Remove token
  removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
  }
}

export const authService = new AuthService();
