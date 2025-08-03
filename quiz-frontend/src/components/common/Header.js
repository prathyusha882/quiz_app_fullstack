// src/components/common/Header.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Header.css';

const Header = ({ user }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleUserMenu = () => {
    setIsUserMenuOpen(!isUserMenuOpen);
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <Link to="/dashboard">
            <h1>Quiz App</h1>
          </Link>
        </div>

        <nav className={`header-nav ${isMenuOpen ? 'nav-open' : ''}`}>
          <ul className="nav-list">
            <li className="nav-item">
              <Link to="/dashboard" className="nav-link">
                Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/quizzes" className="nav-link">
                Quizzes
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/courses" className="nav-link">
                Courses
              </Link>
            </li>
            {user?.role === 'admin' && (
              <>
                <li className="nav-item">
                  <Link to="/admin" className="nav-link">
                    Admin
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/admin/quizzes" className="nav-link">
                    Manage Quizzes
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to="/admin/questions" className="nav-link">
                    Manage Questions
                  </Link>
                </li>
              </>
            )}
          </ul>
        </nav>

        <div className="header-user">
          {user ? (
            <div className="user-menu">
              <button 
                className="user-menu-button"
                onClick={toggleUserMenu}
              >
                <span className="user-name">{user.first_name || user.username}</span>
                <span className="user-avatar">
                  {user.first_name ? user.first_name[0].toUpperCase() : user.username[0].toUpperCase()}
                </span>
              </button>
              
              {isUserMenuOpen && (
                <div className="user-dropdown">
                  <div className="user-info">
                    <p className="user-full-name">
                      {user.first_name} {user.last_name}
                    </p>
                    <p className="user-email">{user.email}</p>
                    <p className="user-role">{user.role}</p>
                  </div>
                  <div className="user-actions">
                    <Link to="/profile" className="dropdown-link">
                      Profile
                    </Link>
                    <Link to="/settings" className="dropdown-link">
                      Settings
                    </Link>
                    <button onClick={handleLogout} className="dropdown-link logout-btn">
                      Logout
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn btn-primary">
                Login
              </Link>
              <Link to="/register" className="btn btn-secondary">
                Register
              </Link>
            </div>
          )}
        </div>

        <button 
          className={`mobile-menu-button ${isMenuOpen ? 'open' : ''}`}
          onClick={toggleMenu}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </header>
  );
};

export default Header;