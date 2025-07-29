// src/pages/Results/UserResultsPage.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import './ResultPages.css'; // Common styling for results pages

// Dummy data for user quiz results
const dummyUserResults = {
  'user': [
    {
      id: 'res-u1-q1', quizId: 'q1', quizTitle: 'React Basics', score: 2, totalQuestions: 3,
      timeTaken: '05:30', dateCompleted: '2025-07-15T10:00:00Z',
      userAnswers: {}, // Simplified for this data structure
      correctAnswers: [], // Simplified
    },
    {
      id: 'res-u1-q3', quizId: 'q3', quizTitle: 'HTML & CSS Fundamentals', score: 4, totalQuestions: 5,
      timeTaken: '07:15', dateCompleted: '2025-07-10T14:30:00Z',
      userAnswers: {}, correctAnswers: [],
    },
  ],
  'admin': [ // Admins might have results too
    {
      id: 'res-a1-q1', quizId: 'q1', quizTitle: 'React Basics', score: 3, totalQuestions: 3,
      timeTaken: '04:00', dateCompleted: '2025-07-16T09:00:00Z',
      userAnswers: {}, correctAnswers: [],
    },
  ]
};


/**
 * User Results Page. Displays a list of quizzes taken by the current user and their results.
 */
const UserResultsPage = () => {
  const { user, authLoading } = useAuth();
  const navigate = useNavigate();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserResults = async () => {
      if (authLoading || !user) {
        // Wait for auth to load or user to be available
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay

        // Fetch results based on the logged-in user's username (or ID)
        const userSpecificResults = dummyUserResults[user.username] || [];
        setResults(userSpecificResults);
      } catch (err) {
        setError('Failed to load your results. Please try again.');
        console.error('Error fetching user results:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchUserResults();
  }, [user, authLoading]); // Re-run when user or authLoading changes

  const handleReviewAnswers = (quizId, dateCompleted) => {
    // This path should ideally map to an endpoint that can fetch full quiz questions and user's answers
    navigate(`/results/review/${quizId}/${encodeURIComponent(dateCompleted)}`);
  };

  if (authLoading || loading) {
    return (
      <div className="results-page-container loading-state">
        <LoadingSpinner />
        <p>Loading your results...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/')} variant="primary">
          Go to Dashboard
        </Button>
      </div>
    );
  }

  if (!user) {
    // Should be redirected by PrivateRoute, but a fallback
    return <p className="results-info-message">Please log in to view your results.</p>;
  }

  if (results.length === 0) {
    return (
      <div className="results-page-container empty-state">
        <p className="results-info-message">You haven't completed any quizzes yet.</p>
        <Button onClick={() => navigate('/quizzes')} variant="primary">
          Start a Quiz
        </Button>
      </div>
    );
  }

  return (
    <div className="results-page-container">
      <h1 className="results-page-title">My Quiz Results</h1>
      <table className="results-table">
        <thead>
          <tr>
            <th>Quiz Title</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Time Taken</th>
            <th>Date Completed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result) => {
            const percentage = ((result.score / result.totalQuestions) * 100).toFixed(0);
            const date = new Date(result.dateCompleted).toLocaleDateString();
            const time = new Date(result.dateCompleted).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return (
              <tr key={result.id} className={percentage >= 70 ? 'result-passed' : 'result-failed'}>
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

export default UserResultsPage;