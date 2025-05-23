import React, { useState } from 'react';
import { 
  FaSearch, FaFilter, FaFileAlt, FaClock, 
  FaMoneyBillWave, FaCheckCircle, FaTimesCircle, 
  FaRegClock, FaChevronLeft, FaChevronRight,
  FaExpandAlt, FaCompressAlt, FaDownload, FaUserTie
} from 'react-icons/fa';
import { BsThreeDotsVertical } from 'react-icons/bs';

const BidManagement = () => {
  // Mock data for Kenyan bids
  const bids = [
    {
      id: "bid_001",
      job: {
        id: "job_101",
        title: "Residential Apartment Construction in Kilimani",
        description: "Construction of a 4-storey luxury apartment building with 12 units, parking, and amenities.",
        customer: {
          name: "Prestige Properties Ltd",
          location: "Kilimani, Nairobi",
          contact: "info@prestigeproperties.co.ke"
        }
      },
      status: "accepted",
      amount: 12500000,
      timeline_weeks: 36,
      proposal: "Our proposal includes complete turnkey construction using quality materials from local suppliers. The project will be completed in three phases: foundation and structure (12 weeks), interior works (16 weeks), and finishing (8 weeks). We include a 2-year structural warranty.",
      created_at: "2023-06-10T14:30:00Z",
      bid_attachments: [
        { name: "Technical_Proposal.pdf", size: "2.4MB" },
        { name: "Cost_Breakdown.xlsx", size: "1.1MB" },
        { name: "Portfolio_Similar_Projects.pdf", size: "5.2MB" }
      ],
      team: [
        { name: "Michael Otieno", role: "Project Manager", experience: "8 years" },
        { name: "Susan Wambui", role: "Lead Architect", experience: "6 years" }
      ]
    },
    // ... (other bid objects from previous example)
  ];

  const [activeTab, setActiveTab] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [expandedBid, setExpandedBid] = useState(null);
  const bidsPerPage = 5;

  // Filter bids
  const filteredBids = bids.filter(bid => {
    const matchesSearch = bid.job?.title?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = activeTab === 'all' || bid.status === activeTab;
    return matchesSearch && matchesStatus;
  });

  // Pagination logic
  const indexOfLastBid = currentPage * bidsPerPage;
  const indexOfFirstBid = indexOfLastBid - bidsPerPage;
  const currentBids = filteredBids.slice(indexOfFirstBid, indexOfLastBid);
  const totalPages = Math.ceil(filteredBids.length / bidsPerPage);

  // Toggle bid expansion
  const toggleExpand = (bidId) => {
    setExpandedBid(expandedBid === bidId ? null : bidId);
  };

  // Status badge component
  const StatusBadge = ({ status }) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-100 text-yellow-800', icon: <FaRegClock className="mr-1" /> },
      accepted: { color: 'bg-green-100 text-green-800', icon: <FaCheckCircle className="mr-1" /> },
      rejected: { color: 'bg-red-100 text-red-800', icon: <FaTimesCircle className="mr-1" /> }
    };

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusConfig[status]?.color || 'bg-gray-100 text-gray-800'}`}>
        {statusConfig[status]?.icon}
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  // Format date in Kenyan style
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-KE', options);
  };

  // Format currency in Kenyan Shillings
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        {/* Header with search and filter */}
        <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <h1 className="text-2xl font-bold text-gray-800">My Bids</h1>
            
            <div className="flex items-center gap-3 w-full md:w-auto">
              <div className="relative flex-1 max-w-md">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FaSearch className="text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Search bids by job title..."
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  value={searchTerm}
                  onChange={(e) => {
                    setSearchTerm(e.target.value);
                    setCurrentPage(1);
                    setExpandedBid(null);
                  }}
                />
              </div>
              
              <button className="px-3 py-2 border border-gray-300 rounded-md flex items-center gap-2 text-gray-700 hover:bg-gray-100 whitespace-nowrap transition-colors">
                <FaFilter />
                <span className="hidden sm:inline">Filters</span>
              </button>
            </div>
          </div>
        </div>
        
        {/* Tabs */}
        <div className="border-b border-gray-200 bg-gray-50">
          <nav className="flex -mb-px overflow-x-auto">
            {['all', 'pending', 'accepted', 'rejected'].map((tab) => (
              <button
                key={tab}
                onClick={() => {
                  setActiveTab(tab);
                  setCurrentPage(1);
                  setExpandedBid(null);
                }}
                className={`whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm ${
                  activeTab === tab
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                {tab !== 'all' && (
                  <span className="ml-1 bg-gray-200 text-gray-600 rounded-full px-2 py-0.5 text-xs">
                    {bids.filter(b => b.status === tab).length}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
        
        {/* Bid List */}
        <div className="divide-y divide-gray-200">
          {currentBids.length > 0 ? (
            currentBids.map((bid) => (
              <div 
                key={bid.id} 
                className={`p-6 transition-all duration-300 ${expandedBid === bid.id ? 'bg-gray-50' : 'hover:bg-gray-50'}`}
              >
                {/* Bid Summary */}
                <div 
                  className="flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer"
                  onClick={() => toggleExpand(bid.id)}
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 flex-wrap">
                      <h2 className="text-lg font-semibold text-gray-800">
                        {bid.job?.title || 'Untitled Job'}
                      </h2>
                      <StatusBadge status={bid.status} />
                    </div>
                    <p className="mt-1 text-sm text-gray-600">
                      <span className="font-medium">Client:</span> {bid.job?.customer?.name || 'Unknown'} • {bid.job?.customer?.location || 'Unknown location'}
                    </p>
                    
                    <div className="mt-3 flex flex-wrap gap-4">
                      <div className="flex items-center text-sm text-gray-500">
                        <FaMoneyBillWave className="mr-2 text-green-500" />
                        <span>{formatCurrency(bid.amount || 0)}</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <FaClock className="mr-2 text-blue-500" />
                        <span>{bid.timeline_weeks || 'N/A'} weeks</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <FaFileAlt className="mr-2 text-purple-500" />
                        <span>{bid.bid_attachments?.length || 0} attachments</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 mt-4 md:mt-0">
                    <div className="text-right">
                      <p className="text-sm text-gray-500">Submitted</p>
                      <p className="text-sm font-medium">
                        {bid.created_at ? formatDate(bid.created_at) : 'Unknown date'}
                      </p>
                    </div>
                    
                    <button 
                      className="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors"
                      onClick={(e) => {
                        e.stopPropagation();
                        // Add action for menu button
                      }}
                    >
                      <BsThreeDotsVertical />
                    </button>
                    
                    <button 
                      className="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleExpand(bid.id);
                      }}
                    >
                      {expandedBid === bid.id ? <FaCompressAlt /> : <FaExpandAlt />}
                    </button>
                  </div>
                </div>
                
                {/* Expanded Bid Details */}
                {expandedBid === bid.id && (
                  <div className="mt-6 pt-6 border-t border-gray-200 animate-fadeIn">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      {/* Left Column */}
                      <div className="md:col-span-2 space-y-4">
                        <div>
                          <h3 className="text-md font-medium text-gray-900 mb-2">Project Description</h3>
                          <p className="text-gray-700">{bid.job?.description || 'No description available.'}</p>
                        </div>
                        
                        <div>
                          <h3 className="text-md font-medium text-gray-900 mb-2">Our Proposal</h3>
                          <p className="text-gray-700 whitespace-pre-line">{bid.proposal}</p>
                        </div>
                        
                        <div>
                          <h3 className="text-md font-medium text-gray-900 mb-2">Project Team</h3>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {bid.team?.map((member, index) => (
                              <div key={index} className="flex items-center gap-3 p-3 bg-gray-100 rounded-lg">
                                <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
                                  <FaUserTie />
                                </div>
                                <div>
                                  <p className="font-medium">{member.name}</p>
                                  <p className="text-sm text-gray-600">{member.role} • {member.experience}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                      
                      {/* Right Column */}
                      <div className="space-y-4">
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h3 className="text-md font-medium text-gray-900 mb-2">Client Information</h3>
                          <div className="space-y-2">
                            <p className="text-gray-700">
                              <span className="font-medium">Company:</span> {bid.job?.customer?.name || 'N/A'}
                            </p>
                            <p className="text-gray-700">
                              <span className="font-medium">Location:</span> {bid.job?.customer?.location || 'N/A'}
                            </p>
                            <p className="text-gray-700">
                              <span className="font-medium">Contact:</span> {bid.job?.customer?.contact || 'N/A'}
                            </p>
                          </div>
                        </div>
                        
                        <div>
                          <h3 className="text-md font-medium text-gray-900 mb-2">Attachments</h3>
                          <div className="space-y-2">
                            {bid.bid_attachments?.map((file, index) => (
                              <div key={index} className="flex items-center justify-between p-2 bg-gray-100 rounded">
                                <div className="flex items-center gap-2">
                                  <FaFileAlt className="text-gray-500" />
                                  <span className="text-sm">{file.name}</span>
                                </div>
                                <button className="text-indigo-600 hover:text-indigo-800 text-sm flex items-center gap-1">
                                  <FaDownload size={12} />
                                  <span>Download</span>
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div className="bg-green-50 p-4 rounded-lg">
                          <h3 className="text-md font-medium text-gray-900 mb-2">Financial Summary</h3>
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-gray-700">Bid Amount:</span>
                              <span className="font-medium">{formatCurrency(bid.amount)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-700">Project Duration:</span>
                              <span className="font-medium">{bid.timeline_weeks} weeks</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-700">Status:</span>
                              <StatusBadge status={bid.status} />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="p-12 text-center">
              <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center text-gray-400 mb-4">
                <FaFileAlt className="text-3xl" />
              </div>
              <h3 className="text-lg font-medium text-gray-900">No bids found</h3>
              <p className="mt-1 text-gray-500">
                {activeTab === 'all' 
                  ? "You haven't submitted any bids yet."
                  : `You don't have any ${activeTab} bids.`}
              </p>
              <button className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors">
                Browse Available Jobs
              </button>
            </div>
          )}
        </div>
        
        {/* Pagination */}
        {filteredBids.length > bidsPerPage && (
          <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center justify-between">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className={`px-3 py-1 rounded-md flex items-center gap-1 ${currentPage === 1 ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                <FaChevronLeft size={14} />
                Previous
              </button>
              
              <div className="hidden sm:flex items-center gap-1">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      currentPage === page 
                        ? 'bg-indigo-600 text-white' 
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    {page}
                  </button>
                ))}
              </div>
              
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className={`px-3 py-1 rounded-md flex items-center gap-1 ${currentPage === totalPages ? 'text-gray-400 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                Next
                <FaChevronRight size={14} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BidManagement;