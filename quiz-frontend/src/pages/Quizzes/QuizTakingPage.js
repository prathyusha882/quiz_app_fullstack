import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';
import './QuizTakingPage.css';

const QuizTakingPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await api.get(`/api/quizzes/${quizId}/`);
        setQuiz(response.data);
        setTimeLeft(response.data.time_limit * 60); // Convert to seconds
        setLoading(false);
      } catch (error) {
        console.error('Error fetching quiz:', error);
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [quizId]);

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [timeLeft]);

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmit = async () => {
    if (submitting) return;
    
    setSubmitting(true);
    try {
      const response = await api.post(`/api/quizzes/${quizId}/submit/`, {
        answers: answers,
        time_taken: quiz.time_limit * 60 - timeLeft
      });
      
      navigate(`/results/${response.data.attempt_id}`);
    } catch (error) {
      console.error('Error submitting quiz:', error);
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="quiz-taking-loading">
        <div className="loading-spinner"></div>
        <p>Loading quiz...</p>
      </div>
    );
  }

  if (!quiz) {
    return <div className="quiz-taking-error">Quiz not found</div>;
  }

  const currentQuestion = quiz.questions[currentQuestionIndex];

  return (
    <div className="quiz-taking-page">
      <div className="quiz-header">
        <h1>{quiz.title}</h1>
        <div className="quiz-info">
          <span>Question {currentQuestionIndex + 1} of {quiz.questions.length}</span>
          <span className="timer">Time: {formatTime(timeLeft)}</span>
        </div>
      </div>

      <div className="question-container">
        <div className="question">
          <h2>{currentQuestion.text}</h2>
          
          {currentQuestion.question_type === 'multiple_choice' && (
            <div className="options">
              {currentQuestion.options.map((option, index) => (
                <label key={index} className="option">
                  <input
                    type="radio"
                    name={`question_${currentQuestion.id}`}
                    value={option}
                    checked={answers[currentQuestion.id] === option}
                    onChange={() => handleAnswerChange(currentQuestion.id, option)}
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.question_type === 'text' && (
            <textarea
              value={answers[currentQuestion.id] || ''}
              onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
              placeholder="Enter your answer..."
              rows={4}
            />
          )}

          {currentQuestion.question_type === 'true_false' && (
            <div className="options">
              <label className="option">
                <input
                  type="radio"
                  name={`question_${currentQuestion.id}`}
                  value="true"
                  checked={answers[currentQuestion.id] === 'true'}
                  onChange={() => handleAnswerChange(currentQuestion.id, 'true')}
                />
                <span>True</span>
              </label>
              <label className="option">
                <input
                  type="radio"
                  name={`question_${currentQuestion.id}`}
                  value="false"
                  checked={answers[currentQuestion.id] === 'false'}
                  onChange={() => handleAnswerChange(currentQuestion.id, 'false')}
                />
                <span>False</span>
              </label>
            </div>
          )}
        </div>

        <div className="navigation">
          <button
            onClick={() => setCurrentQuestionIndex(prev => Math.max(0, prev - 1))}
            disabled={currentQuestionIndex === 0}
            className="nav-button"
          >
            Previous
          </button>
          
          {currentQuestionIndex < quiz.questions.length - 1 ? (
            <button
              onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
              className="nav-button"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="submit-button"
            >
              {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizTakingPage; 