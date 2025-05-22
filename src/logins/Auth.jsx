// src/logins/auth.js

// Save token and user data to localStorage
export const setAuthData = (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  };
  
  // Get token from localStorage
  export const getToken = () => {
    return localStorage.getItem('token');
  };
  
  // Get user data from localStorage
  export const getUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  };
  
  // Remove auth data from localStorage
  export const clearAuthData = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };
  
  // Check if user is authenticated
  export const isAuthenticated = () => {
    return !!getToken();
  };
  
  // Check if user has specific role (if implementing roles)
  export const hasRole = (role) => {
    const user = getUser();
    return user?.roles?.includes(role);
  };