// ProfessionalDashboard.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import ProfessionalSidebar from './ProfessionalSidebar';
import ProfessionalHeader from './ProfessionalHeader';

const ProfessionalDashboard = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <ProfessionalSidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <ProfessionalHeader />
        
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ProfessionalDashboard;
