// quiz-frontend/src/pages/Results/AnswerReviewPage.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AnswerReview from '../../components/results/AnswerReview'; // Assuming you have this component
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import { useAuth } from '../../contexts/AuthContext'; // To ensure user is logged in
// You might need a specific service function here to fetch detailed result for review
import quizService from '../../services/quizService'; // For fetching result details

import './ResultPages.css'; // Consistent styling

/**
 * Page to display a detailed review of a specific quiz attempt.
 * Fetches the full quiz attempt details including user answers and correct answers.
 */
const AnswerReviewPage = () => {
  const { quizId, resultId } = useParams(); // resultId will be the encoded date string
  const navigate = useNavigate();
  const { isAuthenticated, authLoading } = useAuth(); // Check auth status
  const [reviewData, setReviewData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReviewDetails = async () => {
      if (authLoading) {
        setLoading(false);
        return;
      }
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        navigate('/login', { replace: true });
        return;
      }

      setLoading(true);
      setError(null);
      try {
        // Call backend API to get the detailed quiz attempt for review
        // Note: The backend's results/views.py has QuizAttemptReviewView
        // which expects attempt_id, but your URL has resultId (which is date).
        // You'll need to decide how your backend identifies specific attempts
        // based on the frontend's URL structure.
        // For now, let's assume resultId can be used to query the backend.
        // If your backend identifies attempts by a simple ID, you'd need that ID.
        // If the backend expects the date string, make sure it's decoded.

        // Example: If backend expects a unique ID for the attempt, not the date string
        // You might need to change your frontend's navigation or backend's URL/view logic.
        // For now, let's just make a dummy call.

        // In a real app, this would be quizService.getQuizResult(quizId, resultId);
        // And quizService.getQuizResult would call your backend's /api/results/<attempt_id>/review/ endpoint.

        // Dummy data for review
        await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API delay

        // Example dummy review data structure (this should come from your backend)
        const dummyReview = {
          quizTitle: `Quiz ${quizId} Review`,
          questions: [
            { id: 'q1-1', text: 'What is 1+1?', type: 'multiple-choice', options: ['1', '2', '3'], correctAnswers: ['2'] },
            { id: 'q1-2', text: 'Which colors are in RGB?', type: 'checkbox', options: ['Red', 'Green', 'Blue', 'Yellow'], correctAnswers: ['Red', 'Green', 'Blue'] },
          ],
          userAnswers: {
            'q1-1': '2',
            'q1-2': ['Red', 'Blue'], // User chose Red and Blue
          },
          correctAnswers: {
            'q1-1': ['2'],
            'q1-2': ['Red', 'Green', 'Blue'],
          },
        };

        // You'd format dummyReview's `correctAnswers` and `userAnswers` to match `AnswerReview` props
        const formattedUserAnswers = dummyReview.questions.map(q => dummyReview.userAnswers[q.id]);
        const formattedCorrectAnswers = dummyReview.questions.map(q => dummyReview.correctAnswers[q.id]);

        setReviewData({
          quizTitle: dummyReview.quizTitle,
          questions: dummyReview.questions,
          userAnswers: formattedUserAnswers,
          correctAnswers: formattedCorrectAnswers,
        });

      } catch (err) {
        setError('Failed to load review details. Please try again.');
        console.error('Error fetching review:', err);
      } finally {
        setLoading(false);
      }
    };

    if (quizId && resultId) {
      fetchReviewDetails();
    } else {
      setError('Invalid review URL.');
      setLoading(false);
    }
  }, [quizId, resultId, isAuthenticated, authLoading, navigate]);

  if (loading) {
    return (
      <div className="results-page-container loading-state">
        <LoadingSpinner />
        <p>Loading quiz review...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/results')} variant="primary">
          Back to Results
        </Button>
      </div>
    );
  }

  if (!reviewData) {
    return (
      <div className="results-page-container empty-state">
        <p>No review data available.</p>
        <Button onClick={() => navigate('/results')} variant="primary">
          Back to Results
        </Button>
      </div>
    );
  }

  return (
    <div className="results-page-container">
      <AnswerReview
        quizTitle={reviewData.quizTitle}
        questions={reviewData.questions}
        userAnswers={reviewData.userAnswers}
        correctAnswers={reviewData.correctAnswers}
      />
      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <Button onClick={() => navigate('/results')} variant="secondary">
          Back to My Results
        </Button>
      </div>
    </div>
  );
};

export default AnswerReviewPage;