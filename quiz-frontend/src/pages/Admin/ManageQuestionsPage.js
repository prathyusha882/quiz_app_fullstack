// src/pages/Admin/ManageQuestionsPage.js

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { getQuizById } from '../../services/quizService';
import QuestionForm from '../../components/admin/QuestionForm';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Modal from '../../components/common/Modal';
import './AdminPages.css';

// ✅ Dummy data for questions (matches QuizContext's dummy data structure)
let adminDummyQuestions = {
  'q1': [
    {
      id: 'q1-1',
      text: 'What is JSX?',
      type: 'multiple-choice',
      options: ['A markup syntax', 'A JavaScript library', 'A CSS preprocessor', 'A database'],
      correctAnswers: ['A markup syntax'],
    },
    {
      id: 'q1-2',
      text: 'Which hooks manage side effects in functional components?',
      type: 'checkbox',
      options: ['useState', 'useEffect', 'useContext', 'useRef'],
      correctAnswers: ['useEffect'],
    },
    {
      id: 'q1-3',
      text: 'What is the purpose of "props" in React?',
      type: 'text-input',
      correctAnswers: ['to pass data to components', 'to pass data from parent to child components'],
    },
  ],
  'q2': [
    {
      id: 'q2-1',
      text: 'Explain event delegation in JavaScript.',
      type: 'text-input',
      correctAnswers: ['attach event listener to parent element instead of each child'],
    },
    {
      id: 'q2-2',
      text: 'Which of these are ES6 features?',
      type: 'checkbox',
      options: ['let/const', 'arrow functions', 'classes', 'jQuery'],
      correctAnswers: ['let/const', 'arrow functions', 'classes'],
    },
  ],
};

const ManageQuestionsPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const { user, authLoading } = useAuth();
  const [questions, setQuestions] = useState([]);
  const [quizTitle, setQuizTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      if (authLoading) {
        setLoading(false);
        return;
      }
      if (!user || user.role !== 'admin') {
        setError('Access Denied: You must be an administrator to view this page.');
        setLoading(false);
        return;
      }
      if (!quizId) {
        setError('No quiz ID provided.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay
        const quiz = await getQuizById(quizId); // ✅ Fixed
        if (quiz) {
          setQuizTitle(quiz.title);
        } else {
          setQuizTitle('Unknown Quiz');
        }
        setQuestions(quiz?.questions || []);
      } catch (err) {
        setError('Failed to load questions. Please try again.');
        console.error('Error fetching questions:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, [quizId, user, authLoading]);

  const handleAddQuestion = () => {
    setEditingQuestion(null);
    setIsModalOpen(true);
  };

  const handleEditQuestion = (questionId) => {
    const questionToEdit = questions.find(q => q.id === questionId);
    setEditingQuestion(questionToEdit);
    setIsModalOpen(true);
  };

  const handleDeleteQuestion = async (questionId) => {
    if (window.confirm('Are you sure you want to delete this question?')) {
      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 500));
        // This part of the logic needs to be updated to interact with the actual API
        // For now, we'll just remove it from the dummy data and update the state
        // In a real application, you'd call an API to delete the question
        // adminDummyQuestions[quizId] = (adminDummyQuestions[quizId] || []).filter(q => q.id !== questionId);
        // setQuestions(adminDummyQuestions[quizId]);
        alert('Question deletion is not yet implemented via API.');
      } catch (err) {
        setError('Failed to delete question.');
        console.error('Delete question error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      if (editingQuestion) {
        // This part of the logic needs to be updated to interact with the actual API
        // For now, we'll just update the dummy data
        // adminDummyQuestions[quizId] = (adminDummyQuestions[quizId] || []).map(q =>
        //   q.id === editingQuestion.id ? { ...q, ...formData } : q
        // );
        alert('Question update is not yet implemented via API.');
      } else {
        // This part of the logic needs to be updated to interact with the actual API
        // For now, we'll just add to the dummy data
        // const newId = `${quizId}-${(adminDummyQuestions[quizId] || []).length + 1}`;
        // const newQuestion = { ...formData, id: newId };
        // if (!adminDummyQuestions[quizId]) {
        //   adminDummyQuestions[quizId] = [];
        // }
        // adminDummyQuestions[quizId].push(newQuestion);
        alert('Question addition is not yet implemented via API.');
      }
      // setQuestions(adminDummyQuestions[quizId]); // ✅ CORRECTED LINE: Ensure this line has the full argument and semicolon.
      setIsModalOpen(false);
      setEditingQuestion(null);
    } catch (err) {
      setError('Failed to save question.');
      console.error('Save question error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-page-container">
      <h3>{editingQuestion ? 'Edit Question' : 'Add New Question'}</h3>

      <div className="admin-actions-header">
        <Button onClick={handleAddQuestion} variant="primary">
          Add New Question
        </Button>
        <Button onClick={() => navigate('/admin/quizzes')} variant="secondary">
          Back to Quizzes
        </Button>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : questions.length === 0 ? (
        <p className="admin-info-message">No questions for this quiz. Add one!</p>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Question Text</th>
              <th>Type</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {questions.map((question) => (
              <tr key={question.id}>
                <td>{question.id}</td>
                <td>{question.text.substring(0, 70)}{question.text.length > 70 ? '...' : ''}</td>
                <td>{question.type}</td>
                <td className="table-actions">
                  <Button onClick={() => handleEditQuestion(question.id)} variant="secondary" className="action-btn">
                    Edit
                  </Button>
                  <Button onClick={() => handleDeleteQuestion(question.id)} variant="danger" className="action-btn">
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); setEditingQuestion(null); }} title={editingQuestion ? 'Edit Question' : 'Add New Question'}>
        <QuestionForm
          question={editingQuestion}
          onSubmit={handleFormSubmit}
          isLoading={loading}
          error={error}
        />
      </Modal>
    </div>
  );
};

export default ManageQuestionsPage;