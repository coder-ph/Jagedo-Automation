import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage'; // ✅ Import the LoginPage
import SignUpPage from './logins/SignUpPage.jsx';

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

           {/* signup Page */}
          <Route path='signup' element={<SignUpPage/>} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
