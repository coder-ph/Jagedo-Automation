// src/logins/auth.js

// Set this to true to bypass authentication during development
const DEV_MODE = true;

// Mock user data for development mode
const DEV_USER = {
  id: 1,
  email: 'dev@example.com',
  name: 'Development User',
  role: 'user'
};

export const isAuthenticated = () => {
  if (DEV_MODE) {
    return true; // Always return true in development mode
  }
  
  // Check for access token in localStorage
  const token = localStorage.getItem('access_token');
  return !!token;
};

export const setAuthData = (data) => {
  if (!DEV_MODE) {
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
  }
};

export const clearAuthData = () => {
  if (!DEV_MODE) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }
};

export const getAuthToken = () => {
  if (DEV_MODE) {
    return 'dev-token'; // Return a dummy token in development mode
  }
  return localStorage.getItem('access_token');
};

export const getUser = () => {
  if (DEV_MODE) {
    return DEV_USER; // Return mock user data in development mode
  }
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}; 