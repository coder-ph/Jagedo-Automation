// JobFilter.jsx
import React from 'react';

const JobFilter = ({ filters, onChange }) => {
  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'contractor', label: 'Contractor' },
    { value: 'interior-designer', label: 'Interior Designer' },
    { value: 'plumber', label: 'Plumber' },
    { value: 'electrician', label: 'Electrician' },
    { value: 'landscaper', label: 'Landscaper' },
  ];

  const locations = [
    { value: '', label: 'All Locations' },
    { value: 'nairobi', label: 'Nairobi' },
    { value: 'mombasa', label: 'Mombasa' },
    { value: 'kisumu', label: 'Kisumu' },
    { value: 'nakuru', label: 'Nakuru' },
  ];

  const budgets = [
    { value: '', label: 'Any Budget' },
    { value: '0-100k', label: 'Under Ksh 100,000' },
    { value: '100k-500k', label: 'Ksh 100,000 - 500,000' },
    { value: '500k-1m', label: 'Ksh 500,000 - 1M' },
    { value: '1m+', label: 'Over Ksh 1M' },
  ];

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'deadline', label: 'Closest Deadline' },
    { value: 'budget-high', label: 'Highest Budget' },
    { value: 'budget-low', label: 'Lowest Budget' },
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            id="category"
            name="category"
            value={filters.category}
            onChange={(e) => onChange('category', e.target.value)}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            {categories.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
            Location
          </label>
          <select
            id="location"
            name="location"
            value={filters.location}
            onChange={(e) => onChange('location', e.target.value)}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            {locations.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-1">
            Budget
          </label>
          <select
            id="budget"
            name="budget"
            value={filters.budget}
            onChange={(e) => onChange('budget', e.target.value)}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            {budgets.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
            Sort By
          </label>
          <select
            id="sort"
            name="sort"
            value={filters.sort}
            onChange={(e) => onChange('sort', e.target.value)}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            {sortOptions.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        
        <div className="flex items-end">
          <button
            type="button"
            onClick={() => onChange({ category: '', location: '', budget: '', sort: 'newest' })}
            className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Reset Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default JobFilter;