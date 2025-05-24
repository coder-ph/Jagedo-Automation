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
    {
      id: "bid_002",
      job: {
        id: "job_102",
        title: "Office Renovation in Westlands",
        description: "Complete renovation of 5,000 sq ft office space including electrical, plumbing, and interior design.",
        customer: {
          name: "TechHub Africa",
          location: "Westlands, Nairobi",
          contact: "projects@techhubafrica.com"
        }
      },
      status: "pending",
      amount: 3800000,
      timeline_weeks: 10,
      proposal: "We propose a modern open-plan design with energy-efficient lighting and HVAC systems. Our team will work nights and weekends to minimize business disruption. Includes 1-year warranty on all workmanship.",
      created_at: "2023-07-15T09:15:00Z",
      bid_attachments: [
        { name: "Design_Concept.pdf", size: "3.7MB" },
        { name: "Renovation_Plan.pdf", size: "1.8MB" }
      ],
      team: [
        { name: "James Mwangi", role: "Interior Designer", experience: "5 years" },
        { name: "Grace Akinyi", role: "Site Supervisor", experience: "4 years" }
      ]
    },
    {
      id: "bid_003",
      job: {
        id: "job_103",
        title: "Road Construction in Thika",
        description: "Construction of 2km access road with drainage system in Thika's industrial area.",
        customer: {
          name: "Thika Municipal Council",
          location: "Thika, Kiambu County",
          contact: "engineering@thikamunicipal.go.ke"
        }
      },
      status: "rejected",
      amount: 28750000,
      timeline_weeks: 24,
      proposal: "Our bid includes full road construction using durable materials suitable for heavy truck traffic. We propose a phased approach to maintain partial access during construction. Includes 5-year maintenance agreement.",
      created_at: "2023-05-22T11:45:00Z",
      bid_attachments: [
        { name: "Technical_Specs.pdf", size: "4.2MB" },
        { name: "Construction_Timeline.pdf", size: "1.5MB" },
        { name: "Company_Certifications.pdf", size: "2.8MB" }
      ],
      team: [
        { name: "David Kamau", role: "Civil Engineer", experience: "10 years" },
        { name: "Sarah Njoroge", role: "Quantity Surveyor", experience: "7 years" }
      ]
    },
    {
      id: "bid_004",
      job: {
        id: "job_104",
        title: "Solar Installation for School in Kajiado",
        description: "Installation of 50kW solar power system with battery backup for a boarding school.",
        customer: {
          name: "Maasai Education Foundation",
          location: "Kajiado County",
          contact: "director@maasaieducation.org"
        }
      },
      status: "accepted",
      amount: 9500000,
      timeline_weeks: 8,
      proposal: "We propose a hybrid solar system with 120 panels and battery storage capable of 3 days autonomy. Includes staff training and 5-year comprehensive maintenance contract with remote monitoring.",
      created_at: "2023-08-03T16:20:00Z",
      bid_attachments: [
        { name: "System_Design.pdf", size: "3.1MB" },
        { name: "Equipment_Specs.pdf", size: "2.6MB" },
        { name: "Maintenance_Agreement.pdf", size: "1.2MB" }
      ],
      team: [
        { name: "Peter Ndirangu", role: "Solar Engineer", experience: "6 years" },
        { name: "Lucy Wanjiru", role: "Electrical Engineer", experience: "5 years" }
      ]
    },
    {
      id: "bid_005",
      job: {
        id: "job_105",
        title: "Hospital HVAC System Upgrade",
        description: "Upgrade of HVAC systems for a 300-bed hospital in Mombasa.",
        customer: {
          name: "Coast General Hospital",
          location: "Mombasa",
          contact: "facilities@coasthospital.go.ke"
        }
      },
      status: "pending",
      amount: 18700000,
      timeline_weeks: 16,
      proposal: "Our proposal includes energy-efficient HVAC systems with HEPA filtration for critical areas. We'll implement in phases to maintain hospital operations. Includes 24/7 emergency support contract.",
      created_at: "2023-09-12T10:30:00Z",
      bid_attachments: [
        { name: "HVAC_Design.pdf", size: "5.4MB" },
        { name: "Phased_Implementation.pdf", size: "2.3MB" }
      ],
      team: [
        { name: "Robert Ochieng", role: "HVAC Specialist", experience: "12 years" },
        { name: "Mary Atieno", role: "Project Coordinator", experience: "8 years" }
      ]
    },
    {
      id: "bid_006",
      job: {
        id: "job_106",
        title: "Warehouse Construction in Athi River",
        description: "Construction of 10,000 sq ft warehouse with office space and loading docks.",
        customer: {
          name: "Logistics Solutions Kenya",
          location: "Athi River EPZ",
          contact: "tenders@logisticske.com"
        }
      },
      status: "accepted",
      amount: 42500000,
      timeline_weeks: 20,
      proposal: "We propose a steel-framed warehouse with concrete floor suitable for heavy equipment. Includes fire suppression system and security features. Project can be completed in 5 months with our accelerated schedule.",
      created_at: "2023-07-28T13:45:00Z",
      bid_attachments: [
        { name: "Structural_Design.pdf", size: "6.8MB" },
        { name: "Construction_Methodology.pdf", size: "3.2MB" },
        { name: "Safety_Plan.pdf", size: "1.9MB" }
      ],
      team: [
        { name: "Samuel Kariuki", role: "Construction Manager", experience: "15 years" },
        { name: "Elizabeth Muthoni", role: "Structural Engineer", experience: "9 years" }
      ]
    },
    {
      id: "bid_007",
      job: {
        id: "job_107",
        title: "Hotel Interior Design in Diani",
        description: "Complete interior design and furnishing for a 50-room boutique hotel.",
        customer: {
          name: "Diani Beach Resorts",
          location: "Diani Beach, Kwale",
          contact: "development@dianiresorts.com"
        }
      },
      status: "rejected",
      amount: 28500000,
      timeline_weeks: 18,
      proposal: "Our design concept blends contemporary Swahili coastal aesthetics with modern luxury. Includes custom furniture, lighting, and artwork from local artisans. Project timeline accounts for overseas shipping of specialty items.",
      created_at: "2023-06-30T15:10:00Z",
      bid_attachments: [
        { name: "Design_Concept.pdf", size: "8.5MB" },
        { name: "Material_Samples.pdf", size: "4.7MB" },
        { name: "Furniture_Specs.pdf", size: "3.2MB" }
      ],
      team: [
        { name: "Fatma Ali", role: "Lead Designer", experience: "7 years" },
        { name: "Joseph Musyoki", role: "Procurement Specialist", experience: "6 years" }
      ]
    },
    {
      id: "bid_008",
      job: {
        id: "job_108",
        title: "School Playground Equipment Installation",
        description: "Supply and installation of playground equipment for primary school in Nakuru.",
        customer: {
          name: "Nakuru Primary School",
          location: "Nakuru Town",
          contact: "office@nakuruprimary.sc.ke"
        }
      },
      status: "pending",
      amount: 3200000,
      timeline_weeks: 6,
      proposal: "We propose a complete playground with safety-certified equipment including swings, slides, and climbing structures. Installation includes impact-absorbing rubber surfacing for safety. All materials are weather-resistant and low-maintenance.",
      created_at: "2023-10-05T11:20:00Z",
      bid_attachments: [
        { name: "Equipment_Catalog.pdf", size: "2.9MB" },
        { name: "Installation_Plan.pdf", size: "1.4MB" }
      ],
      team: [
        { name: "Brian Omollo", role: "Installation Supervisor", experience: "5 years" },
        { name: "Winnie Adhiambo", role: "Safety Inspector", experience: "4 years" }
      ]
    },
    {
      id: "bid_009",
      job: {
        id: "job_109",
        title: "Fencing and Security Installation for Farm",
        description: "Perimeter fencing and security system for 50-acre farm in Laikipia.",
        customer: {
          name: "Laikipia Highlands Farm",
          location: "Laikipia County",
          contact: "security@laikipiafarm.co.ke"
        }
      },
      status: "accepted",
      amount: 18750000,
      timeline_weeks: 12,
      proposal: "Our solution includes 8ft game-proof fencing with electric deterrent, CCTV surveillance system with solar power, and access control gates. All equipment is wildlife-resistant and designed for harsh conditions.",
      created_at: "2023-08-18T14:50:00Z",
      bid_attachments: [
        { name: "Security_Design.pdf", size: "5.6MB" },
        { name: "Equipment_Specs.pdf", size: "3.1MB" },
        { name: "Maintenance_Manual.pdf", size: "2.4MB" }
      ],
      team: [
        { name: "Daniel Kiprop", role: "Security Specialist", experience: "8 years" },
        { name: "Naomi Chebet", role: "Field Engineer", experience: "5 years" }
      ]
    },
    {
      id: "bid_010",
      job: {
        id: "job_110",
        title: "Swimming Pool Construction in Karen",
        description: "Construction of Olympic-sized swimming pool with filtration system.",
        customer: {
          name: "Karen Sports Club",
          location: "Karen, Nairobi",
          contact: "facilities@karensportsclub.com"
        }
      },
      status: "rejected",
      amount: 22500000,
      timeline_weeks: 14,
      proposal: "We propose a competition-standard 50m pool with 8 lanes, using the latest filtration technology. Includes starting blocks, lane markers, and ADA-compliant access. Construction uses high-quality materials for minimal maintenance.",
      created_at: "2023-07-05T10:15:00Z",
      bid_attachments: [
        { name: "Pool_Design.pdf", size: "4.8MB" },
        { name: "Technical_Specs.pdf", size: "3.5MB" }
      ],
      team: [
        { name: "Paul Gitonga", role: "Pool Specialist", experience: "9 years" },
        { name: "Rebecca Njeri", role: "Project Engineer", experience: "6 years" }
      ]
    },
    {
      id: "bid_011",
      job: {
        id: "job_111",
        title: "Office IT Infrastructure Setup",
        description: "Complete IT infrastructure setup for new office with 50 workstations.",
        customer: {
          name: "Fintech Innovations Ltd",
          location: "Upper Hill, Nairobi",
          contact: "it@fintechinnovations.africa"
        }
      },
      status: "accepted",
      amount: 12500000,
      timeline_weeks: 6,
      proposal: "Our solution includes high-speed networking, VoIP phone system, server setup, and workstation configuration. We provide 24/7 support with 2-hour response time. All equipment is enterprise-grade with 3-year warranty.",
      created_at: "2023-09-20T08:45:00Z",
      bid_attachments: [
        { name: "Network_Design.pdf", size: "3.7MB" },
        { name: "Equipment_List.pdf", size: "1.8MB" },
        { name: "Support_Agreement.pdf", size: "1.2MB" }
      ],
      team: [
        { name: "Kevin Maina", role: "IT Architect", experience: "7 years" },
        { name: "Sharon Wangeci", role: "Systems Engineer", experience: "5 years" }
      ]
    },
    {
      id: "bid_012",
      job: {
        id: "job_112",
        title: "Landscaping for Corporate Headquarters",
        description: "Complete landscaping and outdoor space design for new corporate campus.",
        customer: {
          name: "Pan African Holdings",
          location: "Westlands, Nairobi",
          contact: "facilities@paholdings.com"
        }
      },
      status: "pending",
      amount: 18500000,
      timeline_weeks: 10,
      proposal: "Our design incorporates native drought-resistant plants, water features, and outdoor meeting spaces. Includes irrigation system with rainwater harvesting. Maintenance program available for first year at discounted rate.",
      created_at: "2023-10-15T12:30:00Z",
      bid_attachments: [
        { name: "Landscape_Design.pdf", size: "7.2MB" },
        { name: "Plant_List.pdf", size: "2.1MB" }
      ],
      team: [
        { name: "Grace Mwende", role: "Landscape Architect", experience: "8 years" },
        { name: "Eric Onyango", role: "Horticulturist", experience: "6 years" }
      ]
    },
    {
      id: "bid_013",
      job: {
        id: "job_113",
        title: "Water Borehole Drilling in Isiolo",
        description: "Drilling and equipping of 200m deep water borehole for community use.",
        customer: {
          name: "Isiolo County Government",
          location: "Isiolo County",
          contact: "water@isiolocounty.go.ke"
        }
      },
      status: "accepted",
      amount: 8500000,
      timeline_weeks: 8,
      proposal: "We'll drill to estimated aquifer depth with casing and screen installation. Includes solar-powered submersible pump, storage tank, and community tap stands. Our team has extensive experience in arid regions with 98% success rate.",
      created_at: "2023-08-30T09:50:00Z",
      bid_attachments: [
        { name: "Geological_Report.pdf", size: "4.5MB" },
        { name: "Equipment_Specs.pdf", size: "2.8MB" },
        { name: "Community_Training.pdf", size: "1.5MB" }
      ],
      team: [
        { name: "Ahmed Abdi", role: "Hydrogeologist", experience: "10 years" },
        { name: "Lilian Wanjiku", role: "Project Manager", experience: "7 years" }
      ]
    }
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