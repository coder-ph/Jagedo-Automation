import React from 'react';

const HeroSection = () => {
  const categories = [
    {
      name: 'Fundi',
      description: 'Skilled craftsmen for all your repair needs',
      image: '/images/fundi.webp',
      bgColor: 'bg-blue-50'
    },
    {
      name: 'Professional',
      description: 'Certified experts for specialized projects',
      image: '/images/professional.webp',
      bgColor: 'bg-green-50'
    },
    {
      name: 'Hardware',
      description: 'Quality materials and supplies',
      image: '/images/hardware.webp',
      bgColor: 'bg-orange-50'
    },
    {
      name: 'Contractor',
      description: 'Full-service construction professionals',
      image: '/images/contractor.webp',
      bgColor: 'bg-purple-50'
    }
  ];

  return (
    <section className="relative bg-gradient-to-br from-indigo-50 to-gray-50 py-16 sm:py-24">
      {/* Background pattern */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-0 top-0 h-full w-1/3 bg-gradient-to-r from-white to-transparent"></div>
        <div className="absolute right-0 top-0 h-full w-1/3 bg-gradient-to-l from-white to-transparent"></div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        {/* Hero content */}
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            <span className="block">Construct with a</span>
            <span className="relative inline-block">
              <span className="relative z-10">Builder near you!</span>
              <span className="absolute bottom-2 left-0 w-full h-3 bg-indigo-200/70 -z-0"></span>
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Connect with trusted construction professionals and suppliers in your area
          </p>
        </div>

        {/* Category cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category, index) => (
            <div 
              key={index}
              className={`relative group overflow-hidden rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 ${category.bgColor}`}
            >
              <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent z-10"></div>
              <img 
                src={category.image} 
                alt={category.name}
                className="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute bottom-0 left-0 p-6 z-20 w-full">
                <h3 className="text-2xl font-bold text-white mb-1">{category.name}</h3>
                <p className="text-white/90">{category.description}</p>
                <button className="mt-3 px-4 py-2 bg-white text-indigo-600 rounded-lg text-sm font-medium hover:bg-indigo-50 transition-colors duration-200">
                  Find {category.name}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Stats bar */}
        <div className="mt-16 bg-white rounded-xl shadow-md p-6 max-w-4xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-indigo-600">5,000+</div>
              <div className="text-gray-600">Active Professionals</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600">98%</div>
              <div className="text-gray-600">Satisfaction Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600">10K+</div>
              <div className="text-gray-600">Completed Projects</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-indigo-600">24/7</div>
              <div className="text-gray-600">Support Available</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;