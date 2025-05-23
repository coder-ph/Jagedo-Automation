// MyBids.jsx
import React from 'react';
import BidStatusTabs from './BidStatusTabs';
import BidList from './BidList';

const MyBids = () => {
  const bids = [
    {
      id: '1',
      jobTitle: 'Home Renovation Project',
      client: 'John Mwangi',
      proposedAmount: 'Ksh 1,100,000',
      proposedTimeline: '30 days',
      submittedDate: '2023-07-25',
      status: 'pending',
      jobId: '1'
    },
    {
      id: '2',
      jobTitle: 'Office Interior Design',
      client: 'Tech Solutions Ltd',
      proposedAmount: 'Ksh 800,000',
      proposedTimeline: '25 days',
      submittedDate: '2023-07-20',
      status: 'accepted',
      jobId: '2'
    },
    {
      id: '3',
      jobTitle: 'Landscaping Project',
      client: 'Susan Wambui',
      proposedAmount: 'Ksh 320,000',
      proposedTimeline: '20 days',
      submittedDate: '2023-07-18',
      status: 'rejected',
      jobId: '3'
    },
    {
      id: '4',
      jobTitle: 'Plumbing System Installation',
      client: 'David Omondi',
      proposedAmount: 'Ksh 250,000',
      proposedTimeline: '15 days',
      submittedDate: '2023-07-15',
      status: 'pending',
      jobId: '4'
    },
  ];

  const [activeStatus, setActiveStatus] = React.useState('all');

  const filteredBids = activeStatus === 'all' 
    ? bids 
    : bids.filter(bid => bid.status === activeStatus);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">My Bids</h1>
      
      <BidStatusTabs 
        activeStatus={activeStatus}
        onChange={setActiveStatus}
        counts={{
          all: bids.length,
          pending: bids.filter(b => b.status === 'pending').length,
          accepted: bids.filter(b => b.status === 'accepted').length,
          rejected: bids.filter(b => b.status === 'rejected').length,
        }}
      />
      
      <BidList bids={filteredBids} />
    </div>
  );
};

export default MyBids;