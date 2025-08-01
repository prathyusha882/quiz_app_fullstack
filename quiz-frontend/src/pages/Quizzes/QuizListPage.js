import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import QuizCard from '../../components/quizzes/QuizCard';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import InputField from '../../components/common/InputField';
import { getAllQuizzes } from '../../services/quizService';
import { useAuth } from '../../contexts/AuthContext';
import './QuizPages.css'; // Common styling for quiz pages

/**
 * Quiz List Page. Displays all available quizzes with filtering options.
 */
const QuizListPage = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('All');

  useEffect(() => {
    const fetchQuizzes = async () => {
      setLoading(true);
      setError(null);
      
      // Check authentication
      console.log('User authenticated:', isAuthenticated);
      console.log('User:', user);
      console.log('Access token:', localStorage.getItem('access_token'));
      
      try {
        const quizData = await getAllQuizzes();
        console.log('Quiz data received:', quizData);
        // Ensure quizData is an array
        const quizArray = Array.isArray(quizData) ? quizData : 
                         (quizData && quizData.results ? quizData.results : []);
        console.log('Quiz array after processing:', quizArray);
        setQuizzes(quizArray);
      } catch (err) {
        console.error('Error fetching quizzes:', err);
        // Set a fallback quiz for testing
        setQuizzes([{
          id: 9,
          title: "General Knowledge Quiz",
          description: "Test your knowledge across various subjects including programming, databases, and web technologies.",
          difficulty: "Medium",
          question_count: 31
        }]);
        setError('Using fallback data. Please check your connection.');
      } finally {
        setLoading(false);
      }
    };
    fetchQuizzes();
  }, [isAuthenticated, user]);

  const filteredQuizzes = Array.isArray(quizzes) ? quizzes.filter(quiz => {
    // Safety check for quiz object
    if (!quiz || typeof quiz !== 'object') {
      return false;
    }
    
    const title = quiz.title || '';
    const description = quiz.description || '';
    const difficulty = quiz.difficulty || '';
    
    const matchesSearch = title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDifficulty = filterDifficulty === 'All' || difficulty === filterDifficulty;
    return matchesSearch && matchesDifficulty;
  }) : [];

  const handleStartQuiz = (quizId) => {
    navigate(`/quizzes/take/${quizId}`);
  };

  const handleViewDetails = (quizId) => {
    navigate(`/quizzes/${quizId}`);
  };

  if (loading) {
    return (
      <div className="quiz-page-container">
        <LoadingSpinner />
        <p>Loading quizzes...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quiz-page-container">
        <p className="error-message">{error}</p>
      </div>
    );
  }

  return (
    <div className="quiz-page-container">
      <h1 className="quiz-page-title">Available Quizzes</h1>

      <div className="quiz-filters">
        <InputField
          label="Search Quizzes"
          type="text"
          name="searchTerm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by title or description..."
          className="filter-search-input"
        />
        <div className="form-group filter-select-group">
          <label htmlFor="difficultyFilter">Filter by Difficulty:</label>
          <select
            id="difficultyFilter"
            value={filterDifficulty}
            onChange={(e) => setFilterDifficulty(e.target.value)}
            className="select-field"
          >
            <option value="All">All</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {filteredQuizzes.length === 0 ? (
        <div className="no-quizzes-message">
          <p>No quizzes found matching your criteria.</p>
        </div>
      ) : (
        <div className="quiz-grid">
          {filteredQuizzes.map((quiz) => (
            <QuizCard
              key={quiz.id}
              quiz={quiz}
              onStartQuiz={() => handleStartQuiz(quiz.id)}
              onViewDetails={() => handleViewDetails(quiz.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default QuizListPage;
