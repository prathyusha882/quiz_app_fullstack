// src/pages/Quizzes/QuizDetailPage.js
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import './QuizPages.css';

// Dummy data for quiz details and question count (replace with API calls)
const dummyQuizDetails = {
    'q1': { id: 'q1', title: 'React Basics', description: 'Test your knowledge on React fundamentals, JSX, components, and state management. This quiz covers basic to intermediate concepts.', difficulty: 'Medium', duration: 600, questionCount: 3 },
    'q2': { id: 'q2', title: 'JavaScript Advanced', description: 'Dive deep into advanced JavaScript topics including closures, prototypes, asynchronous programming with Promises and Async/Await, and ES6+ features.', difficulty: 'Hard', duration: 900, questionCount: 2 },
    'q3': { id: 'q3', title: 'HTML & CSS Fundamentals', description: 'A foundational quiz covering HTML structure, common tags, CSS selectors, box model, flexbox, and basic responsiveness.', difficulty: 'Easy', duration: 480, questionCount: 5 },
    'q4': { id: 'q4', title: 'Node.js Essentials', description: 'Explore core Node.js concepts, modules, event loop, streams, and express.js basics for building server-side applications.', difficulty: 'Medium', duration: 720, questionCount: 4 },
    'q5': { id: 'q5', title: 'Database Basics (SQL)', description: 'Understand relational database concepts, SQL queries (SELECT, INSERT, UPDATE, DELETE), joins, and basic table design principles.', difficulty: 'Medium', duration: 840, questionCount: 6 },
};

/**
 * Quiz Detail Page. Displays information about a specific quiz before the user starts it.
 */
const QuizDetailPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuizDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 700)); // Simulate API delay
        const data = dummyQuizDetails[quizId];
        if (data) {
          setQuiz(data);
        } else {
          setError('Quiz not found.');
        }
      } catch (err) {
        setError('Failed to load quiz details. Please try again.');
        console.error('Error fetching quiz details:', err);
      } finally {
        setLoading(false);
      }
    };

    if (quizId) {
      fetchQuizDetails();
    } else {
      setError('No quiz ID provided.');
      setLoading(false);
    }
  }, [quizId]);

  const handleStartQuiz = () => {
    if (quiz) {
      navigate(`/quizzes/take/${quiz.id}`);
    }
  };

  if (loading) {
    return (
      <div className="quiz-detail-page-container loading-state">
        <LoadingSpinner />
        <p>Loading quiz details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quiz-detail-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/quizzes')} variant="primary">
          Back to Quizzes
        </Button>
      </div>
    );
  }

  if (!quiz) {
    return (
        <div className="quiz-detail-page-container loading-state">
            <p>Quiz data not available.</p>
        </div>
    );
  }

  const formatDuration = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes} min ${secs > 0 ? `${secs} sec` : ''}`;
  };

  return (
    <div className="quiz-detail-page-container">
      <div className="quiz-detail-card">
        <h1 className="detail-title">{quiz.title}</h1>
        <p className="detail-description">{quiz.description}</p>
        <div className="detail-meta">
          <p><strong>Difficulty:</strong> <span className={`difficulty-${quiz.difficulty.toLowerCase()}`}>{quiz.difficulty}</span></p>
          <p><strong>Total Questions:</strong> {quiz.questionCount}</p>
          <p><strong>Estimated Time:</strong> {formatDuration(quiz.duration)}</p>
        </div>
        <div className="detail-actions">
          <Button onClick={handleStartQuiz} variant="primary">
            Start Quiz
          </Button>
          <Button onClick={() => navigate('/quizzes')} variant="secondary">
            Back to All Quizzes
          </Button>
        </div>
      </div>
    </div>
  );
};

export default QuizDetailPage;