// Example usage in a parent component
import React from 'react';
import BidList from './BidList';

const ProfessionalDashboard = () => {
  // Mock bid data
  const mockBids = [
    {
      id: '1',
      jobTitle: 'Website Redesign',
      client: 'Acme Corp',
      proposedAmount: 2500,
      submittedDate: '2023-06-15',
      proposedTimeline: 14,
      status: 'pending'
    },
    {
      id: '2',
      jobTitle: 'Mobile App Development',
      client: 'TechStart Inc',
      proposedAmount: 8500,
      submittedDate: '2023-06-10',
      proposedTimeline: 30,
      status: 'accepted'
    },
    {
      id: '3',
      jobTitle: 'SEO Optimization',
      client: 'Local Business LLC',
      proposedAmount: 1200,
      submittedDate: '2023-06-05',
      proposedTimeline: 7,
      status: 'rejected'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Your Bids</h1>
      <BidList bids={mockBids} />
    </div>
  );
};

export default ProfessionalDashboard;