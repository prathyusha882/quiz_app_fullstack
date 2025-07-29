// src/components/admin/QuizForm.js
import React, { useState, useEffect } from 'react';
import InputField from '../common/InputField';
import Button from '../common/Button';
import './QuizForm.css';

/**
 * Form for creating or editing a quiz.
 * @param {object} props - The component props.
 * @param {object} [props.quiz] - Quiz object to pre-fill the form (for editing).
 * @param {function} props.onSubmit - Callback function when the form is submitted.
 * @param {boolean} [props.isLoading=false] - Indicates if the form is in a loading state.
 * @param {string} [props.error] - Error message to display.
 */
const QuizForm = ({ quiz, onSubmit, isLoading = false, error }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    difficulty: 'Easy',
    duration: 600, // Default 10 minutes
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    if (quiz) {
      setFormData({
        title: quiz.title || '',
        description: quiz.description || '',
        difficulty: quiz.difficulty || 'Easy',
        duration: quiz.duration || 600,
      });
    }
  }, [quiz]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    let errors = {};
    if (!formData.title.trim()) errors.title = 'Quiz title is required.';
    if (!formData.description.trim()) errors.description = 'Description is required.';
    if (formData.duration <= 0) errors.duration = 'Duration must be positive.';
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
    <div className="quiz-form-container">
      <h3>{quiz ? 'Edit Quiz' : 'Create New Quiz'}</h3>
      <form onSubmit={handleSubmit} className="quiz-form">
        {error && <p className="form-error-message">{error}</p>}
        <InputField
          label="Quiz Title"
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="e.g., React Basics"
          required
          error={formErrors.title}
        />
        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="A brief overview of the quiz content."
            rows="4"
            required
            className={formErrors.description ? 'has-error' : ''}
          ></textarea>
          {formErrors.description && <p className="input-error">{formErrors.description}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="difficulty">Difficulty</label>
          <select
            id="difficulty"
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
            className="select-field"
          >
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        <InputField
          label="Duration (seconds)"
          type="number"
          name="duration"
          value={formData.duration}
          onChange={handleChange}
          placeholder="e.g., 600 for 10 minutes"
          required
          error={formErrors.duration}
          min="1"
        />
        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'Saving...' : (quiz ? 'Update Quiz' : 'Create Quiz')}
        </Button>
      </form>
    </div>
  );
};

export default QuizForm;