// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './details/CustomerServiceForm';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './logins/ProtectedRoute';
import RequestHistory from './components/RequestHistory';
import Search from './components/Search';
import History from './components/History';
import Notifications from './components/Notifications';
import RequestDetail from './components/RequestDetail';

// Simple placeholder components for any missing ones
function Documents() {
  return <div className="p-4">Documents Management</div>;
}

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
              <Route path="/customer-dashboard" element={<Dashboard />} />
              <Route path="/request-history" element={<RequestHistory />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="/search" element={<Search />} />
              <Route path="/history" element={<History />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/request/:id" element={<RequestDetail />} />
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