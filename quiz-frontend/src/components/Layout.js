import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Layout.css'; // Add some basic styling for layout

const Layout = () => {
  const { user, logout } = useAuth();

  return (
    <div className="layout-container">
      <header className="layout-header">
        <nav>
          <ul className="layout-nav">
            <li>
              <Link to="/">Dashboard</Link>
            </li>
            {/* Add more navigation links here */}
          </ul>
        </nav>
        <div className="user-info">
          <span>Welcome, {user ? user.username : 'Guest'}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </header>
      <main className="layout-main">
        <Outlet /> {/* Renders the child route components */}
      </main>
      <footer className="layout-footer">
        <p>&copy; 2025 My Web App</p>
      </footer>
    </div>
  );
};

export default Layout;