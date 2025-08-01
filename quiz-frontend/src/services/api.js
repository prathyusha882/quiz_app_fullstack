import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000, // 10 second timeout
});

instance.interceptors.request.use((config) => {
  console.log('API: Making request to:', config.url);
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

instance.interceptors.response.use(
  (response) => {
    console.log('API: Response received from:', response.config.url);
    return response;
  },
  (error) => {
    console.error('API: Error response from:', error.config?.url, error.response?.status, error.message);
    if (error.response && error.response.status === 401) {
      // Clear auth data and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('quiz_user');
      localStorage.removeItem('quiz_isAuthenticated');
      window.location.href = '/login'; // Adjust if your login route is different
    }
    return Promise.reject(error);
  }
);

export default instance;
