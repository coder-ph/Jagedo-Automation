// StatCard.jsx
import React from 'react';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa';

const StatCard = ({ title, value, change, trend }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-sm font-medium text-gray-500">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
        <span className={`ml-2 flex items-center text-sm font-medium ${
          trend === 'up' ? 'text-green-600' : 'text-red-600'
        }`}>
          {trend === 'up' ? (
            <FaArrowUp className="h-4 w-4 mr-1" />
          ) : (
            <FaArrowDown className="h-4 w-4 mr-1" />
          )}
          {change}
        </span>
      </div>
    </div>
  );
};

export default StatCard;