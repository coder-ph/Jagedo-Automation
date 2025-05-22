<<<<<<< HEAD
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import CustomerServiceForm from './details/CustomerServiceForm';
import LoginPage from './logins/LoginPage';
=======
// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './details/CustomerServiceForm';
>>>>>>> masinde

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
<<<<<<< HEAD
        {/* Navbar always visible */}
=======
>>>>>>> masinde
        <Navbar />
        
        <main className="flex-grow">
          <Routes>
<<<<<<< HEAD
            {/* Main page */}
            <Route path="/" element={<Hero />} />
            
            {/* Customer service form */}
            <Route path="/customer-request" element={<CustomerServiceForm />} />
            
            {/* Login page */}
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </main>

        {/* Footer always visible */}
=======
            {/* Public Routes */}
            <Route path="/" element={<Hero />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/customer-request" element={<CustomerServiceForm />} />

            {/* Fallback Route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

>>>>>>> masinde
        <Footer />
      </div>
    </BrowserRouter>
  );
}

<<<<<<< HEAD
export default App;
=======
export default App;
>>>>>>> masinde
