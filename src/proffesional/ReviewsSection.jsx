import React from 'react';
import { FaStar, FaQuoteLeft } from 'react-icons/fa';
import PropTypes from 'prop-types';

const mockReviews = [
  {
    id: 1,
    client: "Sarah Johnson",
    rating: 5,
    comment: "The team delivered exceptional results beyond our expectations. Their attention to detail and creative solutions made all the difference in our project.",
    date: "2023-06-15",
    avatar: "https://randomuser.me/api/portraits/women/44.jpg",
    role: "Marketing Director"
  },
  {
    id: 2,
    client: "Michael Chen",
    rating: 4,
    comment: "Professional service with great communication. The project was completed on time and met all our key requirements.",
    date: "2023-05-28",
    avatar: "https://randomuser.me/api/portraits/men/32.jpg",
    role: "CTO"
  },
  {
    id: 3,
    client: "Emma Rodriguez",
    rating: 5,
    comment: "Working with this team was a pleasure from start to finish. They understood our vision and brought it to life beautifully.",
    date: "2023-04-10",
    avatar: "https://randomuser.me/api/portraits/women/63.jpg",
    role: "Founder & CEO"
  }
];

const ReviewsSection = ({ reviews = mockReviews }) => {
  const averageRating = reviews.reduce((acc, review) => acc + review.rating, 0) / reviews.length;

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header with stats */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h2 className="text-2xl md:text-3xl font-bold">What Our Clients Say</h2>
            <p className="mt-2 opacity-90">Trusted by businesses worldwide</p>
          </div>
          <div className="flex flex-col items-center bg-white/10 backdrop-blur-sm rounded-xl p-4 min-w-[180px]">
            <div className="flex items-center mb-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <FaStar
                  key={star}
                  className={`h-5 w-5 ${star <= Math.round(averageRating) ? 'text-yellow-300' : 'text-white/30'}`}
                />
              ))}
            </div>
            <div className="text-3xl font-bold">{averageRating.toFixed(1)}</div>
            <div className="text-sm opacity-80">{reviews.length} {reviews.length === 1 ? 'Review' : 'Reviews'}</div>
          </div>
        </div>
      </div>

      {/* Reviews content */}
      <div className="p-6 md:p-8">
        {!reviews || reviews.length === 0 ? (
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-indigo-100 rounded-full mb-4">
              <FaQuoteLeft className="text-indigo-500 text-2xl" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">No reviews yet</h3>
            <p className="text-gray-500 mb-6">Be the first to share your experience</p>
            <button className="px-6 py-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors shadow-md">
              Leave a Review
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {reviews.map((review) => (
              <div 
                key={review.id} 
                className="bg-gray-50 hover:bg-white transition-all duration-300 rounded-xl p-6 shadow-sm hover:shadow-md border border-gray-100"
              >
                <div className="flex items-start mb-4">
                  <img 
                    src={review.avatar} 
                    alt={review.client} 
                    className="h-12 w-12 rounded-full object-cover mr-4 border-2 border-white shadow"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = 'https://www.gravatar.com/avatar/default?s=200&d=mp';
                    }}
                  />
                  <div>
                    <h3 className="font-semibold text-gray-900">{review.client}</h3>
                    <p className="text-sm text-indigo-600">{review.role}</p>
                  </div>
                  <div className="ml-auto flex items-center bg-white px-3 py-1 rounded-full shadow-sm">
                    <span className="text-yellow-500 font-medium mr-1">{review.rating}</span>
                    <FaStar className="h-4 w-4 text-yellow-400" />
                  </div>
                </div>
                
                <div className="relative mb-4">
                  <FaQuoteLeft className="absolute -top-2 left-0 text-gray-200 text-3xl -z-10" />
                  <p className="text-gray-600 pl-6 relative z-10 italic">
                    {review.comment}
                  </p>
                </div>
                
                <div className="text-sm text-gray-400">
                  {new Date(review.date).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* CTA Footer */}
      <div className="bg-gray-50 border-t border-gray-200 p-6 text-center">
        <h3 className="text-lg font-medium text-gray-800 mb-2">Ready to share your experience?</h3>
        <button className="px-6 py-2 bg-white border border-indigo-600 text-indigo-600 rounded-full hover:bg-indigo-50 transition-colors shadow-sm inline-flex items-center">
          Write a Review
          <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </button>
      </div>
    </div>
  );
};

ReviewsSection.propTypes = {
  reviews: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      client: PropTypes.string,
      rating: PropTypes.number,
      comment: PropTypes.string,
      date: PropTypes.string,
      avatar: PropTypes.string,
      role: PropTypes.string
    })
  ),
};

ReviewsSection.defaultProps = {
  reviews: mockReviews,
};

export default ReviewsSection;