import { Link } from 'react-router-dom';

const Home = () => {
  // Using a high-quality business/tech image from Unsplash
  const heroImage = "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80";

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-r from-indigo-500 to-blue-600 text-white py-20">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">Innovative Solutions for Your Business</h1>
            <p className="text-xl mb-8">Jagedo provides cutting-edge services to help your business grow in the digital age.</p>
            <div className="flex space-x-4">
              <Link to="/services" className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition duration-300">
                Our Services
              </Link>
              <Link to="/contact" className="border-2 border-white text-white px-6 py-3 rounded-lg font-medium hover:bg-white hover:text-indigo-600 transition duration-300">
                Contact Us
              </Link>
            </div>
          </div>
          <div className="md:w-1/2">
            <img 
              src={heroImage} 
              alt="Business team working together" 
              className="rounded-lg shadow-2xl object-cover h-full max-h-[400px] w-full"
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-16">Why Choose Jagedo</h2>
          <div className="grid md:grid-cols-3 gap-10">
            {[
              { title: "Expert Team", desc: "Our professionals have years of industry experience.", icon: "👨‍💼" },
              { title: "Custom Solutions", desc: "Tailored services to meet your specific needs.", icon: "🛠️" },
              { title: "Proven Results", desc: "Track record of successful implementations.", icon: "📈" }
            ].map((feature, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-indigo-700 text-white">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Transform Your Business?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">Let's discuss how we can help you achieve your goals.</p>
          <Link to="/contact" className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition duration-300 inline-block">
            Get Started
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;