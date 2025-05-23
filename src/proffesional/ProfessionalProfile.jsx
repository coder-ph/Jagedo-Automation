import React from 'react';
import PropTypes from 'prop-types';
import { 
  FaUserTie, FaBriefcase, FaStar, FaMapMarkerAlt, 
  FaCertificate, FaTools, FaRegClock, FaEnvelope,
  FaPhone, FaLinkedin, FaCheck, FaTimes
} from 'react-icons/fa';
import { GiSkills } from 'react-icons/gi';
import { RiMoneyDollarCircleLine } from 'react-icons/ri';

const ProfessionalProfile = () => {
  // Mock data for Kenyan professional
  const professional = {
    id: "prof_001",
    name: "James Kariuki",
    email: "james.kariuki@construction.co.ke",
    phone: "+254712345678",
    linkedin: "https://linkedin.com/in/jameskariuki",
    company_name: "Kariuki Construction Ltd",
    profile_description: "Licensed civil engineer with 12 years experience in residential and commercial construction across Nairobi and surrounding counties. Specialize in sustainable building practices and innovative construction techniques. Registered with NCA as a contractor (Level 8).",
    location: "Westlands, Nairobi",
    created_at: "2018-05-15T10:00:00Z",
    nca_level: 8,
    average_rating: 4.7,
    total_ratings: 23,
    successful_bids: 18,
    total_bids: 24,
    is_active: true,
    skills: [
      { certified: true, years_experience: 12, skill: { name: "Civil Engineering" } },
      { certified: true, years_experience: 8, skill: { name: "Project Management" } },
      { certified: false, years_experience: 5, skill: { name: "Green Building" } },
      { certified: true, years_experience: 10, skill: { name: "Structural Design" } }
    ],
    portfolio: [
      { id: 1, title: "Kilimani Apartments", type: "Residential" },
      { id: 2, title: "Upper Hill Office Tower", type: "Commercial" },
      { id: 3, title: "Kiambu County Roads", type: "Infrastructure" },
      { id: 4, title: "Mombasa Warehouse", type: "Industrial" }
    ]
  };

  // Calculate derived values
  const successRate = Math.round((professional.successful_bids / professional.total_bids) * 100);
  const memberSince = new Date(professional.created_at).getFullYear();
  const ratingText = professional.total_ratings > 0 
    ? `${professional.average_rating.toFixed(1)} (${professional.total_ratings} reviews)`
    : 'No ratings yet';

  // Stats cards
  const stats = [
    { icon: <FaBriefcase className="text-blue-500" size={20} />, label: 'Completed Projects', value: professional.successful_bids },
    { icon: <FaStar className="text-yellow-500" size={20} />, label: 'Average Rating', value: ratingText },
    { icon: <RiMoneyDollarCircleLine className="text-green-500" size={20} />, label: 'Success Rate', value: `${successRate}%` },
    { icon: <FaRegClock className="text-purple-500" size={20} />, label: 'Member Since', value: memberSince },
  ];

  // Verification items
  const verifications = [
    { name: 'Email Verified', verified: true },
    { name: 'ID Verified', verified: true },
    { name: 'Payment Verified', verified: true },
    { name: 'NCA Certified', verified: professional.nca_level >= 5 },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        {/* Cover Photo */}
        <div className="h-48 bg-gradient-to-r from-blue-600 to-indigo-700 relative">
          <div className="absolute bottom-4 right-4">
            <span className="px-3 py-1 bg-white text-indigo-700 rounded-full text-sm font-medium">
              {professional.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>

        {/* Profile Header */}
        <div className="px-6 pb-6 relative -mt-16">
          <div className="flex flex-col md:flex-row items-start md:items-end gap-6">
            {/* Avatar */}
            <div className="w-32 h-32 rounded-full border-4 border-white bg-white shadow-lg overflow-hidden flex items-center justify-center">
              <FaUserTie className="text-gray-400 text-6xl" />
            </div>

            {/* Profile Info */}
            <div className="flex-1">
              <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-800">{professional.name}</h1>
                  {professional.company_name && (
                    <p className="text-lg text-gray-600">{professional.company_name}</p>
                  )}
                  <div className="flex items-center mt-2 text-gray-600">
                    <FaMapMarkerAlt className="mr-2" />
                    <span>{professional.location}</span>
                  </div>
                </div>

                {/* Contact Info */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                    NCA Level {professional.nca_level}
                  </span>
                  <div className="flex gap-2">
                    <a href={`mailto:${professional.email}`} className="p-2 bg-indigo-100 text-indigo-600 rounded-full hover:bg-indigo-200 transition">
                      <FaEnvelope />
                    </a>
                    <a href={`tel:${professional.phone}`} className="p-2 bg-green-100 text-green-600 rounded-full hover:bg-green-200 transition">
                      <FaPhone />
                    </a>
                    {professional.linkedin && (
                      <a href={professional.linkedin} target="_blank" rel="noopener noreferrer" className="p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition">
                        <FaLinkedin />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 px-6 pb-6">
          {stats.map((stat, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg flex items-center gap-4 hover:shadow-sm transition">
              <div className="flex-shrink-0">{stat.icon}</div>
              <div>
                <p className="text-gray-500 text-sm">{stat.label}</p>
                <p className="text-xl font-semibold">{stat.value}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 px-6 pb-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* About Section */}
            <section className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FaUserTie className="text-indigo-600" />
                About Me
              </h2>
              <p className="text-gray-700 whitespace-pre-line">
                {professional.profile_description}
              </p>
            </section>

            {/* Skills Section */}
            <section className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <GiSkills className="text-indigo-600" />
                Skills & Expertise
              </h2>
              <div className="flex flex-wrap gap-2">
                {professional.skills?.length > 0 ? (
                  professional.skills.map((skill, index) => (
                    <span 
                      key={index} 
                      className="px-3 py-1 bg-blue-50 text-blue-800 rounded-full text-sm flex items-center gap-1 hover:bg-blue-100 transition"
                    >
                      {skill.certified && <FaCertificate className="text-yellow-500" />}
                      {skill.skill?.name || 'Unnamed Skill'}
                      {skill.years_experience && ` (${skill.years_experience} yrs)`}
                    </span>
                  ))
                ) : (
                  <p className="text-gray-500">No skills added yet.</p>
                )}
              </div>
            </section>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Verification Section */}
            <section className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FaCertificate className="text-indigo-600" />
                Verification
              </h2>
              <div className="space-y-3">
                {verifications.map((verification, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-gray-600">{verification.name}</span>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs ${
                      verification.verified 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {verification.verified ? (
                        <>
                          <FaCheck className="mr-1" /> Verified
                        </>
                      ) : (
                        <>
                          <FaTimes className="mr-1" /> Pending
                        </>
                      )}
                    </span>
                  </div>
                ))}
              </div>
            </section>

            {/* Portfolio Section */}
            <section className="bg-white rounded-lg p-6 shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FaBriefcase className="text-indigo-600" />
                Recent Projects
              </h2>
              <div className="grid grid-cols-2 gap-3">
                {professional.portfolio?.map((project) => (
                  <div 
                    key={project.id} 
                    className="aspect-square bg-gray-100 rounded-lg flex flex-col items-center justify-center p-2 text-center hover:bg-gray-200 transition cursor-pointer"
                  >
                    <FaTools size={24} className="text-gray-500 mb-2" />
                    <p className="text-sm font-medium text-gray-800">{project.title}</p>
                    <p className="text-xs text-gray-500">{project.type}</p>
                  </div>
                ))}
              </div>
              <button className="mt-4 w-full py-2 text-indigo-600 border border-indigo-600 rounded-lg hover:bg-indigo-50 transition flex items-center justify-center gap-2">
                View Full Portfolio
              </button>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalProfile;