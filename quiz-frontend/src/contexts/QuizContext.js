// src/contexts/QuizContext.js
import React, { createContext, useState, useContext, useCallback } from 'react';
import quizService from '../services/quizService'; // ✅ Make sure this exists and works

const QuizContext = createContext(null);

export const QuizProvider = ({ children }) => {
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [score, setScore] = useState(0);
  const [quizStatus, setQuizStatus] = useState('idle');
  const [quizError, setQuizError] = useState(null);
  const [quizResults, setQuizResults] = useState(null);

  const fetchQuizAndQuestions = useCallback(async (quizId) => {
    setQuizStatus('loading');
    setQuizError(null);
    try {
      const quizDetail = await quizService.getQuizById(quizId);
      const questionsData = await quizService.getQuestionsForQuizAttempt(quizId);

      if (quizDetail && questionsData?.length > 0) {
        setCurrentQuiz(quizDetail);
        setQuizQuestions(questionsData);
        setCurrentQuestionIndex(0);
        setUserAnswers({});
        setScore(0);
        setQuizStatus('in-progress');
      } else {
        setQuizError('No quiz data available.');
        setQuizStatus('error');
      }
    } catch (err) {
      setQuizError(err.message || 'Failed to load quiz.');
      setQuizStatus('error');
      console.error('Fetch quiz error:', err);
    }
  }, []);

  const submitAnswer = useCallback((questionId, answer) => {
    setUserAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: answer,
    }));
  }, []);

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

  const finishQuiz = useCallback(async (timeTaken = 'N/A') => {
    setQuizStatus('loading');
    try {
      await new Promise(resolve => setTimeout(resolve, 500)); // simulate result processing

      let calculatedScore = 0;
      const correctAnswersRecord = [];

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
  }, [currentQuiz, quizQuestions, userAnswers]);

  const goToNextQuestion = useCallback(() => {
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
    } else {
      finishQuiz();
    }
  }, [currentQuestionIndex, quizQuestions.length, finishQuiz]);

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
    }}>
      {children}
    </QuizContext.Provider>
  );
};

export const useQuiz = () => {
  const context = useContext(QuizContext);
  if (context === undefined) {
    throw new Error('useQuiz must be used within a QuizProvider');
  }
  return context;
};
