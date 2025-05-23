import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';

const PortfolioSection = ({ items: initialItems = [], onItemsChange }) => {
  const [items, setItems] = useState(initialItems);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    image: '',
    imageFile: null
  });
  const [previewImage, setPreviewImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewImage(reader.result);
      };
      reader.readAsDataURL(file);
      setFormData(prev => ({ ...prev, imageFile: file }));
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const openAddModal = () => {
    setCurrentItem(null);
    setFormData({ title: '', description: '', image: '', imageFile: null });
    setPreviewImage(null);
    setIsModalOpen(true);
  };

  const openEditModal = (item) => {
    setCurrentItem(item);
    setFormData({
      title: item.title,
      description: item.description,
      image: item.image,
      imageFile: null
    });
    setPreviewImage(item.image || null);
    setIsModalOpen(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // In a real app, you would upload the image file to a server here
    // For this example, we'll use either the uploaded file or the image URL
    const imageToUse = formData.imageFile ? URL.createObjectURL(formData.imageFile) : formData.image;

    if (currentItem) {
      // Update existing item
      const updatedItems = items.map(item => 
        item.id === currentItem.id ? { 
          ...item, 
          title: formData.title,
          description: formData.description,
          image: imageToUse
        } : item
      );
      setItems(updatedItems);
      if (onItemsChange) onItemsChange(updatedItems);
    } else {
      // Add new item
      const newItem = {
        id: Date.now(),
        title: formData.title,
        description: formData.description,
        image: imageToUse
      };
      const updatedItems = [...items, newItem];
      setItems(updatedItems);
      if (onItemsChange) onItemsChange(updatedItems);
    }
    setIsModalOpen(false);
  };

  const handleDelete = (id) => {
    const updatedItems = items.filter(item => item.id !== id);
    setItems(updatedItems);
    if (onItemsChange) onItemsChange(updatedItems);
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Portfolio</h2>
      
      {items.length === 0 ? (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900">No portfolio items</h3>
          <p className="mt-1 text-gray-500">Get started by adding your first project.</p>
          <div className="mt-6">
            <button
              onClick={openAddModal}
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Project
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {items.map((item) => (
            <div key={item.id} className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300 relative group">
              <div className="relative h-56 bg-gray-100">
                {item.image ? (
                  <img
                    src={item.image}
                    alt={item.title || 'Portfolio item'}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null; 
                      e.target.src = '';
                      e.target.parentElement.classList.add('flex', 'items-center', 'justify-center', 'bg-gray-200');
                    }}
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gray-200 text-gray-400">
                    <svg className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                )}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <button 
                    onClick={() => openEditModal(item)}
                    className="m-2 p-2 bg-white bg-opacity-80 rounded-full hover:bg-opacity-100 transition-all"
                    title="Edit"
                  >
                    <svg className="h-5 w-5 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button 
                    onClick={() => handleDelete(item.id)}
                    className="m-2 p-2 bg-white bg-opacity-80 rounded-full hover:bg-opacity-100 transition-all"
                    title="Delete"
                  >
                    <svg className="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg text-gray-900 mb-1">
                  {item.title || 'Untitled Project'}
                </h3>
                <p className="text-sm text-gray-600 line-clamp-2">
                  {item.description || 'No description available'}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {items.length > 0 && (
        <div className="mt-6 text-center">
          <button
            onClick={openAddModal}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            Add New Project
          </button>
        </div>
      )}

      {/* Modal for Add/Edit */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium mb-4">
              {currentItem ? 'Edit Project' : 'Add New Project'}
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Project Title*</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  required
                  placeholder="My Awesome Project"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  rows="3"
                  placeholder="Describe your project..."
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Project Image</label>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  className="hidden"
                />
                <div className="flex items-center space-x-4">
                  <button
                    type="button"
                    onClick={triggerFileInput}
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                  >
                    Upload Image
                  </button>
                  <span className="text-sm text-gray-500">or</span>
                  <input
                    type="text"
                    name="image"
                    value={formData.image}
                    onChange={handleInputChange}
                    className="flex-1 p-2 border rounded focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Paste image URL"
                  />
                </div>
                {(previewImage || formData.image) && (
                  <div className="mt-2">
                    <div className="relative h-40 w-full bg-gray-100 rounded overflow-hidden">
                      <img
                        src={previewImage || formData.image}
                        alt="Preview"
                        className="h-full w-full object-contain"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = '';
                          e.target.parentElement.classList.add('flex', 'items-center', 'justify-center');
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded hover:bg-indigo-700"
                >
                  {currentItem ? 'Update' : 'Add'} Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

PortfolioSection.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      title: PropTypes.string,
      description: PropTypes.string,
      image: PropTypes.string,
    })
  ),
  onItemsChange: PropTypes.func,
};

PortfolioSection.defaultProps = {
  items: [],
  onItemsChange: null,
};

export default PortfolioSection;