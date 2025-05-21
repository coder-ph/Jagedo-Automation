import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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
    serviceType: '',
    jobBudget: '',
    materialDocuments: []
  });

  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [activeSection, setActiveSection] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    setIsUploading(true);
    setUploadProgress(0);
    
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    setTimeout(() => {
      setFormData(prev => ({
        ...prev,
        materialDocuments: [...prev.materialDocuments, ...files]
      }));
      clearInterval(interval);
      setIsUploading(false);
      toast.success(`${files.length} file(s) uploaded successfully!`);
    }, 2500);
  };

  const removeFile = (index) => {
    setFormData(prev => ({
      ...prev,
      materialDocuments: prev.materialDocuments.filter((_, i) => i !== index)
    }));
    toast.info('File removed');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    toast.success('Service request submitted successfully! Redirecting to dashboard...', {
      position: "top-center",
      autoClose: 2500,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "colored",
      onClose: () => navigate('/dashboard')
    });
    
    console.log('Service Request Submitted:', formData);
  };

  const toggleSection = (section) => {
    setActiveSection(activeSection === section ? null : section);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 pt-16">
      <ToastContainer 
        position="top-center"
        autoClose={2500}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white shadow-xl rounded-xl overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
            <h2 className="text-2xl sm:text-3xl font-bold">
              Create Service Request
            </h2>
            <p className="mt-2 opacity-90">
              Fill in the details below and we'll connect you with the right service provider
            </p>
          </div>

          <div className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Mobile Accordion Sections */}
              <div className="lg:hidden space-y-4">
                {/* Personal Information Section */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <button
                    type="button"
                    onClick={() => toggleSection('personal')}
                    className="w-full flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <h3 className="text-base font-medium text-gray-900">
                      Personal Information
                    </h3>
                    <svg
                      className={`h-5 w-5 text-gray-500 transform transition-transform ${activeSection === 'personal' ? 'rotate-180' : ''}`}
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                  {activeSection === 'personal' && (
                    <div className="p-4 space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                        <input
                          type="text"
                          name="fullName"
                          value={formData.fullName}
                          onChange={handleChange}
                          placeholder="John Doe"
                          required
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                        <input
                          type="tel"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          placeholder="0712 345 678"
                          required
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                        <input
                          type="email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          placeholder="your@email.com"
                          required
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Region</label>
                        <select
                          name="region"
                          value={formData.region}
                          onChange={handleChange}
                          required
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        >
                          <option value="">Select your region</option>
                          {regionsInKenya.map(region => (
                            <option key={region} value={region}>{region}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  )}
                </div>

                {/* Service Details Section */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <button
                    type="button"
                    onClick={() => toggleSection('service')}
                    className="w-full flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <h3 className="text-base font-medium text-gray-900">
                      Service Details
                    </h3>
                    <svg
                      className={`h-5 w-5 text-gray-500 transform transition-transform ${activeSection === 'service' ? 'rotate-180' : ''}`}
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                  {activeSection === 'service' && (
                    <div className="p-4 space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Location Details</label>
                        <textarea
                          name="locationDetails"
                          value={formData.locationDetails}
                          onChange={handleChange}
                          placeholder="Estate, house number, landmarks..."
                          rows={3}
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                          required
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Service Type</label>
                        <select
                          name="serviceType"
                          value={formData.serviceType}
                          onChange={handleChange}
                          required
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        >
                          <option value="">Select service type</option>
                          {serviceTypes.map(type => (
                            <option key={type} value={type}>{type}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Job Budget (Ksh)</label>
                        <div className="relative rounded-md shadow-sm">
                          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <span className="text-gray-500 text-sm">Ksh</span>
                          </div>
                          <input
                            type="number"
                            name="jobBudget"
                            value={formData.jobBudget}
                            onChange={handleChange}
                            placeholder="0.00"
                            required
                            min="0"
                            step="100"
                            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Additional Information Section */}
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <button
                    type="button"
                    onClick={() => toggleSection('additional')}
                    className="w-full flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <h3 className="text-base font-medium text-gray-900">
                      Additional Information
                    </h3>
                    <svg
                      className={`h-5 w-5 text-gray-500 transform transition-transform ${activeSection === 'additional' ? 'rotate-180' : ''}`}
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </button>
                  {activeSection === 'additional' && (
                    <div className="p-4 space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Service Description</label>
                        <textarea
                          name="serviceDescription"
                          value={formData.serviceDescription}
                          onChange={handleChange}
                          placeholder="Describe in detail what you need done..."
                          rows={4}
                          className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                          required
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Supporting Documents</label>
                        <div className="space-y-3">
                          <div className="relative group">
                            <div className="flex justify-center px-4 pt-6 pb-5 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-400 transition-colors duration-200 bg-gray-50 hover:bg-gray-100">
                              <div className="text-center">
                                <svg
                                  className="mx-auto h-10 w-10 text-gray-400 group-hover:text-indigo-500 transition-colors duration-200"
                                  stroke="currentColor"
                                  fill="none"
                                  viewBox="0 0 48 48"
                                  aria-hidden="true"
                                >
                                  <path
                                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                    strokeWidth={2}
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                  />
                                </svg>
                                <div className="mt-2 flex text-sm text-gray-600 justify-center">
                                  <label
                                    htmlFor="mobile-file-upload"
                                    className="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none"
                                  >
                                    <span>Upload files</span>
                                    <input
                                      id="mobile-file-upload"
                                      name="file-upload"
                                      type="file"
                                      multiple
                                      onChange={handleFileUpload}
                                      className="sr-only"
                                      accept="image/*,.pdf,.doc,.docx"
                                    />
                                  </label>
                                  <p className="pl-1">or drag and drop</p>
                                </div>
                                <p className="text-xs text-gray-500 mt-1">
                                  PNG, JPG, PDF, DOC (Max. 10MB each)
                                </p>
                              </div>
                            </div>
                          </div>

                          {isUploading && (
                            <div className="space-y-1">
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full" 
                                  style={{ width: `${uploadProgress}%` }}
                                ></div>
                              </div>
                              <p className="text-xs text-gray-500 text-right">
                                Uploading... {uploadProgress}%
                              </p>
                            </div>
                          )}

                          {formData.materialDocuments.length > 0 && (
                            <div className="space-y-2">
                              <h4 className="text-xs font-medium text-gray-700">Uploaded Files</h4>
                              <ul className="space-y-1">
                                {formData.materialDocuments.map((file, index) => (
                                  <li key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-md group hover:bg-gray-100 transition-colors duration-150">
                                    <div className="flex items-center space-x-2 truncate">
                                      <svg className="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                      </svg>
                                      <span className="text-xs text-gray-600 truncate">{file.name}</span>
                                    </div>
                                    <button
                                      type="button"
                                      onClick={() => removeFile(index)}
                                      className="text-gray-400 hover:text-red-500 transition-colors duration-200"
                                      aria-label="Remove file"
                                    >
                                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                      </svg>
                                    </button>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Desktop Layout */}
              <div className="hidden lg:grid grid-cols-3 gap-6">
                {/* Personal Details Column */}
                <div className="space-y-5">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                      Personal Information
                    </span>
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                      <input
                        type="text"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleChange}
                        placeholder="John Doe"
                        required
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                      <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        placeholder="0712 345 678"
                        required
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="your@email.com"
                        required
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Region</label>
                      <select
                        name="region"
                        value={formData.region}
                        onChange={handleChange}
                        required
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                      >
                        <option value="">Select your region</option>
                        {regionsInKenya.map(region => (
                          <option key={region} value={region}>{region}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>

                {/* Service Details Column */}
                <div className="space-y-5">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                      Service Details
                    </span>
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Location Details</label>
                      <textarea
                        name="locationDetails"
                        value={formData.locationDetails}
                        onChange={handleChange}
                        placeholder="Estate, house number, landmarks..."
                        rows={3}
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Service Type</label>
                      <select
                        name="serviceType"
                        value={formData.serviceType}
                        onChange={handleChange}
                        required
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                      >
                        <option value="">Select service type</option>
                        {serviceTypes.map(type => (
                          <option key={type} value={type}>{type}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Job Budget (Ksh)</label>
                      <div className="relative rounded-md shadow-sm">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <span className="text-gray-500 text-sm">Ksh</span>
                        </div>
                        <input
                          type="number"
                          name="jobBudget"
                          value={formData.jobBudget}
                          onChange={handleChange}
                          placeholder="0.00"
                          required
                          min="0"
                          step="100"
                          className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Additional Information Column */}
                <div className="space-y-5">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                      Additional Information
                    </span>
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Service Description</label>
                      <textarea
                        name="serviceDescription"
                        value={formData.serviceDescription}
                        onChange={handleChange}
                        placeholder="Describe in detail what you need done..."
                        rows={5}
                        className="w-full px-3 py-2 text-base border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Supporting Documents</label>
                      <div className="space-y-3">
                        <div className="relative group">
                          <div className="flex justify-center px-4 pt-6 pb-5 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-400 transition-colors duration-200 bg-gray-50 hover:bg-gray-100">
                            <div className="text-center">
                              <svg
                                className="mx-auto h-10 w-10 text-gray-400 group-hover:text-indigo-500 transition-colors duration-200"
                                stroke="currentColor"
                                fill="none"
                                viewBox="0 0 48 48"
                                aria-hidden="true"
                              >
                                <path
                                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                  strokeWidth={2}
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                />
                              </svg>
                              <div className="mt-2 flex text-sm text-gray-600 justify-center">
                                <label
                                  htmlFor="desktop-file-upload"
                                  className="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none"
                                >
                                  <span>Upload files</span>
                                  <input
                                    id="desktop-file-upload"
                                    name="file-upload"
                                    type="file"
                                    multiple
                                    onChange={handleFileUpload}
                                    className="sr-only"
                                    accept="image/*,.pdf,.doc,.docx"
                                  />
                                </label>
                                <p className="pl-1">or drag and drop</p>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                PNG, JPG, PDF, DOC (Max. 10MB each)
                              </p>
                            </div>
                          </div>
                        </div>

                        {isUploading && (
                          <div className="space-y-1">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full" 
                                style={{ width: `${uploadProgress}%` }}
                              ></div>
                            </div>
                            <p className="text-xs text-gray-500 text-right">
                              Uploading... {uploadProgress}%
                            </p>
                          </div>
                        )}

                        {formData.materialDocuments.length > 0 && (
                          <div className="space-y-2">
                            <h4 className="text-xs font-medium text-gray-700">Uploaded Files</h4>
                            <ul className="space-y-1">
                              {formData.materialDocuments.map((file, index) => (
                                <li key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-md group hover:bg-gray-100 transition-colors duration-150">
                                  <div className="flex items-center space-x-2 truncate">
                                    <svg className="h-4 w-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                    </svg>
                                    <span className="text-xs text-gray-600 truncate">{file.name}</span>
                                  </div>
                                  <button
                                    type="button"
                                    onClick={() => removeFile(index)}
                                    className="text-gray-400 hover:text-red-500 transition-colors duration-200"
                                    aria-label="Remove file"
                                  >
                                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                  </button>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Submit Service Request
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerServiceRequest;