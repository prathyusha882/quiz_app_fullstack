// src/components/quizzes/QuestionDisplay.js
import React from 'react';
import OptionSelection from './OptionSelection'; // Assuming OptionSelection is in the same folder
import CodeEditor from './CodeEditor';
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
      case 'essay': // For long answer
        return (
          <textarea
            className="essay-answer-input"
            value={selectedAnswer || ''}
            onChange={(e) => onAnswerSelect(e.target.value)}
            placeholder="Type your detailed answer here..."
            rows={6}
          />
        );
      case 'true-false': // True/False questions
        return (
          <OptionSelection
            options={[
              { id: 'true', text: 'True' },
              { id: 'false', text: 'False' }
            ]}
            selectedOption={selectedAnswer}
            onSelect={onAnswerSelect}
            optionType="radio"
          />
        );
      case 'fill-blank': // Fill in the blank
        return (
          <input
            type="text"
            className="fill-blank-input"
            value={selectedAnswer || ''}
            onChange={(e) => onAnswerSelect(e.target.value)}
            placeholder="Fill in the blank..."
          />
        );
      case 'match-following': // Match the following
        return (
          <div className="match-following-container">
            {question.matchPairs && question.matchPairs.map((pair, index) => (
              <div key={index} className="match-pair">
                <span className="match-left">{pair.left}</span>
                <select
                  className="match-select"
                  value={selectedAnswer?.[index] || ''}
                  onChange={(e) => {
                    const newAnswer = [...(selectedAnswer || [])];
                    newAnswer[index] = e.target.value;
                    onAnswerSelect(newAnswer);
                  }}
                >
                  <option value="">Select...</option>
                  {pair.rightOptions && pair.rightOptions.map((option, optIndex) => (
                    <option key={optIndex} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        );
      case 'code': // Code questions
        return (
          <CodeEditor
            language={question.codeLanguage || 'javascript'}
            defaultCode={question.codeTemplate || ''}
            value={selectedAnswer || ''}
            onCodeChange={onAnswerSelect}
            readOnly={false}
          />
        );
      case 'audio': // Audio questions
        return (
          <div className="audio-question">
            {question.audio && (
              <audio controls className="audio-player">
                <source src={question.audio} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            )}
            <OptionSelection
              options={question.options}
              selectedOption={selectedAnswer}
              onSelect={onAnswerSelect}
              optionType="radio"
            />
          </div>
        );
      case 'video': // Video questions
        return (
          <div className="video-question">
            {question.video && (
              <video controls className="video-player">
                <source src={question.video} type="video/mp4" />
                Your browser does not support the video element.
              </video>
            )}
            {question.videoUrl && (
              <iframe
                src={question.videoUrl}
                className="video-iframe"
                frameBorder="0"
                allowFullScreen
              />
            )}
            <OptionSelection
              options={question.options}
              selectedOption={selectedAnswer}
              onSelect={onAnswerSelect}
              optionType="radio"
            />
          </div>
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