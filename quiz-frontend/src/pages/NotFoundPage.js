// src/pages/NotFoundPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import './NotFoundPage.css'; // Dedicated CSS for 404 page

/**
 * Generic 404 Not Found Page.
 */
const NotFoundPage = () => {
  return (
    <div className="not-found-container">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for does not exist or an unexpected error occurred.</p>
      <Link to="/" className="home-link">Go to Dashboard</Link>
    </div>
  );
};

export default NotFoundPage;