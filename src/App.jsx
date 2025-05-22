// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './details/CustomerServiceForm';
// import CustomerDashboard from './components/CustomerDashboard';
import ProtectedRoute from './logins/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        
        <main className="flex-grow">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Hero />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />} />
            
            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/customer-request" element={<CustomerServiceForm />} />
              {/* <Route path="/customer-dashboard" element={<CustomerDashboard />} /> */}
            </Route>

            {/* Fallback Route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;