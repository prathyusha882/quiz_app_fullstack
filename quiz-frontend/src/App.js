import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { QuizProvider } from './contexts/QuizContext';
import './App.css';

// Layout Components
import Layout from './components/Layout';
import LoadingSpinner from './components/common/LoadingSpinner';

// Auth Pages
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';

// Dashboard Pages
import UserDashboard from './pages/Dashboard/UserDashboard';
import AdminDashboard from './pages/Dashboard/AdminDashboard';

// Quiz Pages
import QuizListPage from './pages/Quizzes/QuizListPage';
import QuizDetailPage from './pages/Quizzes/QuizDetailPage';
import QuizTakingPage from './pages/Quizzes/QuizTakingPage';

// Course Pages
import CourseListPage from './pages/Courses/CourseListPage';
import CourseDetailPage from './pages/Courses/CourseDetailPage';

// Admin Pages
import ManageQuestionsPage from './pages/Admin/ManageQuestionsPage';
import ManageQuizzesPage from './pages/Admin/ManageQuizzesPage';
import AdminResultsPage from './pages/Results/AdminResultsPage';

// Results Pages
import AnswerReviewPage from './pages/Results/AnswerReviewPage';

// Protected Route Component
const ProtectedRoute = ({ children, requireAdmin = false }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requireAdmin && user.role !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <QuizProvider>
        <Router>
          <div className="App">
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              
              {/* Protected Routes */}
              <Route path="/" element={
                <ProtectedRoute>
                  <Layout>
                    <UserDashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Layout>
                    <UserDashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/admin" element={
                <ProtectedRoute requireAdmin>
                  <Layout>
                    <AdminDashboard />
                  </Layout>
                </ProtectedRoute>
              } />
              
              {/* Quiz Routes */}
              <Route path="/quizzes" element={
                <ProtectedRoute>
                  <Layout>
                    <QuizListPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/quizzes/:id" element={
                <ProtectedRoute>
                  <Layout>
                    <QuizDetailPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/quizzes/:id/take" element={
                <ProtectedRoute>
                  <QuizTakingPage />
                </ProtectedRoute>
              } />
              
              {/* Course Routes */}
              <Route path="/courses" element={
                <ProtectedRoute>
                  <Layout>
                    <CourseListPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/courses/:slug" element={
                <ProtectedRoute>
                  <Layout>
                    <CourseDetailPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              {/* Admin Routes */}
              <Route path="/admin/questions" element={
                <ProtectedRoute requireAdmin>
                  <Layout>
                    <ManageQuestionsPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/admin/quizzes" element={
                <ProtectedRoute requireAdmin>
                  <Layout>
                    <ManageQuizzesPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              <Route path="/admin/results" element={
                <ProtectedRoute requireAdmin>
                  <Layout>
                    <AdminResultsPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              {/* Results Routes */}
              <Route path="/results/:attemptId" element={
                <ProtectedRoute>
                  <Layout>
                    <AnswerReviewPage />
                  </Layout>
                </ProtectedRoute>
              } />
              
              {/* Default redirect */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </Router>
      </QuizProvider>
    </AuthProvider>
  );
}

export default App;