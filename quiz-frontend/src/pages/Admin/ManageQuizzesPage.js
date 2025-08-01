// src/pages/Admin/ManageQuizzesPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import QuizForm from '../../components/admin/QuizForm';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Modal from '../../components/common/Modal';
import quizService from '../../services/quizService'; // Make sure this file exists
import './AdminPages.css';

let adminDummyQuizzes = [
  { id: 'q1', title: 'React Basics', description: 'Test your knowledge on React fundamentals.', difficulty: 'Medium', duration: 600, questionCount: 3 },
  { id: 'q2', title: 'JavaScript Advanced', description: 'Challenging questions on JS concepts.', difficulty: 'Hard', duration: 900, questionCount: 2 },
  { id: 'q3', title: 'HTML & CSS Fundamentals', description: 'Basic questions on structuring web pages and styling with CSS.', difficulty: 'Easy', duration: 480, questionCount: 5 },
];

const ManageQuizzesPage = () => {
  const { user, authLoading } = useAuth();
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingQuiz, setEditingQuiz] = useState(null);

  // 🧠 AI Question Modal States
  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);
  const [generateTopic, setGenerateTopic] = useState('');
  const [generateDifficulty, setGenerateDifficulty] = useState('Medium');
  const [generateNumQuestions, setGenerateNumQuestions] = useState(5);
  const [selectedQuizId, setSelectedQuizId] = useState(null);

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
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulated delay
        setQuizzes(adminDummyQuizzes);
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
    setEditingQuiz(null);
    setIsModalOpen(true);
  };

  const handleEditQuiz = (quizId) => {
    const quizToEdit = quizzes.find(q => q.id === quizId);
    setEditingQuiz(quizToEdit);
    setIsModalOpen(true);
  };

  const handleDeleteQuiz = async (quizId) => {
    if (window.confirm('Are you sure you want to delete this quiz?')) {
      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 500));
        adminDummyQuizzes = adminDummyQuizzes.filter(q => q.id !== quizId);
        setQuizzes(adminDummyQuizzes);
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
    setLoading(true);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      if (editingQuiz) {
        adminDummyQuizzes = adminDummyQuizzes.map(q =>
          q.id === editingQuiz.id ? { ...q, ...formData } : q
        );
        alert('Quiz updated successfully!');
      } else {
        const newId = `q${adminDummyQuizzes.length + 1}`;
        const newQuiz = { ...formData, id: newId, questionCount: 0 };
        adminDummyQuizzes.push(newQuiz);
        alert('Quiz added successfully!');
      }
      setQuizzes(adminDummyQuizzes);
      setIsModalOpen(false);
      setEditingQuiz(null);
    } catch (err) {
      setError('Failed to save quiz.');
      console.error('Save quiz error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 🧠 Handle AI Question Generation
  const handleGenerate = (quizId, title) => {
    setSelectedQuizId(quizId);
    setGenerateTopic(title);
    setIsGenerateModalOpen(true);
  };

  const confirmGenerate = async () => {
    try {
      const data = {
        quiz_id: selectedQuizId,
        topic: generateTopic,
        difficulty: generateDifficulty,
        num_questions: generateNumQuestions,
      };
      const res = await quizService.generateAIQuestions(data); // ⛳️ Your backend should accept this
      alert(res.message || "AI questions generated successfully!");
      setIsGenerateModalOpen(false);
    } catch (err) {
      console.error(err);
      alert("Failed to generate questions");
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
                  <Button onClick={() => handleEditQuiz(quiz.id)} variant="secondary" className="action-btn">Edit</Button>
                  <Button onClick={() => navigate(`/admin/questions/${quiz.id}`)} variant="outline" className="action-btn">Questions</Button>
                  <Button onClick={() => handleDeleteQuiz(quiz.id)} variant="danger" className="action-btn">Delete</Button>
                  <Button onClick={() => handleGenerate(quiz.id, quiz.title)} variant="highlight" className="action-btn">Generate AI Qs</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* 🧾 Quiz Form Modal */}
      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); setEditingQuiz(null); }} title={editingQuiz ? 'Edit Quiz' : 'Add New Quiz'}>
        <QuizForm
          quiz={editingQuiz}
          onSubmit={handleFormSubmit}
          isLoading={loading}
          error={error}
        />
      </Modal>

      {/* 🧠 AI Generation Modal */}
      {isGenerateModalOpen && (
        <Modal onClose={() => setIsGenerateModalOpen(false)} title="Generate AI Questions">
          <label>Topic</label>
          <input value={generateTopic} onChange={(e) => setGenerateTopic(e.target.value)} className="modal-input" />
          
          <label>Difficulty</label>
          <select value={generateDifficulty} onChange={(e) => setGenerateDifficulty(e.target.value)} className="modal-input">
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>

          <label>Number of Questions</label>
          <input type="number" value={generateNumQuestions} onChange={(e) => setGenerateNumQuestions(Number(e.target.value))} className="modal-input" min="1" />

          <Button onClick={confirmGenerate} variant="primary">Generate</Button>
        </Modal>
      )}
    </div>
  );
};

export default ManageQuizzesPage;
