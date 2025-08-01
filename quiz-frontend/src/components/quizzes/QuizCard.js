// src/components/quizzes/QuizCard.js
import React from 'react';
import Button from '../common/Button';
import './QuizCard.css';

/**
 * Displays a single quiz with its details and action buttons.
 * @param {object} props - The component props.
 * @param {object} props.quiz - The quiz object.
 * @param {number} props.quiz.id - The ID of the quiz.
 * @param {string} props.quiz.title - The title of the quiz.
 * @param {string} props.quiz.description - A brief description of the quiz.
 * @param {string} props.quiz.difficulty - The difficulty level (e.g., 'Easy', 'Medium', 'Hard').
 * @param {number} [props.quiz.questionCount] - Number of questions in the quiz.
 * @param {function} [props.onStartQuiz] - Callback when 'Start Quiz' button is clicked.
 * @param {function} [props.onViewDetails] - Callback when 'View Details' button is clicked.
 */
const QuizCard = ({ quiz, onStartQuiz, onViewDetails }) => {
  // Safety check for quiz object
  if (!quiz || typeof quiz !== 'object') {
    return (
      <div className="quiz-card">
        <h3 className="quiz-card-title">Invalid Quiz</h3>
        <p className="quiz-card-description">Quiz data is not available.</p>
      </div>
    );
  }

  const title = quiz.title || 'Untitled Quiz';
  const description = quiz.description || 'No description available.';
  const difficulty = quiz.difficulty || 'Medium';
  const questionCount = quiz.questionCount || quiz.question_count || 0;

  return (
    <div className="quiz-card">
      <h3 className="quiz-card-title">{title}</h3>
      <p className="quiz-card-description">{description}</p>
      <div className="quiz-card-meta">
        <span>Difficulty: <span className={`difficulty-${difficulty.toLowerCase()}`}>{difficulty}</span></span>
        {questionCount > 0 && <span>Questions: {questionCount}</span>}
      </div>
      <div className="quiz-card-actions">
        {onStartQuiz && (
          <Button onClick={() => onStartQuiz(quiz.id)} variant="primary">
            Start Quiz
          </Button>
        )}
        {onViewDetails && (
          <Button onClick={() => onViewDetails(quiz.id)} variant="secondary">
            View Details
          </Button>
        )}
      </div>
    </div>
  );
};

export default QuizCard;