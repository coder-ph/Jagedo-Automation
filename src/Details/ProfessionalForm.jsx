import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  FaFileUpload, 
  FaFileAlt, 
  FaMoneyBillWave, 
  FaClock, 
  FaMapMarkerAlt, 
  FaUserTie, 
  FaCertificate, 
  FaBriefcase, 
  FaStar 
} from 'react-icons/fa';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ProfessionalForm = () => {
  const { requestId } = useParams();
  const navigate = useNavigate();
  
  // Tender details state
  const [tenderDetails, setTenderDetails] = useState({
    id: requestId,
    title: "Home Renovation Project",
    description: "Complete home renovation including kitchen remodeling, bathroom upgrades, and living room redesign.",
    customerName: "John Mwangi",
    location: "Kileleshwa, Nairobi",
    budget: "Ksh 1,200,000",
    deadline: "2023-08-15",
    postedDate: "2023-07-20",
    serviceType: "Contractor",
    attachments: ["floor_plan.pdf", "design_specs.docx"]
  });

  // Bid form state
  const [bidData, setBidData] = useState({
    proposedAmount: '',
    timeline: '',
    proposalDetails: '',
    qualifications: [],
    portfolioItems: [],
    references: [],
    termsAccepted: false
  });

  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState('proposal');

  // Format file size utility function
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setBidData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  // Handle file uploads
  const handleFileUpload = (e, field) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;
    
    setIsUploading(true);
    setUploadProgress(0);
    
    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    // Process files after upload simulation
    setTimeout(() => {
      setBidData(prev => ({
        ...prev,
        [field]: [
          ...prev[field],
          ...files.map(file => ({
            name: file.name,
            size: file.size,
            type: file.type,
            preview: URL.createObjectURL(file)
          }))
        ]
      }));
      clearInterval(interval);
      setIsUploading(false);
      toast.success(`${files.length} file(s) uploaded successfully!`);
    }, 2500);
  };

  // Remove uploaded file
  const removeFile = (field, index) => {
    setBidData(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index)
    }));
    toast.info('File removed');
  };

  // Form submission handler
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validation
    if (!bidData.proposedAmount || !bidData.timeline || !bidData.proposalDetails) {
      toast.error('Please fill in all required fields');
      return;
    }
    
    if (!bidData.termsAccepted) {
      toast.error('You must accept the terms and conditions');
      return;
    }
    
    // Submit logic
    console.log('Bid submitted:', { requestId, ...bidData });
    
    toast.success('Bid submitted successfully!', {
      position: "top-center",
      autoClose: 3000,
      onClose: () => navigate('/professional-dashboard')
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <ToastContainer position="top-center" autoClose={3000} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb Navigation */}
        <nav className="flex mb-6" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-4">
            <li>
              <a href="/professional-dashboard" className="text-gray-400 hover:text-gray-500">
                <svg className="flex-shrink-0 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
              </a>
            </li>
            <li>
              <div className="flex items-center">
                <svg className="flex-shrink-0 h-5 w-5 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                </svg>
                <a href="/professional-dashboard/opportunities" className="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700">Opportunities</a>
              </div>
            </li>
            <li>
              <div className="flex items-center">
                <svg className="flex-shrink-0 h-5 w-5 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5.555 17.776l8-16 .894.448-8 16-.894-.448z" />
                </svg>
                <span className="ml-4 text-sm font-medium text-gray-500">Submit Bid</span>
              </div>
            </li>
          </ol>
        </nav>

        {/* Main Form Container */}
        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          {/* Tender Header Section */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-white">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between">
              <div>
                <h1 className="text-2xl font-bold">{tenderDetails.title}</h1>
                <p className="mt-2 opacity-90">{tenderDetails.description}</p>
                <div className="mt-4 flex flex-wrap gap-4">
                  <div className="flex items-center">
                    <FaMoneyBillWave className="mr-2" />
                    <span>Budget: {tenderDetails.budget}</span>
                  </div>
                  <div className="flex items-center">
                    <FaClock className="mr-2" />
                    <span>Deadline: {tenderDetails.deadline}</span>
                  </div>
                  <div className="flex items-center">
                    <FaMapMarkerAlt className="mr-2" />
                    <span>{tenderDetails.location}</span>
                  </div>
                </div>
              </div>
              <div className="mt-4 md:mt-0">
                <div className="bg-white/20 p-3 rounded-lg">
                  <p className="text-sm">Posted by: {tenderDetails.customerName}</p>
                  <p className="text-sm mt-1">Posted on: {tenderDetails.postedDate}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Form Content */}
          <div className="p-6">
            {/* Form Tabs */}
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                {['proposal', 'qualifications', 'attachments'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab 
                        ? 'border-indigo-500 text-indigo-600' 
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)} Details
                  </button>
                ))}
              </nav>
            </div>

            {/* Form Sections */}
            <form onSubmit={handleSubmit} className="mt-6">
              {activeTab === 'proposal' && (
                <ProposalSection bidData={bidData} handleChange={handleChange} />
              )}

              {activeTab === 'qualifications' && (
                <QualificationsSection 
                  bidData={bidData}
                  isUploading={isUploading}
                  uploadProgress={uploadProgress}
                  handleFileUpload={handleFileUpload}
                  removeFile={removeFile}
                  formatFileSize={formatFileSize}
                />
              )}

              {activeTab === 'attachments' && (
                <AttachmentsSection tenderDetails={tenderDetails} />
              )}

              {/* Form Footer */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <TermsCheckbox 
                  termsAccepted={bidData.termsAccepted}
                  handleChange={handleChange}
                />
                
                <div className="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => navigate(-1)}
                    className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Submit Bid
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

// Sub-components for better organization
const ProposalSection = ({ bidData, handleChange }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Proposed Amount (Ksh)
        </label>
        <div className="relative rounded-md shadow-sm">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span className="text-gray-500">Ksh</span>
          </div>
          <input
            type="number"
            name="proposedAmount"
            value={bidData.proposedAmount}
            onChange={handleChange}
            placeholder="Enter your proposed amount"
            className="block w-full pl-12 pr-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Proposed Timeline (Days)
        </label>
        <input
          type="number"
          name="timeline"
          value={bidData.timeline}
          onChange={handleChange}
          placeholder="Estimated days to complete"
          className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          required
        />
      </div>
    </div>
    
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Detailed Proposal
      </label>
      <textarea
        name="proposalDetails"
        value={bidData.proposalDetails}
        onChange={handleChange}
        rows={8}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
        placeholder="Describe your approach to this project..."
        required
      />
    </div>
  </div>
);

const QualificationsSection = ({ 
  bidData, 
  isUploading, 
  uploadProgress, 
  handleFileUpload, 
  removeFile, 
  formatFileSize 
}) => (
  <div className="space-y-6">
    <UploadSection 
      title="Professional Qualifications"
      icon={<FaUserTie className="mr-2 text-indigo-600" />}
      field="qualifications"
      description="Certificates, licenses, diplomas (PDF, DOC, JPG up to 10MB each)"
      bidData={bidData}
      isUploading={isUploading}
      uploadProgress={uploadProgress}
      handleFileUpload={handleFileUpload}
      removeFile={removeFile}
      formatFileSize={formatFileSize}
    />

    <UploadSection 
      title="Portfolio Items"
      icon={<FaBriefcase className="mr-2 text-indigo-600" />}
      field="portfolioItems"
      description="Images or documents of previous work (PDF, JPG up to 10MB each)"
      bidData={bidData}
      isUploading={isUploading}
      uploadProgress={uploadProgress}
      handleFileUpload={handleFileUpload}
      removeFile={removeFile}
      formatFileSize={formatFileSize}
      isImagePreview
    />

    <UploadSection 
      title="References"
      icon={<FaStar className="mr-2 text-indigo-600" />}
      field="references"
      description="Client references or testimonials (PDF, DOC up to 10MB each)"
      bidData={bidData}
      isUploading={isUploading}
      uploadProgress={uploadProgress}
      handleFileUpload={handleFileUpload}
      removeFile={removeFile}
      formatFileSize={formatFileSize}
    />
  </div>
);

const UploadSection = ({
  title,
  icon,
  field,
  description,
  bidData,
  isUploading,
  uploadProgress,
  handleFileUpload,
  removeFile,
  formatFileSize,
  isImagePreview = false
}) => (
  <div>
    <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
      {icon}
      {title}
    </h3>
    <div className="space-y-4">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <div className="flex justify-center">
          <FaFileUpload className="h-10 w-10 text-gray-400" />
        </div>
        <div className="mt-2 flex text-sm text-gray-600 justify-center">
          <label className="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500">
            <span>Upload {title.toLowerCase()}</span>
            <input
              type="file"
              multiple
              onChange={(e) => handleFileUpload(e, field)}
              className="sr-only"
              accept={isImagePreview ? ".pdf,.doc,.docx,.jpg,.png" : ".pdf,.doc,.docx"}
            />
          </label>
          <p className="pl-1">or drag and drop</p>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {description}
        </p>
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

      {bidData[field].length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-700">Uploaded {title}</h4>
          {isImagePreview ? (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {bidData[field].map((file, index) => (
                <div key={index} className="relative group">
                  {file.type.startsWith('image/') ? (
                    <img
                      src={file.preview}
                      alt={file.name}
                      className="h-32 w-full object-cover rounded-md"
                    />
                  ) : (
                    <div className="h-32 bg-gray-100 rounded-md flex flex-col items-center justify-center p-2">
                      <FaFileAlt className="h-8 w-8 text-gray-400" />
                      <p className="mt-2 text-xs text-gray-700 text-center truncate w-full">{file.name}</p>
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => removeFile(field, index)}
                    className="absolute top-1 right-1 bg-white/80 rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <svg className="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <ul className="space-y-2">
              {bidData[field].map((file, index) => (
                <li key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div className="flex items-center space-x-3">
                    <FaFileAlt className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-700 truncate">{file.name}</p>
                      <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(field, index)}
                    className="text-gray-400 hover:text-red-500"
                  >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  </div>
);

const AttachmentsSection = ({ tenderDetails }) => (
  <div className="space-y-6">
    <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
      <FaFileAlt className="mr-2 text-indigo-600" />
      Tender Documents
    </h3>
    <p className="text-gray-600">
      Review all attached documents from the customer before submitting your bid.
    </p>
    
    <div className="space-y-2">
      {tenderDetails.attachments.map((file, index) => (
        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
          <div className="flex items-center space-x-3">
            <FaFileAlt className="h-5 w-5 text-gray-400" />
            <div>
              <p className="text-sm font-medium text-gray-700">{file}</p>
              <p className="text-xs text-gray-500">PDF Document</p>
            </div>
          </div>
          <button
            type="button"
            className="text-indigo-600 hover:text-indigo-800 font-medium text-sm"
          >
            Download
          </button>
        </div>
      ))}
    </div>
  </div>
);

const TermsCheckbox = ({ termsAccepted, handleChange }) => (
  <div className="flex items-start">
    <div className="flex items-center h-5">
      <input
        id="terms"
        name="termsAccepted"
        type="checkbox"
        checked={termsAccepted}
        onChange={handleChange}
        className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
        required
      />
    </div>
    <div className="ml-3 text-sm">
      <label htmlFor="terms" className="font-medium text-gray-700">
        I agree to the terms and conditions
      </label>
      <p className="text-gray-500">
        By submitting this bid, I confirm that all information provided is accurate.
      </p>
    </div>
  </div>
);

export default ProfessionalForm;