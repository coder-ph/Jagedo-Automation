import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const regionsInKenya = [
  'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
  'Thika', 'Meru', 'Nyeri', 'Machakos', 'Garissa'
];

const serviceTypes = [
  'Fundi',
  'Professional',
  'Hardware',
  'Contractor'
];

const CustomerServiceRequest = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    email: '',
    region: '',
    locationDetails: '',
    serviceDescription: '',
    materialsNeeded: '',
    serviceType: '',
    jobRate: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Service Request Submitted:', formData);

    // Simulate successful submission then navigate to dashboard
    // You can replace this with your API call logic
    setTimeout(() => {
      navigate('/dashboard');
    }, 500);
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-10 flex flex-col md:flex-row gap-8">
      {/* Left section: Form */}
      <div className="flex-1">
        <h2 className="text-2xl font-bold mb-6 text-indigo-700">Create a Service Request</h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              placeholder="Full Name"
              required
              className="border border-gray-300 rounded-lg p-3 w-full"
            />
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Phone Number"
              required
              className="border border-gray-300 rounded-lg p-3 w-full"
            />
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email Address"
              required
              className="border border-gray-300 rounded-lg p-3 w-full"
            />
            <select
              name="region"
              value={formData.region}
              onChange={handleChange}
              required
              className="border border-gray-300 rounded-lg p-3 w-full bg-white"
            >
              <option value="">Select Your Region</option>
              {regionsInKenya.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
          </div>

          <textarea
            name="locationDetails"
            value={formData.locationDetails}
            onChange={handleChange}
            placeholder="Location Details (e.g., estate, house number)"
            rows={2}
            className="border border-gray-300 rounded-lg p-3 w-full"
            required
          />

          <textarea
            name="serviceDescription"
            value={formData.serviceDescription}
            onChange={handleChange}
            placeholder="Describe the service you need"
            rows={4}
            className="border border-gray-300 rounded-lg p-3 w-full"
            required
          />

          <textarea
            name="materialsNeeded"
            value={formData.materialsNeeded}
            onChange={handleChange}
            placeholder="List any materials or tools needed (optional)"
            rows={3}
            className="border border-gray-300 rounded-lg p-3 w-full"
          />

          {/* New: Service Type */}
          <select
            name="serviceType"
            value={formData.serviceType}
            onChange={handleChange}
            required
            className="border border-gray-300 rounded-lg p-3 w-full bg-white"
          >
            <option value="">Select Service Type</option>
            {serviceTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>

          {/* New: Job Rate */}
          <input
            type="number"
            name="jobRate"
            value={formData.jobRate}
            onChange={handleChange}
            placeholder="Job Rate in Ksh"
            required
            min="0"
            className="border border-gray-300 rounded-lg p-3 w-full"
          />

          <button
            type="submit"
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition"
          >
            Submit Request
          </button>
        </form>
      </div>

      {/* Right section: Info or image or anything else */}
      <div className="flex-1 bg-indigo-50 rounded-lg p-6 flex flex-col justify-center">
        <h3 className="text-xl font-semibold mb-4 text-indigo-700">Why Choose Our Services?</h3>
        <p className="text-gray-700 mb-4">
          Select the right professional for your job, specify your budget, and get quality service in your area.
        </p>
        <ul className="list-disc list-inside text-gray-600 space-y-2">
          <li>Trusted Fundis and Professionals</li>
          <li>Transparent Pricing</li>
          <li>Wide Coverage Across Kenya</li>
          <li>Quick and Reliable Support</li>
        </ul>
      </div>
    </div>
  );
};

export default CustomerServiceRequest;
