// src/contexts/QuizContext.js
import React, { createContext, useState, useContext, useCallback } from 'react';

// Create a context for quiz-taking
const QuizContext = createContext(null);

/**
 * Provides quiz-taking state and functions to the application.
 * Manages the active quiz, current question, user's answers, and score.
 */
export const QuizProvider = ({ children }) => {
  const [currentQuiz, setCurrentQuiz] = useState(null); // Stores the full quiz object
  const [quizQuestions, setQuizQuestions] = useState([]); // Array of question objects
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // { questionId: answer(s) }
  const [score, setScore] = useState(0);
  const [quizStatus, setQuizStatus] = useState('idle'); // 'idle', 'loading', 'in-progress', 'finished', 'error'
  const [quizError, setQuizError] = useState(null);
  const [quizResults, setQuizResults] = useState(null); // Final results after quiz finishes

  /**
   * Simulates fetching quiz details and questions by ID.
   * In a real app, this would be an API call.
   */
  const fetchQuizAndQuestions = useCallback(async (quizId) => {
    setQuizStatus('loading');
    setQuizError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API delay

      // Dummy Data: Replace with actual API fetch for quiz and its questions
      const dummyQuizzes = [
        { id: 'q1', title: 'React Basics', description: 'Test your knowledge on React fundamentals.', difficulty: 'Medium', duration: 600, questionCount: 3 },
        { id: 'q2', title: 'JavaScript Advanced', description: 'Challenging questions on JS concepts.', difficulty: 'Hard', duration: 900, questionCount: 2 },
        { id: 'q3', title: 'HTML & CSS Basics', description: 'Fundamental web development concepts.', difficulty: 'Easy', duration: 400, questionCount: 2 },
        { id: 'q4', title: 'Node.js Essentials', description: 'Explore core Node.js concepts, modules, and asynchronous programming.', difficulty: 'Medium', duration: 720, questionCount: 4 },
        { id: 'q5', title: 'Database Basics (SQL)', description: 'Understand SQL queries, table design, and database concepts.', difficulty: 'Medium', duration: 840, questionCount: 6 },
      ];
      const dummyQuestions = {
        'q1': [
          { id: 'q1-1', text: 'What is JSX?', type: 'multiple-choice', options: ['A markup syntax', 'A JavaScript library', 'A CSS preprocessor', 'A database'], correctAnswers: ['A markup syntax'] },
          { id: 'q1-2', text: 'Which hooks manage side effects in functional components?', type: 'checkbox', options: ['useState', 'useEffect', 'useContext', 'useRef'], correctAnswers: ['useEffect'] },
          { id: 'q1-3', text: 'What is the purpose of "props" in React?', type: 'text-input', correctAnswers: ['to pass data to components', 'to pass data from parent to child components'] }
        ],
        'q2': [
          { id: 'q2-1', text: 'Explain event delegation in JavaScript.', type: 'text-input', correctAnswers: ['attach event listener to parent element instead of each child'] },
          { id: 'q2-2', text: 'Which of these are ES6 features?', type: 'checkbox', options: ['let/const', 'arrow functions', 'classes', 'jQuery'], correctAnswers: ['let/const', 'arrow functions', 'classes'] }
        ],
        'q3': [
          { id: 'q3-1', text: 'What does HTML stand for?', type: 'multiple-choice', options: ['Hyper Text Markup Language', 'High Technology Modern Language', 'Home Tool Management Language'], correctAnswers: ['Hyper Text Markup Language'] },
          { id: 'q3-2', text: 'Which CSS property controls the text size?', type: 'text-input', correctAnswers: ['font-size'] }
        ],
         'q4': [ // Node.js Essentials
            { id: 'q4-1', text: 'Which command starts a Node.js REPL session?', type: 'multiple-choice', options: ['node index.js', 'npm start', 'node', 'npm run dev'], correctAnswers: ['node'] },
            { id: 'q4-2', text: 'What is the Node.js event loop?', type: 'text-input', correctAnswers: ['single-threaded non-blocking I/O model', 'handles asynchronous callbacks'] },
            { id: 'q4-3', text: 'Which module is used for file system operations in Node.js?', type: 'multiple-choice', options: ['http', 'fs', 'path', 'util'], correctAnswers: ['fs'] },
            { id: 'q4-4', text: 'Select all global objects in Node.js:', type: 'checkbox', options: ['process', 'console', 'window', '__dirname'], correctAnswers: ['process', 'console', '__dirname'] }
        ],
        'q5': [ // Database Basics (SQL)
            { id: 'q5-1', text: 'Which SQL keyword is used to extract data from a database?', type: 'multiple-choice', options: ['UPDATE', 'INSERT', 'SELECT', 'DELETE'], correctAnswers: ['SELECT'] },
            { id: 'q5-2', text: 'Which SQL command is used to add new rows to a table?', type: 'text-input', correctAnswers: ['INSERT INTO'] },
            { id: 'q5-3', text: 'What does SQL stand for?', type: 'text-input', correctAnswers: ['Structured Query Language'] },
            { id: 'q5-4', text: 'Which SQL clause is used to filter records based on a specified condition?', type: 'multiple-choice', options: ['GROUP BY', 'ORDER BY', 'HAVING', 'WHERE'], correctAnswers: ['WHERE'] },
            { id: 'q5-5', text: 'Select all SQL JOIN types:', type: 'checkbox', options: ['INNER JOIN', 'FULL JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'MIDDLE JOIN'], correctAnswers: ['INNER JOIN', 'FULL JOIN', 'LEFT JOIN', 'RIGHT JOIN'] },
            { id: 'q5-6', text: 'Which SQL command is used to modify existing records in a table?', type: 'text-input', correctAnswers: ['UPDATE'] }
        ]
      };

      const quizData = dummyQuizzes.find(q => q.id === quizId);
      const questionsData = dummyQuestions[quizId];

      if (quizData && questionsData) {
        setCurrentQuiz(quizData);
        setQuizQuestions(questionsData);
        setCurrentQuestionIndex(0);
        setUserAnswers({});
        setScore(0);
        setQuizStatus('in-progress');
      } else {
        setQuizError('Quiz not found or no questions available.');
        setQuizStatus('error');
      }
    } catch (err) {
      setQuizError('Failed to load quiz. Please try again.');
      setQuizStatus('error');
      console.error('Fetch quiz error:', err);
    }
  }, []);

  /**
   * Updates the user's answer for the current question.
   */
  const submitAnswer = useCallback((questionId, answer) => {
    setUserAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: answer,
    }));
  }, []);


  /**
   * Resets the quiz state to idle.
   */
  const resetQuiz = useCallback(() => {
    setCurrentQuiz(null);
    setQuizQuestions([]);
    setCurrentQuestionIndex(0);
    setUserAnswers({});
    setScore(0);
    setQuizStatus('idle');
    setQuizError(null);
    setQuizResults(null);
  }, []);

  /**
   * Calculates the final score and sets quiz status to 'finished'.
   * This logic should ideally be confirmed by the backend to prevent cheating.
   * ✅ DEFINED BEFORE goToNextQuestion
   */
  const finishQuiz = useCallback(async (timeTaken = 'N/A') => {
    setQuizStatus('loading'); // Show loading while results are being processed/sent
    try {
        await new Promise(resolve => setTimeout(resolve, 500)); // Simulate result processing

        let calculatedScore = 0;
        const correctAnswersRecord = []; // To store correct answers for review

        quizQuestions.forEach((question) => {
            const userAnswer = userAnswers[question.id];
            let isCorrect = false;

            if (question.question_type === 'multiple-choice' || question.question_type === 'text-input') {
                const userNorm = String(userAnswer || '').toLowerCase().trim();
                const correctNorms = Array.isArray(question.correctAnswers)
                    ? question.correctAnswers.map(ans => String(ans).toLowerCase().trim())
                    : [String(question.correctAnswers || '').toLowerCase().trim()];

                if (correctNorms.includes(userNorm) && userNorm !== '') {
                    isCorrect = true;
                }
            } else if (question.question_type === 'checkbox') {
                const userNorms = Array.isArray(userAnswer)
                    ? userAnswer.map(a => String(a).toLowerCase().trim()).sort()
                    : [];
                const correctNorms = Array.isArray(question.correctAnswers)
                    ? question.correctAnswers.map(a => String(a).toLowerCase().trim()).sort()
                    : [];

                // Check if all correct answers were selected and only correct answers were selected
                isCorrect = userNorms.length > 0 &&
                            userNorms.length === correctNorms.length &&
                            userNorms.every((val, i) => val === correctNorms[i]);
            }

            if (isCorrect) {
                calculatedScore += 1;
            }
            correctAnswersRecord.push(question.correctAnswers);
        });

        setScore(calculatedScore);
        setQuizResults({
            quizId: currentQuiz.id,
            quizTitle: currentQuiz.title,
            score: calculatedScore,
            totalQuestions: quizQuestions.length,
            userAnswers: { ...userAnswers },
            correctAnswers: correctAnswersRecord,
            timeTaken: timeTaken,
            dateCompleted: new Date().toISOString(),
        });
        setQuizStatus('finished');

    } catch (err) {
        setQuizError('Failed to process quiz results.');
        setQuizStatus('error');
        console.error('Finish quiz error:', err);
    }
  }, [currentQuiz, quizQuestions, userAnswers]); // Dependencies for finishQuiz


  /**
   * Navigates to the next question.
   * ✅ DEFINED AFTER finishQuiz (calls finishQuiz)
   */
  const goToNextQuestion = useCallback(() => {
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
    } else {
      // Quiz finished
      finishQuiz(); // Calls finishQuiz
    }
  }, [currentQuestionIndex, quizQuestions.length, finishQuiz]); // finishQuiz added to dependencies


  /**
   * Navigates to the previous question.
   */
  const goToPreviousQuestion = useCallback(() => {
    setCurrentQuestionIndex((prevIndex) => Math.max(0, prevIndex - 1));
  }, []);


  const currentQuestion = quizQuestions[currentQuestionIndex];

  return (
    <QuizContext.Provider value={{
      currentQuiz,
      quizQuestions,
      currentQuestionIndex,
      currentQuestion,
      userAnswers,
      score,
      quizStatus,
      quizError,
      quizResults,
      fetchQuizAndQuestions,
      submitAnswer,
      goToNextQuestion,
      goToPreviousQuestion,
      finishQuiz,
      resetQuiz,
      // You can add more like: saveProgress, loadProgress
    }}>
      {children}
    </QuizContext.Provider>
  );
};

/**
 * Custom hook to easily consume the QuizContext.
 */
export const useQuiz = () => {
  const context = useContext(QuizContext);
  if (context === undefined) {
    throw new Error('useQuiz must be used within a QuizProvider');
  }
  return context;
};