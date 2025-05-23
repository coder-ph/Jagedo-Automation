// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Footer from './components/Footer';
import LoginPage from './logins/LoginPage';
import SignUpPage from './logins/SignUpPage';
import CustomerServiceForm from './Details/CustomerServiceForm';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './logins/ProtectedRoute';
import RequestHistory from './components/RequestHistory';
import Search from './components/Search';
import History from './components/History';
import Notifications from './components/Notifications';
import RequestDetail from './components/RequestDetail';
import ProfessionalForm from './proffesional/ProfessionalDashboard';
import StatCard from './proffesional/StatCard';
import ReviewsSection from './proffesional/ReviewsSection';
import RecentJobs from './proffesional/RecentJobs';
import ProfileDetails from './proffesional/ProfileDetails';
import MyBids from './proffesional/MyBids';
import BidList from './proffesional/BidList';
import ProfileHeader from './proffesional/ProfileHeader';
import BidStatusTabs from './proffesional/BidStatusTabs';
import BidStatusChart from './proffesional/BidStatusChart';
import JobCard from './proffesional/JobCard';
import DashboardOverview from './proffesional/DashboardOverview';
import PortfolioSection from './proffesional/PortfolioSection';
import JobFilter from './proffesional/JobFilter';
import ProfessionalDashboard from './proffesional/ProfessionalDashboard';
import ProfessionalSidebar from './proffesional/ProfessionalSidebar';
import ProfessionalProfile from './proffesional/ProfessionalProfile';
import ProfessionalHeader from './proffesional/ProfessionalHeader';


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
            {/* <Route element={<ProtectedRoute />}> */}
              {/* Customer Routes */}
              <Route path="/customer-request" element={<CustomerServiceForm />} />
              <Route path="/customer-dashboard" element={<Dashboard />} />
              <Route path="/request-history" element={<RequestHistory />} />
              <Route path="/search" element={<Search />} />
              <Route path="/history" element={<History />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/request/:id" element={<RequestDetail />} />
              
              {/* Professional Routes */}
              <Route path="/professional-form" element={<ProfessionalForm />} />
              <Route path="/professional-profile" element={<ProfessionalProfile />} />
              <Route path="/stat-card" element={<StatCard />} />
              <Route path="/review-section" element={<ReviewsSection />} />
              <Route path="/recent-jobs" element={<RecentJobs />} />
              <Route path="/profile-details" element={<ProfileDetails />} />
              <Route path="/my-bids" element={<MyBids />} />
              <Route path="/bid-list" element={<BidList />} />
              <Route path="/profile-header" element={<ProfileHeader />} />
              <Route path="/bid-status-tabs" element={<BidStatusTabs />} />
              <Route path="/bid-status-chart" element={<BidStatusChart />} />
              <Route path="/job-card" element={<JobCard />} />
              <Route path="/dashboard-overview" element={<DashboardOverview />} />
              <Route path="/portfolio-section" element={<PortfolioSection />} />
              <Route path="/job-filter" element={<JobFilter />} />
              <Route path="/professional-sidebar" element={<ProfessionalSidebar />} />
              <Route path="/professional-header" element={<ProfessionalHeader />} />

            {/* </Route> */}

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