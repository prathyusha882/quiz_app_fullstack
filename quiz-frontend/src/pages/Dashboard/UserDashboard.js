// quiz-frontend/src/pages/Dashboard/UserDashboard.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
// Temporarily comment out imports that might be causing issues
// import Button from '../../components/common/Button';
// import LoadingSpinner from '../../components/common/LoadingSpinner';
// import progressService from '../../services/progressService';
// Temporarily comment out Chart.js imports to test if they're causing issues
// import { Line } from 'react-chartjs-2';
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend,
// } from 'chart.js';

import './DashboardPages.css';

// Temporarily comment out Chart.js registration
// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend
// );

const UserDashboard = () => {
  console.log('UserDashboard: Component rendered - MINIMAL VERSION');
  const { user } = useAuth();
  console.log('UserDashboard: User from context:', user);
  
  // Return a very simple component for testing
  return (
    <div style={{ padding: '20px', backgroundColor: 'lightblue' }}>
      <h1>UserDashboard is working!</h1>
      <p>User: {user ? user.username : 'No user'}</p>
      <p>This is a minimal test version</p>
    </div>
  );

  // All the complex logic is temporarily removed for debugging
};

export default UserDashboard;
