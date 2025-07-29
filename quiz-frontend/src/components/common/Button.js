// src/components/common/Button.js
import React from 'react';
import './Button.css';

/**
 * Reusable Button component.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The content inside the button.
 * @param {string} [props.type='button'] - The type of the button (e.g., 'submit', 'button').
 * @param {function} [props.onClick] - The click handler for the button.
 * @param {string} [props.className] - Additional CSS class names.
 * @param {boolean} [props.disabled=false] - Whether the button is disabled.
 * @param {string} [props.variant='primary'] - Visual style variant ('primary', 'secondary', 'danger', 'outline').
 */
const Button = ({ children, type = 'button', onClick, className = '', disabled = false, variant = 'primary' }) => {
  const buttonClass = `button ${variant} ${className}`.trim();

  return (
    <button
      type={type}
      onClick={onClick}
      className={buttonClass}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;