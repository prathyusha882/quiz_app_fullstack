// quiz-frontend/src/components/common/PrivateRoute.js
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import LoadingSpinner from './LoadingSpinner'; // Assuming you have LoadingSpinner

/**
 * A private route component that checks user authentication and roles.
 * Renders child routes if authenticated and authorized, otherwise redirects.
 * @param {object} props - The component props.
 * @param {Array<string>} [props.allowedRoles] - An array of roles that are allowed to access this route.
 * If empty or null, only checks if isAuthenticated.
 * @param {React.ReactNode} [props.children] - Child components to render if authorized (for older Route v5 syntax).
 * With Route v6, typically used with Outlet.
 */
const PrivateRoute = ({ allowedRoles }) => {
  const { isAuthenticated, user, authLoading } = useAuth(); // Get auth state and user from hook

  // Show a loading spinner while authentication state is being determined
  if (authLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
        <LoadingSpinner />
        <p style={{ marginLeft: '10px' }}>Loading authentication...</p>
      </div>
    );
  }

  // If not authenticated, redirect to login page
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If roles are specified, check if the user's role is allowed
  if (allowedRoles && allowedRoles.length > 0) {
    if (!user || !user.role || !allowedRoles.includes(user.role)) {
      // If user doesn't have an allowed role, redirect to unauthorized page or dashboard
      // For now, redirect to dashboard, you could create a /403-unauthorized page
      return <Navigate to="/" replace />;
    }
  }

  // If authenticated and authorized, render the child route content
  // Outlet is used for nested routes in React Router v6
  return <Outlet />;
};

export default PrivateRoute;