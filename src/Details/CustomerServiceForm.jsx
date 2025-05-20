import React, { useState } from 'react';

const CustomerServiceForm = () => {
  const [formData, setFormData] = useState({
    serviceName: '',
    description: '',
    materials: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    if (!formData.serviceName || !formData.description) {
      setError('Please fill in all required fields.');
      return;
    }

    // Simulate form submission
    console.log('Submitting service request:', formData);
    setMessage('Service request submitted successfully!');
    setError('');
    
    // Reset form
    setFormData({
      serviceName: '',
      description: '',
      materials: ''
    });
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md mt-10">
      <h2 className="text-2xl font-bold mb-4 text-indigo-700">Create a Service Request</h2>
      
      {message && (
        <div className="mb-4 text-green-600 font-medium bg-green-100 p-3 rounded">
          {message}
        </div>
      )}

      {error && (
        <div className="mb-4 text-red-600 font-medium bg-red-100 p-3 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700 font-medium mb-1">Service Name <span className="text-red-500">*</span></label>
          <input
            type="text"
            name="serviceName"
            value={formData.serviceName}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="e.g., Plumbing Repair"
            required
          />
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-1">Service Description <span className="text-red-500">*</span></label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Describe the issue or task in detail"
            required
          ></textarea>
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-1">Materials Needed (if any)</label>
          <textarea
            name="materials"
            value={formData.materials}
            onChange={handleChange}
            rows="2"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="List any tools or materials required"
          ></textarea>
        </div>

        <button
          type="submit"
          className="bg-indigo-600 text-white font-semibold px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
        >
          Submit Request
        </button>
      </form>
    </div>
  );
};

export default CustomerServiceForm;
