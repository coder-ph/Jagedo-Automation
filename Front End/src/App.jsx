import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './logins/CustomerServiceForm';
import DashboardLayout from './dashboard/DashboardLayout';
import CustomerDashboard from './dashboard/customer/CustomerDashboard';
import ProjectsList from './dashboard/customer/ProjectsList';
import ProjectDetails from './dashboard/customer/ProjectDetails';
import ProjectDetailsLeft from './dashboard/customer/ProjectDetailsLeft';
import ProjectDetailsRight from './dashboard/customer/ProjectDetailsRight';
import ProjectDetailsModal from './dashboard/customer/ProjectDetailsModal';
import ProjectFilesSection from './dashboard/customer/ProjectFilesSection';
import ProjectFilesModal from './dashboard/customer/ProjectFilesModal';
import ProjectsTabs from './dashboard/customer/ProjectsTabs';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState(null);

  const handleLogin = (role) => {
    setIsAuthenticated(true);
    setUserRole(role);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUserRole(null);
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        {/* Navbar always visible */}
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        
        <main className="flex-grow">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Hero />} />
            <Route 
              path="/login" 
              element={
                !isAuthenticated ? (
                  <LoginPage onLogin={handleLogin} />
                ) : (
                  <Navigate to="/customer-dashboard" replace />
                )
              } 
            />
            <Route 
              path="/signup" 
              element={
                !isAuthenticated ? (
                  <SignUpPage />
                ) : (
                  <Navigate to="/customer-dashboard" replace />
                )
              } 
            />
            <Route path="/customer-request" element={<CustomerServiceForm />} />

            {/* Protected Routes */}
            <Route 
              path="/customer-dashboard/*" 
              element={
                isAuthenticated ? (
                  <DashboardLayout role={userRole} onLogout={handleLogout} />
                ) : (
                  <Navigate to="/login" replace />
                )
              }
            >
              <Route index element={<CustomerDashboard />} />
              <Route path="projects" element={<ProjectsList />} />
              <Route path="projects/:id" element={<ProjectDetails />}>
                <Route 
                  path="details" 
                  element={
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-4">
                      <div className="lg:col-span-2">
                        <ProjectDetailsLeft />
                      </div>
                      <div className="lg:col-span-1">
                        <ProjectDetailsRight />
                        <ProjectDetailsModal />
                      </div>
                    </div>
                  } 
                />
                <Route 
                  path="files" 
                  element={
                    <div className="p-4">
                      <ProjectFilesSection />
                      <ProjectFilesModal />
                    </div>
                  } 
                />
              </Route>
              <Route path="tabs" element={<ProjectsTabs />} />
            </Route>

            {/* Fallback route */}
            <Route path="*" element={<Navigate to={isAuthenticated ? "/customer-dashboard" : "/"} />} />
          </Routes>
        </main>

        {/* Footer always visible */}
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;