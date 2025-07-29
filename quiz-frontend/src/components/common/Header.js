// src/components/common/Header.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Button from './Button';
import './Header.css'; // Create this CSS file

const Header = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <Link to="/" className="app-logo">QuizApp</Link>
        {isAuthenticated && (
          <nav className="main-nav">
            <ul>
              <li><Link to="/quizzes">Quizzes</Link></li>
              <li><Link to="/results">My Results</Link></li>
              {user?.role === 'admin' && (
                <li><Link to="/admin">Admin</Link></li>
              )}
            </ul>
          </nav>
        )}
      </div>
      <div className="header-right">
        {isAuthenticated ? (
          <>
            <span className="user-greeting">Hello, {user?.username} ({user?.role})</span>
            <Button onClick={handleLogout} variant="secondary">Logout</Button>
          </>
        ) : (
          <>
            <Link to="/login"><Button variant="outline">Login</Button></Link>
            <Link to="/register"><Button variant="primary">Register</Button></Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;