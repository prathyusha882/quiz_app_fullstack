// quiz-frontend/src/pages/Auth/RegisterPage.js
import React, { useEffect } from 'react'; // <-- Import useEffect
import { useNavigate } from 'react-router-dom';
import RegisterForm from '../../components/auth/RegisterForm';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { backgroundImage } from '../../assets'; // Corrected import

const RegisterPage = () => {
  console.log('RegisterPage: Component rendered');
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

  const handleRegisterSuccess = () => {
    alert('Registration successful! You are now logged in.');
    navigate('/'); // This navigate is triggered by a user action, so it's fine
  };

  return (
    <div
      className="auth-page-container"
      style={{ backgroundImage: `url(${backgroundImage})` }}
    >
      <RegisterForm
        onRegisterSuccess={handleRegisterSuccess}
        onSwitchToLogin={() => navigate('/login')}
      />
    </div>
  );
};

export default RegisterPage;