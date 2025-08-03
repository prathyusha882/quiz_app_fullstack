// src/App.js 
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { QuizProvider } from './contexts/QuizContext';
import PrivateRoute from './components/common/PrivateRoute'; // Assuming this file now exists and is correct

// Layout Components
import Header from './components/common/Header';
import Footer from './components/common/Footer';

// Pages (ensure all these imports are actually used in your <Routes>)
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import UserDashboard from './pages/Dashboard/UserDashboard';
import AdminDashboard from './pages/Dashboard/AdminDashboard';
import QuizListPage from './pages/Quizzes/QuizListPage';
import QuizDetailPage from './pages/Quizzes/QuizDetailPage';
import TakeQuizPage from './pages/Quizzes/TakeQuizPage';
import UserResultsPage from './pages/Results/UserResultsPage';
import AdminResultsPage from './pages/Results/AdminResultsPage';
import ManageQuizzesPage from './pages/Admin/ManageQuizzesPage';
import ManageQuestionsPage from './pages/Admin/ManageQuestionsPage';
import ManageUsersPage from './pages/Admin/ManageUsersPage';
import NotFoundPage from './pages/NotFoundPage';
import AnswerReviewPage from './pages/Results/AnswerReviewPage'; 

function App() { // <--- This is your component definition
  console.log('App: Component rendered');
  console.log('App: Current location:', window.location.pathname);
  return (
    <Router>
      <AuthProvider>
        <QuizProvider>
          <div className="app-container">
            <Header />
            <main className="app-main-content pt-16">
              <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/quizzes" element={<QuizListPage />} /> {/* Make QuizList public for Browse */}
                <Route path="/quizzes/:quizId" element={<QuizDetailPage />} /> {/* Make QuizDetail public for viewing info */}


                {/* User Protected Routes */}
                <Route path="/" element={<PrivateRoute allowedRoles={['user', 'admin']} />}>
                  <Route index element={<UserDashboard />} /> {/* Default route for authenticated users */}
                  <Route path="quizzes/take/:quizId" element={<TakeQuizPage />} /> {/* Taking quiz requires login */}
                  <Route path="results" element={<UserResultsPage />} />
                  {/* You'll need a specific route for review, which might be another PrivateRoute */}
                  <Route path="results/review/:quizId/:resultId" element={<AnswerReviewPage />} />
                </Route>


                {/* Admin Protected Routes */}
                <Route path="/admin" element={<PrivateRoute allowedRoles={['admin']} />}>
                  <Route index element={<AdminDashboard />} /> {/* Default route for admins */}
                  <Route path="quizzes" element={<ManageQuizzesPage />} />
                  <Route path="questions/:quizId" element={<ManageQuestionsPage />} />
                  <Route path="users" element={<ManageUsersPage />} />
                  <Route path="results" element={<AdminResultsPage />} />
                </Route>


                {/* Fallback Route for 404 */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </QuizProvider>
      </AuthProvider>
    </Router>
  );
}

export default App; // <--- THIS LINE IS ABSOLUTELY ESSENTIAL