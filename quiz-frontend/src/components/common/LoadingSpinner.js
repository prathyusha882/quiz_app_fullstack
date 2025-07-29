// src/components/common/LoadingSpinner.js
import React from 'react';
import './LoadingSpinner.css';

/**
 * A simple, visual loading spinner component.
 * @param {object} props - The component props.
 * @param {string} [props.className] - Additional CSS class names for customization.
 */
const LoadingSpinner = ({ className = '' }) => {
  return (
    <div className={`spinner-container ${className}`}>
      <div className="loading-spinner"></div>
    </div>
  );
};

export default LoadingSpinner;