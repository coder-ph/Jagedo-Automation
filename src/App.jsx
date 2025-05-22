// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './logins/AuthContext'; // Updated import path
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './details/CustomerServiceForm';
import DashboardLayout from './dashboard/DashboardLayout';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider> {/* Now using AuthProvider from the correct path */}
        <div className="min-h-screen flex flex-col">
          <Navbar />
          
          <main className="flex-grow">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Hero />} />
              <Route 
                path="/login" 
                element={
                  <PublicRoute>
                    <LoginPage />
                  </PublicRoute>
                } 
              />
              <Route 
                path="/signup" 
                element={
                  <PublicRoute>
                    <SignUpPage />
                  </PublicRoute>
                } 
              />
              <Route path="/customer-request" element={<CustomerServiceForm />} />

              {/* Protected Routes */}
              <Route 
                path="/customer-dashboard/*" 
                element={
                  <ProtectedRoute>
                    <DashboardLayout />
                  </ProtectedRoute>
                }
              >
                {/* ... nested routes remain the same ... */}
              </Route>

              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Public Route Component
const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? children : <Navigate to="/customer-dashboard" replace />;
};

export default App;