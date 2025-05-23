// src/logins/auth.js

// Save token and user data to localStorage
export const setAuthData = (token, user) => {
  if (!token || !user) {
    console.error('Invalid auth data provided');
    return false;
  }
  
  try {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    return true;
  } catch (error) {
    console.error('Error storing auth data:', error);
    return false;
  }
};

// Get token from localStorage
export const getToken = () => {
  try {
    return localStorage.getItem('token');
  } catch (error) {
    console.error('Error retrieving token:', error);
    return null;
  }
};

// Get user data from localStorage
export const getUser = () => {
  try {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  } catch (error) {
    console.error('Error retrieving user data:', error);
    return null;
  }
};

// Remove auth data from localStorage
export const clearAuthData = () => {
  try {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return true;
  } catch (error) {
    console.error('Error clearing auth data:', error);
    return false;
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = getToken();
  const user = getUser();
  return !!(token && user);
};

// Check if user has specific role (if implementing roles)
export const hasRole = (role) => {
  try {
    const user = getUser();
    if (!user) return false;
    
    // Check both roles array and single role
    if (Array.isArray(user.roles)) {
      return user.roles.includes(role);
    }
    return user.role?.toUpperCase() === role.toUpperCase();
  } catch (error) {
    console.error('Error checking user role:', error);
    return false;
  }
};