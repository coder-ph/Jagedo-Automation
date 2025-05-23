// JobListings.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import JobFilter from './JobFilter';
import JobCard from './JobCard';

const JobListings = () => {
  const [filters, setFilters] = useState({
    category: '',
    location: '',
    budget: '',
    sort: 'newest',
  });

  const jobs = [
    {
      id: '1',
      title: "Home Renovation Project",
      description: "Complete home renovation including kitchen remodeling, bathroom upgrades, and living room redesign.",
      location: "Kileleshwa, Nairobi",
      budget: "Ksh 1,200,000",
      deadline: "2023-08-15",
      postedDate: "2023-07-20",
      serviceType: "Contractor",
      status: "open"
    },
    {
      id: '2',
      title: "Office Interior Design",
      description: "Modern office interior design for a 500 sq ft space with ergonomic furniture and lighting solutions.",
      location: "Westlands, Nairobi",
      budget: "Ksh 850,000",
      deadline: "2023-09-10",
      postedDate: "2023-07-25",
      serviceType: "Interior Designer",
      status: "open"
    },
    {
      id: '3',
      title: "Landscaping Project",
      description: "Garden landscaping including lawn installation, flower beds, and irrigation system.",
      location: "Karen, Nairobi",
      budget: "Ksh 350,000",
      deadline: "2023-08-30",
      postedDate: "2023-07-18",
      serviceType: "Landscaper",
      status: "open"
    },
    {
      id: '4',
      title: "Plumbing System Installation",
      description: "Full plumbing system installation for a new residential building with 4 bathrooms.",
      location: "Runda, Nairobi",
      budget: "Ksh 280,000",
      deadline: "2023-08-25",
      postedDate: "2023-07-22",
      serviceType: "Plumber",
      status: "open"
    },
  ];

  const handleFilterChange = (name, value) => {
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Available Job Listings</h1>
        <Link
          to="/professional-dashboard/bids"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          View My Bids
        </Link>
      </div>
      
      <JobFilter filters={filters} onChange={handleFilterChange} />
      
      <div className="grid grid-cols-1 gap-6">
        {jobs.map(job => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
};

export default JobListings;