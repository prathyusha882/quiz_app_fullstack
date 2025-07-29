// src/components/common/InputField.js
import React from 'react';
import './InputField.css';

/**
 * Reusable InputField component.
 * @param {object} props - The component props.
 * @param {string} props.label - The label for the input field.
 * @param {string} props.type - The HTML input type (e.g., 'text', 'password', 'email').
 * @param {string} props.name - The name attribute for the input.
 * @param {string} props.value - The current value of the input.
 * @param {function} props.onChange - The change handler for the input.
 * @param {string} [props.placeholder=''] - The placeholder text.
 * @param {boolean} [props.required=false] - Whether the input is required.
 * @param {string} [props.error] - Error message to display below the input.
 * @param {string} [props.className] - Additional CSS class names for the container.
 */
const InputField = ({
  label,
  type,
  name,
  value,
  onChange,
  placeholder = '',
  required = false,
  error,
  className = ''
}) => {
  const inputGroupClass = `input-field-group ${className} ${error ? 'has-error' : ''}`.trim();

  return (
    <div className={inputGroupClass}>
      <label htmlFor={name}>{label}{required && <span className="required-asterisk">*</span>}</label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="input-field"
      />
      {error && <p className="input-error">{error}</p>}
    </div>
  );
};

export default InputField;