// src/components/common/ThemeToggle.js
import React, { useState, useEffect } from 'react';
import './ThemeToggle.css';

/**
 * Theme toggle component for switching between light and dark modes
 * @param {object} props - Component props
 * @param {string} props.theme - Current theme ('light' or 'dark')
 * @param {function} props.onThemeChange - Callback when theme changes
 */
const ThemeToggle = ({ theme = 'light', onThemeChange }) => {
  const [isChecked, setIsChecked] = useState(theme === 'dark');

  useEffect(() => {
    setIsChecked(theme === 'dark');
  }, [theme]);

  const handleToggle = () => {
    const newTheme = isChecked ? 'light' : 'dark';
    setIsChecked(!isChecked);
    onThemeChange && onThemeChange(newTheme);
    
    // Update CSS variables for theme
    document.documentElement.setAttribute('data-theme', newTheme);
    
    // Save to localStorage
    localStorage.setItem('quiz-theme', newTheme);
  };

  return (
    <div className="theme-toggle-container">
      <label className="theme-toggle">
        <input
          type="checkbox"
          checked={isChecked}
          onChange={handleToggle}
          className="theme-toggle-input"
        />
        <span className="theme-toggle-slider">
          <span className="theme-toggle-icon light">☀️</span>
          <span className="theme-toggle-icon dark">🌙</span>
        </span>
      </label>
    </div>
  );
};

export default ThemeToggle; 