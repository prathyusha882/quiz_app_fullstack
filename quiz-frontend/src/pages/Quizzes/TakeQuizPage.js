import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './TakeQuizPage.css';

const TakeQuizPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [warningCount, setWarningCount] = useState(0);
  const [showWarning, setShowWarning] = useState(false);
  const [fullscreenAttempts, setFullscreenAttempts] = useState(0);

  // Mock quiz data - replace with API call
  const mockQuiz = {
    id: quizId,
    title: 'Advanced React Patterns',
    description: 'Test your knowledge of React hooks, context, and advanced patterns',
    timeLimit: 1800, // 30 minutes in seconds
    questions: [
      {
        id: 1,
        type: 'multiple_choice',
        text: 'What is the primary purpose of React.memo?',
        options: [
          'To optimize performance by preventing unnecessary re-renders',
          'To create memoized values',
          'To handle side effects',
          'To manage component state'
        ],
        correctAnswer: 0,
        explanation: 'React.memo is a higher-order component that memoizes your component, preventing re-renders when props haven\'t changed.'
      },
      {
        id: 2,
        type: 'checkbox',
        text: 'Which of the following are valid React hooks? (Select all that apply)',
        options: [
          'useState',
          'useEffect',
          'useContext',
          'useReducer',
          'useCustomHook'
        ],
        correctAnswers: [0, 1, 2, 3],
        explanation: 'All of these are valid React hooks. Custom hooks must start with "use" to follow React\'s rules of hooks.'
      },
      {
        id: 3,
        type: 'text',
        text: 'What is the difference between controlled and uncontrolled components in React?',
        correctAnswer: 'Controlled components have their state managed by React, while uncontrolled components manage their own state internally.',
        explanation: 'Controlled components use props and callbacks to manage state, while uncontrolled components use refs to access DOM values directly.'
      },
      {
        id: 4,
        type: 'multiple_choice',
        text: 'When should you use useCallback?',
        options: [
          'Always, for better performance',
          'When passing callbacks to optimized child components',
          'When you want to memoize expensive calculations',
          'When dealing with async operations'
        ],
        correctAnswer: 1,
        explanation: 'useCallback is most useful when passing callbacks to optimized child components that rely on reference equality to prevent unnecessary renders.'
      },
      {
        id: 5,
        type: 'checkbox',
        text: 'Which patterns are commonly used for state management in React? (Select all that apply)',
        options: [
          'Redux',
          'Context API',
          'Zustand',
          'MobX',
          'Local component state'
        ],
        correctAnswers: [0, 1, 2, 3, 4],
        explanation: 'All of these are valid state management patterns in React, each with their own use cases and trade-offs.'
      }
    ]
  };

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setQuiz(mockQuiz);
      setTimeLeft(mockQuiz.timeLimit);
      setLoading(false);
    }, 1000);

    // Anti-cheating: Detect tab switching
    const handleVisibilityChange = () => {
      if (document.hidden && !isSubmitted) {
        setWarningCount(prev => prev + 1);
        setShowWarning(true);
        setTimeout(() => setShowWarning(false), 3000);
      }
    };

    // Anti-cheating: Detect fullscreen exit
    const handleFullscreenChange = () => {
      if (!document.fullscreenElement && !isSubmitted) {
        setFullscreenAttempts(prev => prev + 1);
        setShowWarning(true);
        setTimeout(() => setShowWarning(false), 3000);
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('fullscreenchange', handleFullscreenChange);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, [isSubmitted]);

  useEffect(() => {
    if (timeLeft > 0 && !isSubmitted) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [timeLeft, isSubmitted]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleSubmit = useCallback(async () => {
    if (isSubmitted) return;
    
    setIsSubmitted(true);
    
    // Calculate results
    const results = {
      totalQuestions: quiz.questions.length,
      correctAnswers: 0,
      answers: answers,
      timeTaken: quiz.timeLimit - timeLeft,
      submittedAt: new Date().toISOString()
    };

    // Grade answers
    quiz.questions.forEach(question => {
      const userAnswer = answers[question.id];
      if (question.type === 'multiple_choice') {
        if (userAnswer === question.correctAnswer) {
          results.correctAnswers++;
        }
      } else if (question.type === 'checkbox') {
        if (Array.isArray(userAnswer) && 
            userAnswer.length === question.correctAnswers.length &&
            userAnswer.every(ans => question.correctAnswers.includes(ans))) {
          results.correctAnswers++;
        }
      }
      // Text questions would need manual grading
    });

    results.percentageScore = (results.correctAnswers / results.totalQuestions) * 100;
    results.passed = results.percentageScore >= 70;

    // Simulate API call to submit results
    console.log('Submitting results:', results);
    
    // Navigate to results page
    navigate(`/results/${quizId}`, { state: { results } });
  }, [isSubmitted, quiz, answers, timeLeft, navigate, quizId]);

  const getProgressPercentage = () => {
    return ((currentQuestionIndex + 1) / quiz?.questions.length) * 100;
  };

  const getQuestionTypeIcon = (type) => {
    switch (type) {
      case 'multiple_choice': return '🔘';
      case 'checkbox': return '☑️';
      case 'text': return '📝';
      default: return '❓';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 pt-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-xl p-8 shadow-soft border border-gray-100">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded-lg mb-4 w-1/3"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded mb-8"></div>
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = quiz.questions[currentQuestionIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 pt-20">
      {/* Warning Modal */}
      {showWarning && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md mx-4 shadow-large">
            <div className="text-center">
              <div className="w-16 h-16 bg-danger-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">⚠️</span>
              </div>
              <h3 className="text-lg font-semibold text-secondary-900 mb-2">
                Warning: Tab Switching Detected
              </h3>
              <p className="text-secondary-600 mb-4">
                Please stay on this tab during the quiz. Multiple violations may result in quiz termination.
              </p>
              <p className="text-sm text-danger-600 font-medium">
                Warnings: {warningCount}/3
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quiz Header */}
        <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-display font-bold text-secondary-900">
                {quiz.title}
              </h1>
              <p className="text-secondary-600 mt-1">{quiz.description}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-primary-600">
                {formatTime(timeLeft)}
              </div>
              <div className="text-sm text-secondary-500">
                Time Remaining
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm text-secondary-600 mb-2">
              <span>Progress</span>
              <span>{currentQuestionIndex + 1} of {quiz.questions.length}</span>
            </div>
            <div className="w-full bg-secondary-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${getProgressPercentage()}%` }}
              ></div>
            </div>
          </div>

          {/* Question Navigation */}
          <div className="flex flex-wrap gap-2">
            {quiz.questions.map((question, index) => (
              <button
                key={question.id}
                onClick={() => setCurrentQuestionIndex(index)}
                className={`w-10 h-10 rounded-lg flex items-center justify-center text-sm font-medium transition-all duration-200 ${
                  index === currentQuestionIndex
                    ? 'bg-primary-600 text-white shadow-glow'
                    : answers[question.id]
                    ? 'bg-success-100 text-success-700 border border-success-200'
                    : 'bg-secondary-100 text-secondary-600 hover:bg-secondary-200'
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white rounded-xl p-8 shadow-soft border border-gray-100 mb-6">
          <div className="flex items-center space-x-3 mb-6">
            <span className="text-2xl">{getQuestionTypeIcon(currentQuestion.type)}</span>
            <div>
              <h2 className="text-xl font-semibold text-secondary-900">
                Question {currentQuestionIndex + 1}
              </h2>
              <p className="text-sm text-secondary-500">
                {currentQuestion.type === 'multiple_choice' ? 'Single Choice' :
                 currentQuestion.type === 'checkbox' ? 'Multiple Choice' : 'Text Answer'}
              </p>
            </div>
          </div>

          <div className="mb-8">
            <p className="text-lg text-secondary-900 leading-relaxed">
              {currentQuestion.text}
            </p>
          </div>

          {/* Answer Options */}
          <div className="space-y-4">
            {currentQuestion.type === 'multiple_choice' && (
              currentQuestion.options.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-soft ${
                    answers[currentQuestion.id] === index
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-primary-300'
                  }`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion.id}`}
                    value={index}
                    checked={answers[currentQuestion.id] === index}
                    onChange={(e) => handleAnswerChange(currentQuestion.id, parseInt(e.target.value))}
                    className="sr-only"
                  />
                  <div className={`w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center ${
                    answers[currentQuestion.id] === index
                      ? 'border-primary-500 bg-primary-500'
                      : 'border-gray-300'
                  }`}>
                    {answers[currentQuestion.id] === index && (
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    )}
                  </div>
                  <span className="text-secondary-900">{option}</span>
                </label>
              ))
            )}

            {currentQuestion.type === 'checkbox' && (
              currentQuestion.options.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-soft ${
                    answers[currentQuestion.id]?.includes(index)
                      ? 'border-success-500 bg-success-50'
                      : 'border-gray-200 hover:border-success-300'
                  }`}
                >
                  <input
                    type="checkbox"
                    value={index}
                    checked={answers[currentQuestion.id]?.includes(index) || false}
                    onChange={(e) => {
                      const currentAnswers = answers[currentQuestion.id] || [];
                      const newAnswers = e.target.checked
                        ? [...currentAnswers, index]
                        : currentAnswers.filter(ans => ans !== index);
                      handleAnswerChange(currentQuestion.id, newAnswers);
                    }}
                    className="sr-only"
                  />
                  <div className={`w-5 h-5 rounded border-2 mr-4 flex items-center justify-center ${
                    answers[currentQuestion.id]?.includes(index)
                      ? 'border-success-500 bg-success-500'
                      : 'border-gray-300'
                  }`}>
                    {answers[currentQuestion.id]?.includes(index) && (
                      <span className="text-white text-sm">✓</span>
                    )}
                  </div>
                  <span className="text-secondary-900">{option}</span>
                </label>
              ))
            )}

            {currentQuestion.type === 'text' && (
              <div>
                <textarea
                  value={answers[currentQuestion.id] || ''}
                  onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                  placeholder="Type your answer here..."
                  className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 transition-all duration-200 resize-none"
                  rows={6}
                />
                <p className="text-sm text-secondary-500 mt-2">
                  Provide a detailed answer. This will be reviewed manually.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setCurrentQuestionIndex(prev => Math.max(0, prev - 1))}
            disabled={currentQuestionIndex === 0}
            className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
              currentQuestionIndex === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
            }`}
          >
            ← Previous
          </button>

          <div className="flex items-center space-x-4">
            <button
              onClick={handleSubmit}
              className="px-8 py-3 bg-danger-600 text-white rounded-lg font-medium hover:bg-danger-700 transition-all duration-200 shadow-soft hover:shadow-medium"
            >
              Submit Quiz
            </button>

            {currentQuestionIndex < quiz.questions.length - 1 ? (
              <button
                onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-all duration-200 shadow-soft hover:shadow-medium"
              >
                Next →
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                className="px-6 py-3 bg-success-600 text-white rounded-lg font-medium hover:bg-success-700 transition-all duration-200 shadow-soft hover:shadow-medium"
              >
                Finish Quiz
              </button>
            )}
          </div>
        </div>

        {/* Anti-cheating notice */}
        <div className="mt-6 p-4 bg-warning-50 border border-warning-200 rounded-lg">
          <div className="flex items-center space-x-3">
            <span className="text-warning-600">🔒</span>
            <div>
              <p className="text-sm font-medium text-warning-800">
                Quiz Security Active
              </p>
              <p className="text-xs text-warning-600">
                Tab switching and fullscreen exit are monitored. Multiple violations may result in quiz termination.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TakeQuizPage;
