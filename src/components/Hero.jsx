import React from 'react';

const HeroSection = () => {
  const categories = [
    {
      name: 'Fundi',
      description: 'Skilled craftsmen for all your repair needs',
      image: '/images/Wrench.webp', // Removed 'public' from path
      colorClass: 'from-blue-500 to-blue-600'
    },
    {
      name: 'Professional',
      description: 'Certified experts for specialized projects',
      image: '/images/Reflector.webp',
      colorClass: 'from-green-500 to-green-600'
    },
    {
      name: 'Hardware',
      description: 'Quality materials and supplies',
      image: '/images/Toolbox.webp',
      colorClass: 'from-orange-500 to-orange-600'
    },
    {
      name: 'Contractor',
      description: 'Full-service construction professionals',
      image: '/images/Helmet.webp',
      colorClass: 'from-purple-500 to-purple-600'
    }
  ];

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-purple-300 to-white py-16 sm:py-24">
      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-full h-full opacity-10">
        <div className="absolute top-20 left-10 w-40 h-40 rounded-full bg-indigo-300 mix-blend-multiply filter blur-xl animate-float"></div>
        <div className="absolute top-1/3 right-20 w-32 h-32 rounded-full bg-blue-300 mix-blend-multiply filter blur-xl animate-float-delay"></div>
        <div className="absolute bottom-20 left-1/4 w-48 h-48 rounded-full bg-purple-300 mix-blend-multiply filter blur-xl animate-float"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Hero content */}
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            <span className="block mb-2">Construct with a</span>
            <span className="relative inline-block">
              <span className="relative z-10 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                Builder near you!
              </span>
              <span className="absolute bottom-2 left-0 w-full h-3 bg-indigo-200/70 -z-0 rounded-full"></span>
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Connect with trusted construction professionals and suppliers in your area
          </p>
        </div>

        {/* Category cards - Updated layout */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {categories.map((category, index) => (
            <div 
              key={index}
              className="relative group overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 bg-white"
            >
              {/* Image container with reduced height */}
              <div className="h-48 overflow-hidden">
                <img 
                  src={category.image} 
                  alt={category.name}
                  className="w-full h-full object-cover transition-all duration-500 group-hover:scale-105"
                  onError={(e) => {
                    e.target.onerror = null; 
                    e.target.src = '/images/placeholder.webp';
                  }}
                />
              </div>
              
              {/* Content container with better contrast */}
              <div className={`p-6 bg-gradient-to-br ${category.colorClass} text-white`}>
                <h3 className="text-2xl font-bold mb-2">{category.name}</h3>
                <p className="mb-4 opacity-90">{category.description}</p>
                <button className={`px-5 py-2 bg-white text-gray-800 rounded-full text-sm font-semibold hover:bg-gray-100 transition-colors duration-300 shadow-md hover:shadow-lg`}>
                  Find {category.name}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <style jsx global>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
        .animate-float { animation: float 6s ease-in-out infinite; }
        .animate-float-delay { animation: float 6s ease-in-out 1s infinite; }
      `}</style>
    </section>
  );
};

export default HeroSection;