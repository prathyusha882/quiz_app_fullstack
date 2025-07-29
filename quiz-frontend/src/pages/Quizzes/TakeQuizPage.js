// src/pages/Quizzes/TakeQuizPage.js
import React, { useEffect} from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuiz } from '../../contexts/QuizContext';
import { useQuizTimer } from '../../hooks/useQuizTimer';
import QuestionDisplay from '../../components/quizzes/QuestionDisplay';
import Timer from '../../components/quizzes/Timer';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import QuizResultSummary from '../../components/results/QuizResultSummary';
import './QuizPages.css';

const TakeQuizPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const {
    currentQuiz,
    quizQuestions,
    currentQuestionIndex,
    currentQuestion,
    userAnswers,
    quizStatus,
    quizError,
    quizResults,
    fetchQuizAndQuestions,
    submitAnswer,
    goToNextQuestion,
    goToPreviousQuestion,
    finishQuiz,
    resetQuiz,
  } = useQuiz();

  const {
    formattedTime,
    isRunning,
    startTimer,
    pauseTimer,
    resetTimer: resetQuizTimer,
  } = useQuizTimer(currentQuiz ? currentQuiz.duration : 0, false, () => finishQuiz(formattedTime));

  useEffect(() => {
    if (quizId && quizStatus === 'idle') {
      fetchQuizAndQuestions(quizId);
    }
  }, [quizId, quizStatus, fetchQuizAndQuestions]);

  useEffect(() => {
    if (quizStatus === 'in-progress' && !isRunning && currentQuiz && currentQuiz.duration > 0) {
      startTimer();
    }
    if (quizStatus !== 'in-progress' && isRunning) {
      pauseTimer();
    }
  }, [quizStatus, isRunning, startTimer, pauseTimer, currentQuiz]);

  const handleNext = () => {
    goToNextQuestion();
  };

  const handlePrevious = () => {
    goToPreviousQuestion();
  };

  const handleSubmitQuiz = () => {
    finishQuiz(formattedTime);
  };

  const handleReviewAnswers = () => {
    if (quizResults) {
      navigate(
        `/results/review/${quizResults.quizId}/${encodeURIComponent(quizResults.dateCompleted)}`
      );
    }
  };

  const handleTakeAnotherQuiz = () => {
    resetQuiz();
    resetQuizTimer();
    navigate('/quizzes');
  };

  if (quizStatus === 'loading') {
    return (
      <div className="quiz-page-container loading-state">
        <LoadingSpinner />
        <p>Loading quiz...</p>
      </div>
    );
  }

  if (quizStatus === 'error') {
    return (
      <div className="quiz-page-container error-state">
        <p className="error-message">{quizError}</p>
        <Button onClick={() => navigate('/quizzes')} variant="primary">
          Back to Quizzes
        </Button>
      </div>
    );
  }

  if (quizStatus === 'finished' && quizResults) {
    return (
      <div className="quiz-page-container finished-state">
        <QuizResultSummary
          result={quizResults}
          onReviewAnswers={() =>
            navigate(`/results/review/${quizResults.quizId}/${quizResults.id}`)
  }
  onTakeAnotherQuiz={handleTakeAnotherQuiz}
/>
      </div>
    );
  }

  if (quizStatus !== 'in-progress' || !currentQuiz || !currentQuestion) {
    return (
      <div className="quiz-page-container empty-state">
        <p>Please select a quiz to start.</p>
        <Button onClick={() => navigate('/quizzes')} variant="primary">
          Browse Quizzes
        </Button>
      </div>
    );
  }

  const isLastQuestion = currentQuestionIndex === quizQuestions.length - 1;
  const isFirstQuestion = currentQuestionIndex === 0;

  return (
    <div className="quiz-page-container">
      <h1 className="quiz-page-title">{currentQuiz.title}</h1>

      <div className="quiz-header">
        {currentQuiz.duration > 0 && (
          <Timer duration={currentQuiz.duration} onTimeUp={handleSubmitQuiz} isRunning={isRunning} />
        )}
        <span className="question-progress">
          Question {currentQuestionIndex + 1} of {quizQuestions.length}
        </span>
      </div>

      <QuestionDisplay
        question={currentQuestion}
        selectedAnswer={userAnswers[currentQuestion.id]}
        onAnswerSelect={(answer) => submitAnswer(currentQuestion.id, answer)}
        questionNumber={currentQuestionIndex + 1}
      />

      <div className="quiz-navigation">
        <Button onClick={handlePrevious} disabled={isFirstQuestion} variant="secondary">
          Previous
        </Button>
        {isLastQuestion ? (
          <Button onClick={handleSubmitQuiz} variant="primary">
            Submit Quiz
          </Button>
        ) : (
          <Button onClick={handleNext} variant="primary">
            Next
          </Button>
        )}
      </div>
    </div>
  );
};

export default TakeQuizPage;
