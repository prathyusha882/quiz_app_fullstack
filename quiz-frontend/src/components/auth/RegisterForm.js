// src/components/auth/RegisterForm.js
import React, { useState } from 'react';
import InputField from '../common/InputField';
import Button from '../common/Button';
import { useAuth } from '../../contexts/AuthContext'; // Assuming AuthContext exists
import './RegisterForm.css';

/**
 * RegisterForm component for new user registration.
 * Handles username, email, password, and confirm password input.
 * @param {object} props - The component props.
 * @param {function} [props.onRegisterSuccess] - Callback after successful registration.
 * @param {function} [props.onSwitchToLogin] - Callback to switch to login form.
 */
const RegisterForm = ({ onRegisterSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const { register } = useAuth(); // Assuming useAuth provides a register function

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    // Clear error for the current field as user types
    if (errors[name]) {
      setErrors((prevErrors) => ({ ...prevErrors, [name]: '' }));
    }
  };

  const validateForm = () => {
    let newErrors = {};
    if (!formData.username) newErrors.username = 'Username is required.';
    if (!formData.email) {
      newErrors.email = 'Email is required.';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email address is invalid.';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required.';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters.';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      // In a real app, you'd call an API.
      // Assuming register function takes username, email, password
      const success = await register(formData.username, formData.email, formData.password);
      if (success) {
        onRegisterSuccess && onRegisterSuccess();
      } else {
        // This might be a generic error from backend, or specific like 'username taken'
        setErrors({ form: 'Registration failed. Please try again.' });
      }
    } catch (err) {
      setErrors({ form: err.message || 'An unexpected error occurred.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-form-container">
      <h2>Create New Account</h2>
      <form onSubmit={handleSubmit} className="register-form">
        {errors.form && <p className="auth-error-message">{errors.form}</p>}
        <InputField
          label="Username"
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Choose a username"
          required
          error={errors.username}
        />
        <InputField
          label="Email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Enter your email"
          required
          error={errors.email}
        />
        <InputField
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Create a password"
          required
          error={errors.password}
        />
        <InputField
          label="Confirm Password"
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          placeholder="Re-enter your password"
          required
          error={errors.confirmPassword}
        />
        <Button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </Button>
      </form>
      {onSwitchToLogin && (
        <p className="switch-auth-mode">
          Already have an account? <span onClick={onSwitchToLogin}>Login here.</span>
        </p>
      )}
    </div>
  );
};

export default RegisterForm;