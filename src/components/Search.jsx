import React, { useState } from 'react';
import { FaSearch, FaFilter, FaFileAlt, FaMapMarkerAlt, FaCalendarAlt, FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const Search = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [searchResults, setSearchResults] = useState([]);

  // Mock data - replace with API calls
  const mockData = [
    { id: 'JPG-1001', type: 'request', title: 'Land Survey Request', description: 'Request for land survey in downtown area', date: '2023-06-15' },
    { id: 'DOC-001', type: 'document', title: 'Survey Report.pdf', description: 'Final survey report for plot #245', date: '2023-06-18' },
    { id: 'JPG-1002', type: 'request', title: 'Soil Analysis Request', description: 'Soil composition analysis for construction site', date: '2023-06-10' },
    { id: 'DOC-002', type: 'document', title: 'Topographic Map.jpg', description: 'Detailed topographic map of the region', date: '2023-05-28' },
    { id: 'LOC-001', type: 'location', title: 'Plot #245 Coordinates', description: 'GPS coordinates for the surveyed plot', date: '2023-06-16' },
  ];

  const handleSearch = () => {
    const results = mockData.filter(item => {
      const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          item.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesFilter = activeFilter === 'all' || item.type === activeFilter;
      return matchesSearch && matchesFilter;
    });
    setSearchResults(results);
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'request': return <FaFileAlt className="text-indigo-500" />;
      case 'document': return <FaFileAlt className="text-blue-500" />;
      case 'location': return <FaMapMarkerAlt className="text-green-500" />;
      default: return <FaFileAlt className="text-gray-500" />;
    }
  };

  const handleBack = () => {
    navigate(-1); // Go back to previous page
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back button added here */}
      <button 
        onClick={handleBack}
        className="flex items-center text-indigo-600 hover:text-indigo-800 mb-6 transition-colors"
      >
        <FaArrowLeft className="mr-2" />
        Back
      </button>

      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Search Japageo Resources</h1>
        <p className="text-lg text-gray-600">Find requests, documents, and location data</p>
      </div>

      <div className="max-w-3xl mx-auto mb-8">
        <div className="relative rounded-md shadow-sm">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaSearch className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 pr-12 py-3 text-lg border-gray-300 rounded-md"
            placeholder="Search for requests, documents, locations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <div className="absolute inset-y-0 right-0 flex items-center">
            <button
              onClick={handleSearch}
              className="px-4 py-2 bg-indigo-600 text-white rounded-r-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Search
            </button>
          </div>
        </div>
      </div>

      <div className="flex justify-center space-x-4 mb-8">
        <button
          onClick={() => setActiveFilter('all')}
          className={`px-4 py-2 rounded-md ${activeFilter === 'all' ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'} hover:bg-gray-200`}
        >
          All
        </button>
        <button
          onClick={() => setActiveFilter('request')}
          className={`px-4 py-2 rounded-md ${activeFilter === 'request' ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'} hover:bg-gray-200`}
        >
          Requests
        </button>
        <button
          onClick={() => setActiveFilter('document')}
          className={`px-4 py-2 rounded-md ${activeFilter === 'document' ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'} hover:bg-gray-200`}
        >
          Documents
        </button>
        <button
          onClick={() => setActiveFilter('location')}
          className={`px-4 py-2 rounded-md ${activeFilter === 'location' ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100 text-gray-700'} hover:bg-gray-200`}
        >
          Locations
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        {searchResults.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {searchResults.map((result) => (
              <li key={result.id} className="hover:bg-gray-50 transition-colors duration-150">
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 mr-4">
                        {getTypeIcon(result.type)}
                      </div>
                      <div>
                        <p className="text-lg font-medium text-gray-900">
                          {result.title}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          {result.description}
                        </p>
                      </div>
                    </div>
                    <div className="ml-4 flex-shrink-0 flex items-center text-sm text-gray-500">
                      <FaCalendarAlt className="mr-1" />
                      {result.date}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="px-4 py-12 text-center">
            {searchTerm ? (
              <p className="text-gray-500">No results found for "{searchTerm}"</p>
            ) : (
              <p className="text-gray-500">Enter a search term to find resources</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;