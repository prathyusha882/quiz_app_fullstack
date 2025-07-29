// src/pages/Results/AdminResultsPage.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import './ResultPages.css';

// Combined dummy results for all users (Admin view)
const dummyAllResults = [
  { id: 'res-u1-q1', userId: 1, username: 'user', quizId: 'q1', quizTitle: 'React Basics', score: 2, totalQuestions: 3, timeTaken: '05:30', dateCompleted: '2025-07-15T10:00:00Z' },
  { id: 'res-u1-q3', userId: 1, username: 'user', quizId: 'q3', quizTitle: 'HTML & CSS Fundamentals', score: 4, totalQuestions: 5, timeTaken: '07:15', dateCompleted: '2025-07-10T14:30:00Z' },
  { id: 'res-u2-q1', userId: 2, username: 'admin', quizId: 'q1', quizTitle: 'React Basics', score: 3, totalQuestions: 3, timeTaken: '04:00', dateCompleted: '2025-07-16T09:00:00Z' },
  { id: 'res-u3-q2', userId: 3, username: 'newuser', quizId: 'q2', quizTitle: 'JavaScript Advanced', score: 1, totalQuestions: 2, timeTaken: '06:00', dateCompleted: '2025-07-14T11:00:00Z' },
];

/**
 * Admin Results Page. Displays all quiz results across all users.
 */
const AdminResultsPage = () => {
  const { user, authLoading } = useAuth();
  const navigate = useNavigate();
  const [allResults, setAllResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllResults = async () => {
      if (authLoading) {
        setLoading(false);
        return;
      }

      if (!user || user.role !== 'admin') {
        setError('Access Denied: You must be an administrator to view this page.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API delay
        setAllResults(dummyAllResults);
      } catch (err) {
        setError('Failed to load all results. Please try again.');
        console.error('Error fetching all results:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllResults();
  }, [user, authLoading]);

  const handleReviewAnswers = (quizId, dateCompleted) => {
    // This path should ideally map to an endpoint that can fetch full quiz questions and user's answers
    navigate(`/results/review/${quizId}/${encodeURIComponent(dateCompleted)}`);
  };

  if (authLoading || loading) {
    return (
      <div className="results-page-container loading-state">
        <LoadingSpinner />
        <p>Loading all results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/admin')} variant="primary">
          Back to Admin Dashboard
        </Button>
      </div>
    );
  }

  if (!user || user.role !== 'admin') {
    return (
      <div className="results-page-container error-state">
        <p className="error-message">Access Denied: You must be an administrator to view this page.</p>
        <Button onClick={() => navigate('/')} variant="primary">
          Go to Dashboard
        </Button>
      </div>
    );
  }

  if (allResults.length === 0) {
    return (
      <div className="results-page-container empty-state">
        <p className="results-info-message">No quiz results recorded yet.</p>
      </div>
    );
  }

  return (
    <div className="results-page-container">
      <h1 className="results-page-title">All Quiz Results</h1>
      <table className="results-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Quiz Title</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Time Taken</th>
            <th>Date Completed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {allResults.map((result) => {
            const percentage = ((result.score / result.totalQuestions) * 100).toFixed(0);
            const date = new Date(result.dateCompleted).toLocaleDateString();
            const time = new Date(result.dateCompleted).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return (
              <tr key={result.id} className={percentage >= 70 ? 'result-passed' : 'result-failed'}>
                <td>{result.username}</td>
                <td>{result.quizTitle}</td>
                <td>{result.score} / {result.totalQuestions}</td>
                <td>{percentage}%</td>
                <td>{result.timeTaken}</td>
                <td>{date} {time}</td>
                <td>
                  <Button
                    onClick={() => handleReviewAnswers(result.quizId, result.dateCompleted)}
                    variant="secondary"
                    className="action-btn"
                  >
                    Review
                  </Button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default AdminResultsPage;