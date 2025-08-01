// quiz-frontend/src/services/progressService.js
import api from './api';

const getProgressData = async () => {
  try {
    console.log('progressService: Making request to /api/results/progress/');
    const response = await api.get('/api/results/progress/');
    console.log('progressService: Response received:', response.data);
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

