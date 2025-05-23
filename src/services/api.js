import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: '/api', // This will be proxied to http://localhost:5000/api by Vite
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 10000, // 10 seconds timeout
});

// Add a request interceptor to include the auth token in requests
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    // Check if response data exists and is valid JSON
    if (response.data === '' || response.data === undefined) {
      return Promise.reject(new Error('Empty response from server'));
    }
    return response;
  },
  (error) => {
    // Handle network errors
    if (error.message === 'Network Error') {
      error.response = {
        data: { message: 'Unable to connect to the server. Please check your internet connection.' },
        status: 0
      };
    }
    
    // Handle common errors here (e.g., 401 Unauthorized)
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login if token is invalid/expired
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
