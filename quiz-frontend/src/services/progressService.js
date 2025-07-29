// quiz-frontend/src/services/progressService.js
import api from './api';

const getProgressData = async () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.warn("No access token found. User may not be logged in.");
    throw new Error("User not authenticated");
  }

  try {
    const response = await api.get('/results/progress/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    return response.data;

  } catch (error) {
    console.error('Error fetching user progress:', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to fetch user progress');
  }
};

const progressService = {
  getProgressData,
};

export default progressService;

