// quiz-frontend/src/pages/Dashboard/UserDashboard.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Link } from 'react-router-dom';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import progressService from '../../services/progressService';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

import './DashboardPages.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const UserDashboard = () => {
  const { user } = useAuth();
  const [progressData, setProgressData] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(true);
  const [progressError, setProgressError] = useState(null);

  useEffect(() => {
    const fetchProgress = async () => {
      const token = localStorage.getItem("access_token");

      if (!user || !token) {
        console.warn("⚠️ User not logged in or token missing.");
        setLoadingProgress(false);
        return;
      }

      setLoadingProgress(true);
      setProgressError(null);
      try {
        const data = await progressService.getProgressData(token); // ✅ Pass token here
        setProgressData(data);
      } catch (err) {
        console.error("❌ Error fetching progress:", err);
        setProgressError(err.message || 'Could not load progress data.');
      } finally {
        setLoadingProgress(false);
      }
    };

    fetchProgress();
  }, [user]);

  if (!user) {
    return <p>User data not available. Please log in.</p>;
  }

  const chartData = {
    labels: progressData?.last_5_quizzes_scores.map((s, index) => `Quiz ${progressData.last_5_quizzes_scores.length - index}`) || [],
    datasets: [
      {
        label: 'Score Percentage',
        data: progressData?.last_5_quizzes_scores.map(s => s.percentage) || [],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Last 5 Quiz Scores (Percentage)',
      },
      tooltip: {
        callbacks: {
          title: function (tooltipItems) {
            return progressData?.last_5_quizzes_scores[chartData.labels.length - 1 - tooltipItems[0].dataIndex]?.quiz_title || 'Quiz';
          },
          label: function (tooltipItem) {
            let label = tooltipItem.dataset.label || '';
            if (label) label += ': ';
            label += tooltipItem.raw + '%';
            return label;
          },
        },
      },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        title: {
          display: true,
          text: 'Percentage Score (%)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Quiz Attempt (Newest to Oldest)',
        },
      },
    },
  };

  return (
    <div className="dashboard-page-container">
      <h1 className="dashboard-title">Welcome, {user.username}!</h1>
      <p className="dashboard-greeting">Your personal space for quizzes and learning.</p>

      <section className="dashboard-section">
        <h2 className="section-title">Quick Actions</h2>
        <div className="quick-actions-grid">
          <Link to="/quizzes" className="action-card">
            <h3>Explore Quizzes</h3>
            <p>Find new quizzes to test your knowledge.</p>
            <Button variant="outline">Browse Quizzes</Button>
          </Link>
          <Link to="/results" className="action-card">
            <h3>View My Results</h3>
            <p>Check your past quiz scores and progress.</p>
            <Button variant="outline">See Results</Button>
          </Link>
          <div className="action-card coming-soon">
            <h3>Challenge Friends</h3>
            <p>Coming Soon!</p>
            <Button disabled>Invite & Play</Button>
          </div>
        </div>
      </section>

      <section className="dashboard-section">
        <h2 className="section-title">Your Progress</h2>
        {loadingProgress ? (
          <LoadingSpinner />
        ) : progressError ? (
          <p className="error-message">{progressError}</p>
        ) : progressData && progressData.total_quizzes_attempted > 0 ? (
          <div className="progress-graph-container">
            <div className="progress-summary">
              <p>Total Quizzes Attempted: <strong>{progressData.total_quizzes_attempted}</strong></p>
              <p>Average Score: <strong>{progressData.average_score_percentage}%</strong></p>
            </div>
            <div className="chart-wrapper">
              <Line data={chartData} options={chartOptions} />
            </div>
          </div>
        ) : (
          <div className="progress-graph-placeholder">
            <p>No quiz attempts yet. Start a quiz to see your progress!</p>
            <Link to="/quizzes"><Button variant="primary">Browse Quizzes</Button></Link>
          </div>
        )}
      </section>
    </div>
  );
};

export default UserDashboard;
