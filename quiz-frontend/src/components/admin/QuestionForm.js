// src/components/admin/QuestionForm.js
import React, { useState, useEffect } from 'react';
import InputField from '../common/InputField';
import Button from '../common/Button';
import './QuestionForm.css';

/**
 * Form for creating or editing a question for a specific quiz.
 * @param {object} props - The component props.
 * @param {object} [props.question] - Question object to pre-fill the form (for editing).
 * @param {function} props.onSubmit - Callback function when the form is submitted.
 * @param {boolean} [props.isLoading=false] - Indicates if the form is in a loading state.
 * @param {string} [props.error] - Error message to display.
 */
const QuestionForm = ({ question, onSubmit, isLoading = false, error }) => {
  const [formData, setFormData] = useState({
    text: '',
    type: 'multiple-choice', // Default type
    options: [''], // For multiple-choice/checkbox
    correctAnswers: [], // For multiple-choice/checkbox
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    if (question) {
      setFormData({
        text: question.text || '',
        type: question.type || 'multiple-choice',
        options: question.options && question.options.length > 0 ? question.options : [''],
        correctAnswers: Array.isArray(question.correctAnswers) ? question.correctAnswers : [],
      });
    }
  }, [question]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleOptionChange = (index, value) => {
    const newOptions = [...formData.options];
    newOptions[index] = value;
    setFormData((prev) => ({ ...prev, options: newOptions }));
  };

  const addOption = () => {
    setFormData((prev) => ({ ...prev, options: [...prev.options, ''] }));
  };

  const removeOption = (index) => {
    const newOptions = formData.options.filter((_, i) => i !== index);
    setFormData((prev) => ({ ...prev, options: newOptions }));
    // Also remove from correctAnswers if it was correct
    setFormData((prev) => ({
        ...prev,
        correctAnswers: prev.correctAnswers.filter(ans => ans !== prev.options[index])
    }));
  };

  const handleCorrectAnswerChange = (e) => {
    const { value, checked } = e.target;
    if (formData.type === 'multiple-choice') {
      setFormData((prev) => ({ ...prev, correctAnswers: checked ? [value] : [] }));
    } else if (formData.type === 'checkbox') {
      setFormData((prev) => ({
        ...prev,
        correctAnswers: checked
          ? [...prev.correctAnswers, value]
          : prev.correctAnswers.filter((ans) => ans !== value),
      }));
    } else { // text-input
        setFormData((prev) => ({ ...prev, correctAnswers: [value] }));
    }
  };

  const validate = () => {
    let errors = {};
    if (!formData.text.trim()) errors.text = 'Question text is required.';
    if (formData.type === 'multiple-choice' || formData.type === 'checkbox') {
      if (formData.options.some(opt => !opt.trim())) {
        errors.options = 'All options must be filled.';
      }
      if (formData.options.length < 2) {
          errors.options = 'At least two options are required.';
      }
      if (formData.correctAnswers.length === 0) {
        errors.correctAnswers = 'At least one correct answer must be selected.';
      }
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="question-form-container">
      <h3>{question ? 'Edit Question' : 'Add New Question'}</h3>
      <form onSubmit={handleSubmit} className="question-form">
        {error && <p className="form-error-message">{error}</p>}
        <InputField
          label="Question Text"
          type="text"
          name="text"
          value={formData.text}
          onChange={handleChange}
          placeholder="e.g., What is the capital of France?"
          required
          error={formErrors.text}
        />
        <div className="form-group">
          <label htmlFor="type">Question Type</label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="select-field"
          >
            <option value="multiple-choice">Multiple Choice</option>
            <option value="checkbox">Checkboxes (Multiple Answers)</option>
            <option value="text-input">Text Input (Short Answer)</option>
          </select>
        </div>

        {(formData.type === 'multiple-choice' || formData.type === 'checkbox') && (
          <div className="options-section">
            <h4>Options <span className="required-asterisk">*</span></h4>
            {formData.options.map((option, index) => (
              <div key={index} className="option-input-group">
                <InputField
                  label={`Option ${index + 1}`}
                  type="text"
                  name={`option-${index}`}
                  value={option}
                  onChange={(e) => handleOptionChange(index, e.target.value)}
                  placeholder={`Option ${index + 1} text`}
                  required
                />
                <label className="correct-answer-checkbox">
                  <input
                    type={formData.type === 'multiple-choice' ? 'radio' : 'checkbox'}
                    name="correctAnswer"
                    value={option}
                    checked={formData.correctAnswers.includes(option)}
                    onChange={handleCorrectAnswerChange}
                    disabled={!option.trim()} // Disable if option is empty
                  />
                  Correct
                </label>
                {formData.options.length > 1 && (
                  <Button type="button" onClick={() => removeOption(index)} variant="danger" className="remove-option-btn">
                    Remove
                  </Button>
                )}
              </div>
            ))}
            {formErrors.options && <p className="input-error">{formErrors.options}</p>}
            {formErrors.correctAnswers && <p className="input-error">{formErrors.correctAnswers}</p>}
            <Button type="button" onClick={addOption} variant="secondary">
              Add Option
            </Button>
          </div>
        )}

        {formData.type === 'text-input' && (
          <InputField
            label="Correct Answer (for Text Input)"
            type="text"
            name="correctAnswers"
            value={formData.correctAnswers[0] || ''}
            onChange={(e) => handleCorrectAnswerChange(e)}
            placeholder="e.g., Paris"
            required
            error={formErrors.correctAnswers}
          />
        )}

        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'Saving...' : (question ? 'Update Question' : 'Add Question')}
        </Button>
      </form>
    </div>
  );
};

export default QuestionForm;