// src/components/common/Header.js
import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Header.css';

const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
    setIsUserMenuOpen(false);
  };

  const isActiveRoute = (path) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  const getNavItems = () => {
    if (!isAuthenticated) {
      return [
        { path: '/quizzes', label: 'Browse Quizzes', icon: '📚' },
        { path: '/login', label: 'Login', icon: '🔐' },
        { path: '/register', label: 'Register', icon: '📝' },
      ];
    }

    if (user?.role === 'admin') {
      return [
        { path: '/', label: 'Dashboard', icon: '📊' },
        { path: '/admin/quizzes', label: 'Manage Quizzes', icon: '🎯' },
        { path: '/admin/users', label: 'Manage Users', icon: '👥' },
        { path: '/admin/results', label: 'Analytics', icon: '📈' },
      ];
    }

    return [
      { path: '/', label: 'Dashboard', icon: '📊' },
      { path: '/quizzes', label: 'My Quizzes', icon: '📚' },
      { path: '/results', label: 'Results', icon: '📋' },
    ];
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled 
        ? 'bg-white/95 backdrop-blur-md shadow-soft border-b border-gray-200' 
        : 'bg-white/80 backdrop-blur-sm'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-glow group-hover:shadow-glow-primary transition-all duration-300">
              <span className="text-white text-xl font-bold">Q</span>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-display font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
                QuizMaster
              </h1>
              <p className="text-xs text-secondary-500 -mt-1">Learning Platform</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {getNavItems().map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  isActiveRoute(item.path)
                    ? 'bg-primary-50 text-primary-700 border border-primary-200'
                    : 'text-secondary-600 hover:text-primary-600 hover:bg-primary-50'
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>

          {/* User Menu & Actions */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            {isAuthenticated && (
              <div className="relative">
                <button className="p-2 text-secondary-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200 relative">
                  <span className="text-xl">🔔</span>
                  {notifications.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-danger-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center animate-bounce">
                      {notifications.length}
                    </span>
                  )}
                </button>
              </div>
            )}

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="flex items-center space-x-3 p-2 rounded-lg hover:bg-primary-50 transition-all duration-200"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user?.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div className="hidden sm:block text-left">
                    <p className="text-sm font-medium text-secondary-900">
                      {user?.username}
                    </p>
                    <p className="text-xs text-secondary-500 capitalize">
                      {user?.role}
                    </p>
                  </div>
                  <span className="text-secondary-400">▼</span>
                </button>

                {/* Dropdown Menu */}
                {isUserMenuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-large border border-gray-200 py-2 animate-scale-in">
                    <div className="px-4 py-3 border-b border-gray-100">
                      <p className="text-sm font-medium text-secondary-900">
                        {user?.username}
                      </p>
                      <p className="text-xs text-secondary-500 capitalize">
                        {user?.role}
                      </p>
                    </div>
                    
                    <div className="py-1">
                      <Link
                        to="/profile"
                        className="flex items-center px-4 py-2 text-sm text-secondary-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        <span className="mr-3">👤</span>
                        Profile
                      </Link>
                      <Link
                        to="/settings"
                        className="flex items-center px-4 py-2 text-sm text-secondary-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        <span className="mr-3">⚙️</span>
                        Settings
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="flex items-center w-full px-4 py-2 text-sm text-danger-600 hover:bg-danger-50 transition-colors"
                      >
                        <span className="mr-3">🚪</span>
                        Logout
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="px-4 py-2 text-secondary-600 hover:text-primary-600 font-medium transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition-all duration-200 shadow-soft hover:shadow-medium"
                >
                  Get Started
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-secondary-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200"
            >
              <span className="text-xl">{isMenuOpen ? '✕' : '☰'}</span>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 bg-white/95 backdrop-blur-md animate-slide-down">
            <div className="px-4 py-4 space-y-2">
              {getNavItems().map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                    isActiveRoute(item.path)
                      ? 'bg-primary-50 text-primary-700 border border-primary-200'
                      : 'text-secondary-600 hover:text-primary-600 hover:bg-primary-50'
                  }`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;