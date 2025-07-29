// src/components/results/QuizResultSummary.js
import React from 'react';
import Button from '../common/Button';
import './QuizResultSummary.css';

/**
 * Displays a summary of a completed quiz result.
 * @param {object} props - The component props.
 * @param {object} props.result - The quiz result object.
 * @param {string} props.result.quizTitle - Title of the quiz.
 * @param {number} props.result.score - User's score.
 * @param {number} props.result.totalQuestions - Total number of questions.
 * @param {string} [props.result.timeTaken] - Time taken to complete the quiz (e.g., "10:30").
 * @param {Date} [props.result.dateCompleted] - Date the quiz was completed.
 * @param {function} [props.onReviewAnswers] - Callback to review detailed answers.
 * @param {function} [props.onTakeAnotherQuiz] - Callback to go back to quiz list.
 */
const QuizResultSummary = ({ result, onReviewAnswers, onTakeAnotherQuiz }) => {
  const percentage = ((result.score / result.totalQuestions) * 100).toFixed(0);
  const passed = percentage >= 70; // Example pass threshold

  const completionDate = result.dateCompleted
    ? new Date(result.dateCompleted).toLocaleDateString(undefined, {
        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
      })
    : 'N/A';

  return (
    <div className="quiz-result-summary">
      <h2 className="summary-title">Quiz Completed!</h2>
      <p className="summary-quiz-title">Quiz: {result.quizTitle}</p>

      <div className="summary-metrics">
        <div className="metric-item">
          <span className="metric-label">Your Score:</span>
          <span className="metric-value">{result.score} / {result.totalQuestions}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Percentage:</span>
          <span className={`metric-value ${passed ? 'pass' : 'fail'}`}>{percentage}%</span>
        </div>
        {result.timeTaken && (
          <div className="metric-item">
            <span className="metric-label">Time Taken:</span>
            <span className="metric-value">{result.timeTaken}</span>
          </div>
        )}
        {result.dateCompleted && (
          <div className="metric-item">
            <span className="metric-label">Completed On:</span>
            <span className="metric-value">{completionDate}</span>
          </div>
        )}
      </div>

      <p className={`summary-status ${passed ? 'status-pass' : 'status-fail'}`}>
        {passed ? 'Congratulations! You passed!' : 'Keep learning! You can do better next time.'}
      </p>

      <div className="summary-actions">
        {onReviewAnswers && (
          <Button onClick={onReviewAnswers} variant="secondary">
            Review Answers
          </Button>
        )}
        {onTakeAnotherQuiz && (
          <Button onClick={onTakeAnotherQuiz} variant="primary">
            Take Another Quiz
          </Button>
        )}
      </div>
    </div>
  );
};

export default QuizResultSummary;