// src/pages/Quizzes/QuizListPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import QuizCard from '../../components/quizzes/QuizCard';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import InputField from '../../components/common/InputField';
import './QuizPages.css'; // Common styling for quiz pages

// Dummy data for quizzes (replace with API calls)
export const dummyQuizList = [ // <-- ADD export keyword here
  { id: 'q1', title: 'React Basics', description: 'Test your knowledge on React fundamentals, JSX, components, and state.', difficulty: 'Medium', questionCount: 3 },
  { id: 'q2', title: 'JavaScript Advanced', description: 'Challenging questions on closures, prototypes, async/await, and ES6+ features.', difficulty: 'Hard', questionCount: 2 },
  { id: 'q3', title: 'HTML & CSS Fundamentals', description: 'Basic questions on structuring web pages and styling with CSS.', difficulty: 'Easy', questionCount: 5 },
  { id: 'q4', title: 'Node.js Essentials', description: 'Explore core Node.js concepts, modules, and asynchronous programming.', difficulty: 'Medium', questionCount: 4 },
  { id: 'q5', title: 'Database Basics (SQL)', description: 'Understand SQL queries, table design, and database concepts.', difficulty: 'Medium', questionCount: 6 },
];
/**
 * Quiz List Page. Displays all available quizzes with filtering options.
 */
const QuizListPage = () => {
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('All'); // 'All', 'Easy', 'Medium', 'Hard'

  useEffect(() => {
    // Simulate fetching quizzes from an API
    const fetchQuizzes = async () => {
      setLoading(true);
      setError(null);
      try {
        await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay
        setQuizzes(dummyQuizList);
      } catch (err) {
        setError('Failed to load quizzes. Please try again.');
        console.error('Error fetching quizzes:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuizzes();
  }, []);

  const filteredQuizzes = quizzes.filter(quiz => {
    const matchesSearch = quiz.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          quiz.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDifficulty = filterDifficulty === 'All' || quiz.difficulty === filterDifficulty;
    return matchesSearch && matchesDifficulty;
  });

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
        <p className="no-quizzes-message">No quizzes match your criteria.</p>
      ) : (
        <div className="quiz-list-grid">
          {filteredQuizzes.map((quiz) => (
            <QuizCard
              key={quiz.id}
              quiz={quiz}
              onStartQuiz={handleStartQuiz}
              onViewDetails={handleViewDetails}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default QuizListPage;