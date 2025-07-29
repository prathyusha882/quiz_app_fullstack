// src/components/results/AnswerReview.js
import React from 'react';
import { checkIcon, crossIcon } from '../../assets'; // Import icons from assets
import './AnswerReview.css';

/**
 * Displays a detailed review of quiz answers, showing questions, user's answer, and correct answer.
 * @param {object} props - The component props.
 * @param {Array<object>} props.questions - Array of original question objects.
 * @param {Array<any>} props.userAnswers - Array of user's answers, corresponding to questions.
 * @param {Array<any>} props.correctAnswers - Array of correct answers, corresponding to questions.
 * @param {string} [props.quizTitle] - Optional title of the quiz for context.
 */
const AnswerReview = ({ questions, userAnswers, correctAnswers, quizTitle }) => {

  if (!questions || questions.length === 0) {
    return <p className="review-info-message">No questions to review.</p>;
  }

  const getAnswerStatus = (questionIndex, userAnswer, correctAnswer) => {
    // Normalize answers for comparison
    const normalize = (answer) => {
      if (Array.isArray(answer)) {
        return answer.map(a => String(a).toLowerCase()).sort().join(',');
      }
      return String(answer).toLowerCase();
    };

    const userNorm = normalize(userAnswer);
    const correctNorm = normalize(correctAnswer);

    if (userNorm === correctNorm) {
      return 'correct';
    } else if (userAnswer === null || userAnswer === undefined || userAnswer.length === 0) {
      return 'skipped';
    }
    return 'incorrect';
  };

  const renderCorrectAnswer = (question, correctAnswer) => {
    if (Array.isArray(correctAnswer)) {
      return `Correct Answer(s): ${correctAnswer.join(', ')}`;
    }
    return `Correct Answer: ${correctAnswer}`;
  };

  const renderUserAnswer = (question, userAnswer) => {
    if (userAnswer === null || userAnswer === undefined || (Array.isArray(userAnswer) && userAnswer.length === 0)) {
        return <span className="skipped-answer">Skipped</span>;
    }
    if (Array.isArray(userAnswer)) {
      return `Your Answer(s): ${userAnswer.join(', ')}`;
    }
    return `Your Answer: ${userAnswer}`;
  };

  return (
    <div className="answer-review-container">
      {quizTitle && <h2 className="review-title">Review Answers for "{quizTitle}"</h2>}
      {!quizTitle && <h2 className="review-title">Answer Review</h2>}

      {questions.map((question, index) => {
        const userAnswer = userAnswers[index];
        const correctAnswer = correctAnswers[index];
        const status = getAnswerStatus(index, userAnswer, correctAnswer);

        return (
          <div key={question.id || index} className={`review-item ${status}`}>
            <div className="review-header">
              <span className="question-number">Question {index + 1}</span>
              <p className="review-question-text">{question.text}</p>
            </div>
            <div className="review-details">
              <p className="user-answer-display">
                {renderUserAnswer(question, userAnswer)}
                <img
                  src={status === 'correct' ? checkIcon : crossIcon}
                  alt={status}
                  className="answer-status-icon"
                />
              </p>
              {status !== 'correct' && (
                <p className="correct-answer-display">
                  {renderCorrectAnswer(question, correctAnswer)}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AnswerReview;