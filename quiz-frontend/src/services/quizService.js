// src/services/quizService.js
import api from './api';

// --- Quiz Management ---

/**
 * Fetches all quizzes.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of quiz objects.
 */
const getAllQuizzes = async () => {
  try {
    const response = await api.get('/quizzes');
    return response.data;
  } catch (error) {
    console.error('Error fetching quizzes:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch quizzes');
  }
};

/**
 * Fetches a single quiz by ID.
 * @param {string} quizId - The ID of the quiz.
 * @returns {Promise<object>} A promise that resolves with the quiz object.
 */
const getQuizById = async (quizId) => {
  try {
    const response = await api.get(`/quizzes/${quizId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch quiz details');
  }
};

/**
 * Creates a new quiz.
 * @param {object} quizData - The data for the new quiz.
 * @returns {Promise<object>} A promise that resolves with the created quiz object.
 */
const createQuiz = async (quizData) => {
  try {
    const response = await api.post('/admin/quizzes', quizData); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error('Error creating quiz:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to create quiz');
  }
};

/**
 * Updates an existing quiz.
 * @param {string} quizId - The ID of the quiz to update.
 * @param {object} updatedData - The updated quiz data.
 * @returns {Promise<object>} A promise that resolves with the updated quiz object.
 */
const updateQuiz = async (quizId, updatedData) => {
  try {
    const response = await api.put(`/admin/quizzes/${quizId}`, updatedData); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error(`Error updating quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to update quiz');
  }
};

/**
 * Deletes a quiz by ID.
 * @param {string} quizId - The ID of the quiz to delete.
 * @returns {Promise<void>} A promise that resolves on successful deletion.
 */
const deleteQuiz = async (quizId) => {
  try {
    await api.delete(`/admin/quizzes/${quizId}`); // Admin endpoint
  } catch (error) {
    console.error(`Error deleting quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to delete quiz');
  }
};

// --- Question Management ---

/**
 * Fetches all questions for a specific quiz.
 * @param {string} quizId - The ID of the quiz.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of question objects.
 */
const getQuestionsByQuizId = async (quizId) => {
  try {
    const response = await api.get(`/quizzes/${quizId}/questions`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching questions for quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch questions');
  }
};

/**
 * Creates a new question for a quiz.
 * @param {string} quizId - The ID of the quiz.
 * @param {object} questionData - The data for the new question.
 * @returns {Promise<object>} A promise that resolves with the created question object.
 */
const createQuestion = async (quizId, questionData) => {
  try {
    const response = await api.post(`/admin/quizzes/${quizId}/questions`, questionData); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error(`Error creating question for quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to create question');
  }
};

/**
 * Updates an existing question.
 * @param {string} quizId - The ID of the quiz the question belongs to.
 * @param {string} questionId - The ID of the question to update.
 * @param {object} updatedData - The updated question data.
 * @returns {Promise<object>} A promise that resolves with the updated question object.
 */
const updateQuestion = async (quizId, questionId, updatedData) => {
  try {
    const response = await api.put(`/admin/quizzes/${quizId}/questions/${questionId}`, updatedData); // Admin endpoint
    return response.data;
  } catch (error) {
    console.error(`Error updating question ${questionId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to update question');
  }
};

/**
 * Deletes a question.
 * @param {string} quizId - The ID of the quiz the question belongs to.
 * @param {string} questionId - The ID of the question to delete.
 * @returns {Promise<void>} A promise that resolves on successful deletion.
 */
const deleteQuestion = async (quizId, questionId) => {
  try {
    await api.delete(`/admin/quizzes/${quizId}/questions/${questionId}`); // Admin endpoint
  } catch (error) {
    console.error(`Error deleting question ${questionId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to delete question');
  }
};

// --- Quiz Submission / Results ---

/**
 * Submits user's answers for a quiz to be graded by the backend.
 * @param {string} quizId - The ID of the quiz.
 * @param {object} answers - An object mapping question IDs to user answers.
 * @param {string} timeTaken - Formatted string of time taken (e.g., "MM:SS").
 * @returns {Promise<object>} A promise that resolves with the quiz result object (e.g., score).
 */
const submitQuizAnswers = async (quizId, answers, timeTaken) => {
  try {
    // This endpoint would typically grade the quiz on the backend
    const response = await api.post(`/quizzes/${quizId}/submit`, { answers, timeTaken });
    return response.data;
  } catch (error) {
    console.error(`Error submitting quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to submit quiz');
  }
};

/**
 * Fetches a user's specific quiz result.
 * @param {string} quizId - The ID of the quiz.
 * @param {string} resultId - The ID of the specific result (e.g., timestamp or unique ID).
 * @returns {Promise<object>} A promise that resolves with the detailed quiz result.
 */
const getQuizResult = async (quizId, resultId) => {
  try {
    // This endpoint would fetch a specific result for a user
    const response = await api.get(`/results/${quizId}/${resultId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching result ${resultId} for quiz ${quizId}:`, error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch quiz result');
  }
};

/**
 * Fetches all results for the current user.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of user's quiz results.
 */
const getUserResults = async () => {
  try {
    const response = await api.get('/results/my'); // Endpoint for current user's results
    return response.data;
  } catch (error) {
    console.error('Error fetching user results:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch user results');
  }
};

const quizService = {
  getAllQuizzes,
  getQuizById,
  createQuiz,
  updateQuiz,
  deleteQuiz,
  getQuestionsByQuizId,
  createQuestion,
  updateQuestion,
  deleteQuestion,
  submitQuizAnswers,
  getQuizResult,
  getUserResults,
};

export default quizService;