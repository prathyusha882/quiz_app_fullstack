import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AnswerReview from '../../components/results/AnswerReview';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Button from '../../components/common/Button';
import { useAuth } from '../../contexts/AuthContext';
import quizService from '../../services/quizService';

import './ResultPages.css';

const AnswerReviewPage = () => {
  const { quizId, resultId: attemptId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, authLoading } = useAuth();
  const [reviewData, setReviewData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReviewDetails = async () => {
      if (authLoading) return;

      if (!isAuthenticated) {
        navigate('/login', { replace: true });
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const data = await quizService.getQuizReviewDetails(quizId, attemptId);

        const formattedUserAnswers = data.questions_for_review.map(
          q => q.user_chosen_option_text || q.user_chosen_text_answer || []
        );
        const formattedCorrectAnswers = data.questions_for_review.map(
          q => q.correct_answers || []
        );

        setReviewData({
          quizTitle: data.quiz_title,
          questions: data.questions_for_review,
          userAnswers: formattedUserAnswers,
          correctAnswers: formattedCorrectAnswers,
        });
      } catch (err) {
        setError('Failed to load review.');
      } finally {
        setLoading(false);
      }
    };

    if (quizId && attemptId && !isNaN(Number(attemptId))) {
      fetchReviewDetails();
    } else {
      setError('Invalid review URL.');
      setLoading(false);
    }
  }, [quizId, attemptId, isAuthenticated, authLoading, navigate]);

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
