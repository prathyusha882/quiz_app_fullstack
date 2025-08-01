// src/components/auth/LoginForm.js
import React, { useState } from 'react';
import InputField from '../common/InputField';
import Button from '../common/Button';
import { useAuth } from '../../contexts/AuthContext'; // Assuming AuthContext exists
import './LoginForm.css';

/**
 * LoginForm component for user authentication.
 * Handles username and password input, and submission.
 * @param {object} props - The component props.
 * @param {function} [props.onLoginSuccess] - Callback after successful login.
 * @param {function} [props.onSwitchToRegister] - Callback to switch to registration form.
 */
const LoginForm = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, authError } = useAuth(); // Get authError from context

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('LoginForm: Form submitted with username:', username);
    setError('');
    setLoading(true);

    try {
      console.log('LoginForm: Calling login function...');
      const success = await login(username, password);
      console.log('LoginForm: Login result:', success);
      if (success) {
        console.log('LoginForm: Login successful, calling onLoginSuccess');
        onLoginSuccess && onLoginSuccess();
      } else {
        console.log('LoginForm: Login failed, showing error');
        // Show error from context if available
        setError(authError || 'Invalid username or password.');
      }
    } catch (err) {
      console.error('LoginForm: Login error:', err);
      setError(err.message || authError || 'An error occurred during login.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form-container">
      <h2>Login to Your Account</h2>
      <form onSubmit={handleSubmit} className="login-form">
        {error && <p className="auth-error-message">{error}</p>}
        <InputField
          label="Username"
          type="text"
          name="username"
          value={username}
          onChange={(e) => {
            console.log('LoginForm: Username changed to:', e.target.value);
            setUsername(e.target.value);
          }}
          placeholder="Enter your username"
          required
        />
        <InputField
          label="Password"
          type="password"
          name="password"
          value={password}
          onChange={(e) => {
            console.log('LoginForm: Password changed');
            setPassword(e.target.value);
          }}
          placeholder="Enter your password"
          required
        />
        <Button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </Button>
      </form>
      {onSwitchToRegister && (
        <p className="switch-auth-mode">
          Don't have an account? <span onClick={onSwitchToRegister}>Register here.</span>
        </p>
      )}
    </div>
  );
};

export default LoginForm;