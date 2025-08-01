// src/services/quizService.js
import axios from './api'; // Uses baseURL and token injection

// --- 📘 Quiz Management ---

export const getAllQuizzes = async () => {
  try {
    const response = await axios.get('/api/quizzes/');
    return response.data;
  } catch (error) {
    console.error('Error fetching quizzes:', error.response?.data || error.message);
    throw error;
  }
};

export const getQuizById = async (quizId) => {
  try {
    const response = await axios.get(`/api/quizzes/${quizId}/`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch quiz:', error.response?.data || error.message);
    throw error;
  }
};

export const createQuiz = async (quizData) => {
  try {
    const response = await axios.post('/api/admin/quizzes/', quizData);
    return response.data;
  } catch (error) {
    console.error('Error creating quiz:', error.response?.data || error.message);
    throw error;
  }
};

export const updateQuiz = async (quizId, updatedData) => {
  try {
    const response = await axios.put(`/api/admin/quizzes/${quizId}/`, updatedData);
    return response.data;
  } catch (error) {
    console.error('Error updating quiz:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteQuiz = async (quizId) => {
  try {
    await axios.delete(`/api/admin/quizzes/${quizId}/`);
  } catch (error) {
    console.error('Error deleting quiz:', error.response?.data || error.message);
    throw error;
  }
};

// --- ❓ Question Management ---

export const getQuestionsByQuizId = async (quizId) => {
  try {
    const response = await axios.get(`/api/quizzes/${quizId}/questions/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching questions:', error.response?.data || error.message);
    throw error;
  }
};

export const createQuestion = async (quizId, questionData) => {
  try {
    const response = await axios.post(`/api/admin/quizzes/${quizId}/questions/`, questionData);
    return response.data;
  } catch (error) {
    console.error('Error creating question:', error.response?.data || error.message);
    throw error;
  }
};

export const updateQuestion = async (quizId, questionId, updatedData) => {
  try {
    const response = await axios.put(`/api/admin/quizzes/${quizId}/questions/${questionId}/`, updatedData);
    return response.data;
  } catch (error) {
    console.error('Error updating question:', error.response?.data || error.message);
    throw error;
  }
};

export const deleteQuestion = async (quizId, questionId) => {
  try {
    await axios.delete(`/api/admin/quizzes/${quizId}/questions/${questionId}/`);
  } catch (error) {
    console.error('Error deleting question:', error.response?.data || error.message);
    throw error;
  }
};

// --- 📝 Quiz Submission & Results ---

export const submitQuizAnswers = async (quizId, answers, timeTaken) => {
  try {
    const response = await axios.post(`/api/results/submit/${quizId}/`, { answers, timeTaken });
    return response.data;
  } catch (error) {
    console.error('Error submitting quiz:', error.response?.data || error.message);
    throw error;
  }
};

export const getQuizResult = async (quizId, resultId) => {
  try {
    const response = await axios.get(`/api/results/${quizId}/${resultId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching quiz result:', error.response?.data || error.message);
    throw error;
  }
};

export const getUserResults = async () => {
  try {
    const response = await axios.get('/api/results/my/');
    return response.data;
  } catch (error) {
    console.error('Error fetching user results:', error.response?.data || error.message);
    throw error;
  }
};

export const getQuizReviewDetails = async (quizId, resultId) => {
  try {
    const response = await axios.get(`/api/results/${quizId}/${resultId}/review/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching review data:', error.response?.data || error.message);
    throw error;
  }
};

// --- 🤖 AI Question Generation (Admin) ---

export const generateAIQuestions = async (data) => {
  try {
    const response = await axios.post('/api/admin/generate-ai-questions/', data);
    return response.data;
  } catch (error) {
    console.error('Error generating AI questions:', error.response?.data || error.message);
    throw error;
  }
};

// ✅ Add default export (IMPORTANT for resolving import errors)
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
  getQuizReviewDetails,
  generateAIQuestions,
};

export default quizService;
