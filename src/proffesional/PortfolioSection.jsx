// PortfolioSection.jsx
import React from 'react';

const PortfolioSection = ({ items }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Portfolio</h2>
      
      {items.length === 0 ? (
        <p className="text-gray-500">No portfolio items added yet</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {items.map((item) => (
            <div key={item.id} className="border rounded-lg overflow-hidden">
              <div className="h-48 bg-gray-200">
                {item.image ? (
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">
                    <span>No Image</span>
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-medium text-gray-900">{item.title}</h3>
                <p className="text-sm text-gray-600 mt-1">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-4">
        <button className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
          Add Portfolio Item +
        </button>
      </div>
    </div>
  );
};

export default PortfolioSection;