// src/pages/Dashboard/AdminDashboard.js
import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
import Button from '../../components/common/Button';
import './DashboardPages.css'; // Common styling for dashboard pages

/**
 * Admin Dashboard Page. Displays administrative overview and quick links for management.
 */
const AdminDashboard = () => {
  const { user } = useAuth(); // Get current user from AuthContext

  if (!user || user.role !== 'admin') {
    // This should also be caught by a more robust role-based route guard
    return <p>Access Denied: You must be an administrator to view this page.</p>;
  }

  return (
    <div className="dashboard-page-container">
      <h1 className="dashboard-title">Admin Dashboard</h1>
      <p className="dashboard-greeting">Welcome, {user.username}. Here's your overview.</p>

      <section className="dashboard-section">
        <h2 className="section-title">Admin Quick Links</h2>
        <div className="quick-actions-grid">
          <Link to="/admin/quizzes" className="action-card admin-card">
            <h3>Manage Quizzes</h3>
            <p>Add, edit, or delete quizzes.</p>
            <Button variant="primary">Go to Quizzes</Button>
          </Link>
          <Link to="/admin/questions" className="action-card admin-card">
            <h3>Manage Questions</h3>
            <p>Add, edit, or delete questions for quizzes.</p>
            <Button variant="primary">Go to Questions</Button>
          </Link>
          <Link to="/admin/users" className="action-card admin-card">
            <h3>Manage Users</h3>
            <p>View, edit roles, or delete user accounts.</p>
            <Button variant="primary">Go to Users</Button>
          </Link>
          <Link to="/admin/results" className="action-card admin-card">
            <h3>View All Results</h3>
            <p>Analyze overall quiz performance.</p>
            <Button variant="primary">See All Results</Button>
          </Link>
        </div>
      </section>

      {/* Optionally, display key metrics or recent admin activities */}
      <section className="dashboard-section">
        <h2 className="section-title">System Overview</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h4>Total Quizzes</h4>
            <p className="stat-value">50+</p>
          </div>
          <div className="stat-card">
            <h4>Total Users</h4>
            <p className="stat-value">1,200+</p>
          </div>
          <div className="stat-card">
            <h4>Quizzes Taken</h4>
            <p className="stat-value">5,000+</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AdminDashboard;