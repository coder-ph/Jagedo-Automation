import React from 'react';

const HeroSection = () => {
  const categories = [
    {
      name: 'Fundi',
      description: 'Skilled craftsmen for all your repair needs',
      image: '/images/Wrench.webp',
    },
    {
      name: 'Professional',
      description: 'Certified experts for specialized projects',
      image: '/images/Reflector.webp',
    },
    {
      name: 'Hardware',
      description: 'Quality materials and supplies',
      image: '/images/Toolbox.webp',
    },
    {
      name: 'Contractor',
      description: 'Full-service construction professionals',
      image: '/images/Helmet.webp',
    }
  ];

  return (
    <section className="relative bg-gradient-to-br from-purple-200 to-white py-16 sm:py-24 overflow-hidden">
      {/* Decorative Blobs */}
      <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 bg-indigo-300 rounded-full filter blur-3xl animate-float"></div>
        <div className="absolute top-1/3 right-20 w-28 h-28 bg-blue-300 rounded-full filter blur-3xl animate-float-delay"></div>
        <div className="absolute bottom-20 left-1/4 w-36 h-36 bg-purple-300 rounded-full filter blur-3xl animate-float"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Heading */}
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900">
            <span className="block mb-2">Construct with a</span>
            <span className="relative inline-block">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 z-10 relative">
                Builder near you!
              </span>
              <span className="absolute bottom-1 left-0 w-full h-2 bg-indigo-200/60 rounded-full -z-0"></span>
            </span>
          </h1>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto">
            Connect with trusted construction professionals and suppliers in your area
          </p>
        </div>

        {/* Improved Landscape Cards with Better Alignment */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {categories.map((category, index) => (
            <div
              key={index}
              className="flex bg-white shadow-md hover:shadow-lg rounded-xl overflow-hidden transition-all duration-300 h-44"
            >
              {/* Image Section */}
              <div className="w-28 h-full flex-shrink-0 relative">
                <img
                  src={category.image}
                  alt={category.name}
                  className="w-full h-full object-cover"
                />
                {/* Gradient overlay for better text contrast */}
                <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-white/30"></div>
              </div>

              {/* Text Content Section - Centered vertically */}
              <div className="flex flex-col justify-center p-4 flex-grow">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">{category.name}</h3>
                  <p className="text-sm text-gray-600 leading-tight">{category.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Floating animation keyframes */}
      <style jsx global>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        .animate-float-delay {
          animation: float 6s ease-in-out 1s infinite;
        }
      `}</style>
    </section>
  );
};

export default HeroSection;