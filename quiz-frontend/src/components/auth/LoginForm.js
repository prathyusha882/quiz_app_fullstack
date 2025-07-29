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
  const { login } = useAuth(); // Assuming useAuth provides a login function

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const success = await login(username, password);
      if (success) {
        onLoginSuccess && onLoginSuccess();
      } else {
        setError('Invalid username or password.');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during login.');
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
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
          required
        />
        <InputField
          label="Password"
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
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