// ReviewsSection.jsx
import React from 'react';
import { FaStar } from 'react-icons/fa';

const ReviewsSection = ({ reviews }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Client Reviews</h2>
      
      {reviews.length === 0 ? (
        <p className="text-gray-500">No reviews yet</p>
      ) : (
        <div className="space-y-6">
          {reviews.map((review) => (
            <div key={review.id} className="border-b border-gray-200 pb-6 last:border-0 last:pb-0">
              <div className="flex items-center justify-between">
                <h3 className="font-medium text-gray-900">{review.client}</h3>
                <div className="flex items-center">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <FaStar
                      key={star}
                      className={`h-4 w-4 ${star <= review.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                    />
                  ))}
                </div>
              </div>
              <p className="text-gray-600 mt-1">{review.comment}</p>
              <p className="text-sm text-gray-500 mt-2">{review.date}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReviewsSection;