import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import CustomerServiceForm from './details/CustomerServiceForm';
import LoginPage from './logins/LoginPage';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        {/* Navbar always visible */}
        <Navbar />
        
        <main className="flex-grow">
          <Routes>
            {/* Main page */}
            <Route path="/" element={<Hero />} />
            
            {/* Customer service form */}
            <Route path="/customer-request" element={<CustomerServiceForm />} />
            
            {/* Login page */}
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </main>

        {/* Footer always visible */}
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;