// src/pages/Admin/ManageQuizzesPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import QuizForm from '../../components/admin/QuizForm';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Modal from '../../components/common/Modal';
import './AdminPages.css'; // Common styling for admin pages

// Dummy data (same as QuizListPage's, for consistency)
let adminDummyQuizzes = [
  { id: 'q1', title: 'React Basics', description: 'Test your knowledge on React fundamentals.', difficulty: 'Medium', duration: 600, questionCount: 3 },
  { id: 'q2', title: 'JavaScript Advanced', description: 'Challenging questions on JS concepts.', difficulty: 'Hard', duration: 900, questionCount: 2 },
  { id: 'q3', title: 'HTML & CSS Fundamentals', description: 'Basic questions on structuring web pages and styling with CSS.', difficulty: 'Easy', duration: 480, questionCount: 5 },
];

/**
 * Admin page for managing quizzes (create, edit, delete).
 */
const ManageQuizzesPage = () => {
  const { user, authLoading } = useAuth();
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingQuiz, setEditingQuiz] = useState(null); // Quiz object being edited

  useEffect(() => {
    const fetchQuizzes = async () => {
      if (authLoading) {
        setLoading(false);
        return;
      }
      if (!user || user.role !== 'admin') {
        setError('Access Denied: You must be an administrator to view this page.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay
        setQuizzes(adminDummyQuizzes); // Use the mutable dummy data
      } catch (err) {
        setError('Failed to load quizzes. Please try again.');
        console.error('Error fetching quizzes:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuizzes();
  }, [user, authLoading]);

  const handleAddQuiz = () => {
    setEditingQuiz(null); // Clear any existing quiz data
    setIsModalOpen(true);
  };

  const handleEditQuiz = (quizId) => {
    const quizToEdit = quizzes.find(q => q.id === quizId);
    setEditingQuiz(quizToEdit);
    setIsModalOpen(true);
  };

  const handleDeleteQuiz = async (quizId) => {
    if (window.confirm('Are you sure you want to delete this quiz?')) {
      // Simulate API delete
      setLoading(true); // Can use a more granular loading state if preferred
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 500));
        adminDummyQuizzes = adminDummyQuizzes.filter(q => q.id !== quizId);
        setQuizzes(adminDummyQuizzes); // Update state with filtered list
        alert('Quiz deleted successfully!');
      } catch (err) {
        setError('Failed to delete quiz.');
        console.error('Delete quiz error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleFormSubmit = async (formData) => {
    // Simulate API save
    setLoading(true); // Can use a more granular loading state if preferred
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      if (editingQuiz) {
        // Update existing quiz
        adminDummyQuizzes = adminDummyQuizzes.map(q =>
          q.id === editingQuiz.id ? { ...q, ...formData } : q
        );
        alert('Quiz updated successfully!');
      } else {
        // Add new quiz
        const newId = `q${adminDummyQuizzes.length + 1}`; // Simple ID generation
        const newQuiz = { ...formData, id: newId, questionCount: 0 }; // Assume 0 questions initially
        adminDummyQuizzes.push(newQuiz);
        alert('Quiz added successfully!');
      }
      setQuizzes(adminDummyQuizzes); // Update state
      setIsModalOpen(false); // Close modal
      setEditingQuiz(null); // Reset editing state
    } catch (err) {
      setError('Failed to save quiz.');
      console.error('Save quiz error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="admin-page-container loading-state">
        <LoadingSpinner />
        <p>Loading quizzes...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-page-container error-state">
        <p className="error-message">{error}</p>
        <Button onClick={() => navigate('/admin')} variant="primary">
          Back to Admin Dashboard
        </Button>
      </div>
    );
  }

  if (!user || user.role !== 'admin') {
    return (
      <div className="admin-page-container error-state">
        <p className="error-message">Access Denied: You must be an administrator to view this page.</p>
        <Button onClick={() => navigate('/')} variant="primary">
          Go to Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div className="admin-page-container">
      <h1 className="admin-page-title">Manage Quizzes</h1>

      <div className="admin-actions-header">
        <Button onClick={handleAddQuiz} variant="primary">
          Add New Quiz
        </Button>
      </div>

      {quizzes.length === 0 ? (
        <p className="admin-info-message">No quizzes to display. Add one!</p>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Difficulty</th>
              <th>Duration (s)</th>
              <th>Questions</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {quizzes.map((quiz) => (
              <tr key={quiz.id}>
                <td>{quiz.id}</td>
                <td>{quiz.title}</td>
                <td>{quiz.difficulty}</td>
                <td>{quiz.duration}</td>
                <td>{quiz.questionCount}</td>
                <td className="table-actions">
                  <Button onClick={() => handleEditQuiz(quiz.id)} variant="secondary" className="action-btn">
                    Edit
                  </Button>
                  <Button onClick={() => navigate(`/admin/questions/${quiz.id}`)} variant="outline" className="action-btn">
                    Questions
                  </Button>
                  <Button onClick={() => handleDeleteQuiz(quiz.id)} variant="danger" className="action-btn">
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); setEditingQuiz(null); }} title={editingQuiz ? 'Edit Quiz' : 'Add New Quiz'}>
        <QuizForm
          quiz={editingQuiz}
          onSubmit={handleFormSubmit}
          isLoading={loading} // Use form-specific loading if multiple forms
          error={error} // Pass error from page state
        />
      </Modal>
    </div>
  );
};

export default ManageQuizzesPage;