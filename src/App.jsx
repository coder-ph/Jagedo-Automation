import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage.jsx';
import CustomerServiceRequest from './Details/CustomerServiceForm.jsx';
import CustomerDashboard from './dashboard/Customer'; // ✅ Imported here

// Optional: placeholders for other user forms, in case you want to add routes for professionals and fundis later
const ProfessionalServiceRequest = () => (
  <div className="p-6 text-center text-xl font-semibold">Professional Service Request Page (Coming Soon)</div>
);
const FundiServiceRequest = () => (
  <div className="p-6 text-center text-xl font-semibold">Fundi Service Request Page (Coming Soon)</div>
);

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />

        <Routes>
          {/* Homepage */}
          <Route path="/" element={<Hero />} />

          {/* Login Page */}
          <Route path="/login" element={<LoginPage />} />

          {/* Signup Page */}
          <Route path="/signup" element={<SignUpPage />} />

          {/* Customer Service Request Page */}
          <Route path="/customer-request" element={<CustomerServiceRequest />} />

          {/* Customer Dashboard */}
          <Route path="/customer-dashboard" element={<CustomerDashboard />} /> {/* ✅ Added */}

          {/* Optional placeholders for other user roles */}
          <Route path="/professional-request" element={<ProfessionalServiceRequest />} />
          <Route path="/fundi-request" element={<FundiServiceRequest />} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
