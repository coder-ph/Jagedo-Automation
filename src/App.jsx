import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';

import Footer from './components/Footer';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        
        {/* Optional Footer can be added here */}
        <Footer/>
      </div>
    </BrowserRouter>
  );
}

export default App;