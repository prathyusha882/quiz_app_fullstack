// src/components/quizzes/OptionSelection.js
import React from 'react';
import './OptionSelection.css';

/**
 * Renders a list of options for selection (radio or checkbox).
 * @param {object} props - The component props.
 * @param {Array<string>} props.options - Array of option strings.
 * @param {string | string[]} props.selectedOption - The currently selected option(s).
 * @param {function} props.onSelect - Callback when an option is selected.
 * @param {'radio' | 'checkbox'} [props.optionType='radio'] - Type of selection control.
 */
const OptionSelection = ({ options, selectedOption, onSelect, optionType = 'radio' }) => {
  const isSelected = (option) => {
    if (optionType === 'radio') {
      return selectedOption === option;
    } else { // checkbox
      return Array.isArray(selectedOption) && selectedOption.includes(option);
    }
  };

  const handleChange = (e) => {
    const value = e.target.value;
    if (optionType === 'radio') {
      onSelect(value);
    } else { // checkbox
      let newSelection;
      if (isSelected(value)) {
        newSelection = selectedOption.filter(item => item !== value);
      } else {
        newSelection = [...selectedOption, value];
      }
      onSelect(newSelection);
    }
  };

  return (
    <div className="option-selection">
      {options.map((option, index) => (
        <label key={index} className="option-item">
          <input
            type={optionType}
            name="quizOption" // Use a common name for radio buttons
            value={option}
            checked={isSelected(option)}
            onChange={handleChange}
          />
          <span className="option-text">{option}</span>
        </label>
      ))}
    </div>
  );
};

export default OptionSelection;