// quiz-frontend/src/pages/Dashboard/UserDashboard.js
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './UserDashboard.css';

const UserDashboard = () => {
  const { user } = useAuth();

  return (
    <div className="user-dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.first_name || user?.username}!</h1>
        <p>Here's your learning dashboard</p>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>0</h3>
          <p>Quizzes Taken</p>
        </div>
        <div className="stat-card">
          <h3>0</h3>
          <p>Courses Enrolled</p>
        </div>
        <div className="stat-card">
          <h3>0%</h3>
          <p>Average Score</p>
        </div>
      </div>

      <div className="dashboard-actions">
        <Link to="/quizzes" className="action-card">
          <h3>Take a Quiz</h3>
          <p>Test your knowledge</p>
        </Link>
        <Link to="/courses" className="action-card">
          <h3>Browse Courses</h3>
          <p>Learn new skills</p>
        </Link>
        <Link to="/results" className="action-card">
          <h3>View Results</h3>
          <p>Check your progress</p>
        </Link>
      </div>
    </div>
  );
};

export default UserDashboard;
