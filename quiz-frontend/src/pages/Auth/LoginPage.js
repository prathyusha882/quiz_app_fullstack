// quiz-frontend/src/pages/Auth/LoginPage.js
import React, { useEffect } from 'react'; // <-- Import useEffect
import { useNavigate } from 'react-router-dom';
import LoginForm from '../../components/auth/LoginForm';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { backgroundImage } from '../../assets';

const LoginPage = () => {
  console.log('LoginPage: Component rendered');
  const navigate = useNavigate();
  const { isAuthenticated, authLoading } = useAuth();

  // ✅ FIX: Redirect logic inside useEffect
  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      navigate('/'); // Redirect to dashboard if already authenticated
    }
  }, [isAuthenticated, authLoading, navigate]); // Add navigate to dependencies

  if (authLoading) {
    return (
      <div className="auth-page-container">
        <LoadingSpinner />
        <p>Loading authentication state...</p>
      </div>
    );
  }

  const handleLoginSuccess = () => {
    navigate('/'); // This navigate is triggered by a user action (form submit), so it's fine
  };

  return (
    <div
      className="auth-page-container"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <LoginForm
        onLoginSuccess={handleLoginSuccess}
        onSwitchToRegister={() => navigate('/register')}
      />
    </div>
  );
};

export default LoginPage;