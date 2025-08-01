import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getQuizById, getQuestionsByQuizId, submitQuizAnswers } from '../../services/quizService';
import Button from '../../components/common/Button';
import './QuizPages.css';

const TakeQuizPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchQuizData();
  }, [quizId]);

  const fetchQuizData = async () => {
    try {
      setLoading(true);
      const [quizData, questionsData] = await Promise.all([
        getQuizById(quizId),
        getQuestionsByQuizId(quizId)
      ]);

      console.log('Quiz data:', quizData);
      console.log('Questions data:', questionsData);

      setQuiz(quizData);
      
      // Extract questions from the paginated response
      const questionsArray = questionsData.results || questionsData;
      console.log('Questions array:', questionsArray);
      console.log('Number of questions in array:', questionsArray.length);
      
      setQuestions(questionsArray);
      setLoading(false);
    } catch (error) {
      console.error('Error loading quiz:', error);
      setError('Failed to load quiz');
      setLoading(false);
    }
  };

  const handleStartQuiz = () => {
    setQuizStarted(true);
  };

  const handleAnswerSelect = (questionId, selectedOption) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: selectedOption
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    try {
      // Convert answers to the format expected by the backend
      const answersArray = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: questionId,
        submitted_answer: answer
      }));

      console.log('Submitting answers:', answersArray);

      // Submit the quiz answers
      const result = await submitQuizAnswers(quizId, answersArray, '00:00');
      
      console.log('Quiz submitted successfully:', result);
      
      // Navigate to results page with the attempt ID
      if (result && result.id) {
        navigate(`/results/${quizId}/${result.id}`);
      } else {
        navigate('/results');
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
      alert('Failed to submit quiz. Please try again.');
    }
  };

  if (loading) {
    return <div className="loading">Loading quiz...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!quiz) {
    return <div className="error">Quiz not found</div>;
  }

  // Show quiz overview before starting
  if (!quizStarted) {
    return (
      <div className="quiz-page-container">
        <h1 className="quiz-page-title">{quiz.title}</h1>
        <p className="quiz-description">{quiz.description}</p>
        <p className="quiz-duration">Duration: {quiz.duration} minutes</p>
        <p className="quiz-questions-count">Number of Questions: {questions.length}</p>
        
        <div className="quiz-start-section">
          <Button onClick={handleStartQuiz} variant="primary" size="large">
            Start Quiz
          </Button>
        </div>
      </div>
    );
  }

  // Show quiz questions
  const currentQuestion = questions[currentQuestionIndex];
  
  return (
    <div className="quiz-page-container">
      <div className="quiz-header">
        <h1 className="quiz-page-title">{quiz.title}</h1>
        <p className="question-counter">
          Question {currentQuestionIndex + 1} of {questions.length}
        </p>
      </div>

      {currentQuestion && (
        <div className="question-container">
          <h2 className="question-text">{currentQuestion.text}</h2>
          
          <div className="options-container">
            {currentQuestion.options && currentQuestion.options.length > 0 ? (
              currentQuestion.options.map((option, index) => {
                return (
                  <div key={index} className="option-item">
                    <input
                      type="radio"
                      id={`option-${currentQuestion.id}-${index}`}
                      name={`question-${currentQuestion.id}`}
                      value={option.text}
                      checked={answers[currentQuestion.id] === option.text}
                      onChange={() => handleAnswerSelect(currentQuestion.id, option.text)}
                    />
                    <label htmlFor={`option-${currentQuestion.id}-${index}`}>
                      {option.text}
                    </label>
                  </div>
                );
              })
            ) : (
              <div className="no-options-message">
                <p>This question has no answer options available.</p>
                <p>Please contact the administrator to add options to this question.</p>
              </div>
            )}
          </div>

          <div className="navigation-buttons">
            <Button 
              onClick={handlePreviousQuestion} 
              disabled={currentQuestionIndex === 0}
              variant="secondary"
            >
              Previous
            </Button>
            
            {currentQuestionIndex === questions.length - 1 ? (
              <Button onClick={handleSubmitQuiz} variant="primary">
                Submit Quiz
              </Button>
            ) : (
              <Button onClick={handleNextQuestion} variant="primary">
                Next
              </Button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TakeQuizPage;
