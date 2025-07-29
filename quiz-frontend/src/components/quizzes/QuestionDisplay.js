// src/components/quizzes/QuestionDisplay.js
import React from 'react';
import OptionSelection from './OptionSelection'; // Assuming OptionSelection is in the same folder
import './QuestionDisplay.css';

/**
 * Displays a single quiz question and handles user answer selection.
 * @param {object} props - The component props.
 * @param {object} props.question - The question object.
 * @param {number} props.question.id - Question ID.
 * @param {string} props.question.text - The question text.
 * @param {string} props.question.type - Type of question (e.g., 'multiple-choice').
 * @param {Array<string | object>} props.question.options - Array of options for selection.
 * @param {any} props.selectedAnswer - The currently selected answer for this question.
 * @param {function} props.onAnswerSelect - Callback function when an answer is selected.
 * @param {number} [props.questionNumber] - The current question number for display.
 */
const QuestionDisplay = ({ question, selectedAnswer, onAnswerSelect, questionNumber }) => {
  const renderOptions = () => {
    switch (question.type) {
      case 'multiple-choice':
        return (
          <OptionSelection
            options={question.options}
            selectedOption={selectedAnswer}
            onSelect={onAnswerSelect}
            optionType="radio"
          />
        );
      case 'checkbox': // For multiple correct answers
        return (
          <OptionSelection
            options={question.options}
            selectedOption={selectedAnswer || []} // Ensure array for checkboxes
            onSelect={onAnswerSelect}
            optionType="checkbox"
          />
        );
      case 'text-input': // For short answer
        return (
          <input
            type="text"
            className="text-answer-input"
            value={selectedAnswer || ''}
            onChange={(e) => onAnswerSelect(e.target.value)}
            placeholder="Type your answer here..."
          />
        );
      default:
        return <p>Unsupported question type: {question.type}</p>;
    }
  };

  return (
    <div className="question-display">
      <div className="question-header">
        {questionNumber && <span className="question-number">Question {questionNumber}</span>}
        <h3 className="question-text">{question.text}</h3>
      </div>
      <div className="question-options">
        {renderOptions()}
      </div>
    </div>
  );
};

export default QuestionDisplay;