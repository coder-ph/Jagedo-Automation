const Services = () => {
    const services = [
      {
        title: "Fundi Services",
        description: "Skilled craftsmanship and technical expertise for all your specialized needs.",
        icon: "🔧",
        features: [
          "Electrical Installations", 
          "Plumbing Solutions", 
          "Building Maintenance",
          "Equipment Repair"
        ]
      },
      {
        title: "Professional Services",
        description: "Expert consulting and advisory for your business growth.",
        icon: "👔",
        features: [
          "Business Consulting", 
          "Financial Advisory", 
          "Legal Services",
          "HR Solutions"
        ]
      },
      {
        title: "Hardware Solutions",
        description: "Quality tools, equipment and materials for all your projects.",
        icon: "🛠️",
        features: [
          "Construction Materials", 
          "Power Tools", 
          "Safety Equipment",
          "Industrial Supplies"
        ]
      },
      {
        title: "Contractor Services",
        description: "Comprehensive project management and execution.",
        icon: "🏗️",
        features: [
          "Construction Management", 
          "Renovation Services", 
          "Project Supervision",
          "Quality Assurance"
        ]
      }
    ];
  
    return (
      <div className="min-h-screen py-16">
        {/* Services Hero */}
        <section className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-20">
          <div className="container mx-auto px-6 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">Our Services</h1>
            <p className="text-xl max-w-2xl mx-auto">
              Comprehensive solutions for all your construction, professional and hardware needs.
            </p>
          </div>
        </section>
  
        {/* Services List */}
        <section className="py-20">
          <div className="container mx-auto px-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {services.map((service, index) => (
                <div key={index} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
                  <div className="p-6">
                    <div className="text-5xl mb-4">{service.icon}</div>
                    <h2 className="text-xl font-bold mb-3">{service.title}</h2>
                    <p className="text-gray-600 mb-4 text-sm">{service.description}</p>
                    <ul className="space-y-2 text-sm">
                      {service.features.map((feature, i) => (
                        <li key={i} className="flex items-start">
                          <span className="text-indigo-500 mr-2 mt-0.5">✓</span>
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="px-6 pb-6">
                    <button className="text-indigo-600 font-medium hover:text-indigo-800 transition duration-200 text-sm">
                      Learn More →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
  
        {/* Process Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-16">Our Work Process</h2>
            <div className="relative">
              <div className="hidden md:block absolute left-1/2 top-0 h-full w-1 bg-indigo-200 transform -translate-x-1/2"></div>
              {[
                { step: "1", title: "Consultation", desc: "We discuss your project requirements" },
                { step: "2", title: "Assessment", desc: "Detailed evaluation of your needs" },
                { step: "3", title: "Proposal", desc: "Customized solution and quote" },
                { step: "4", title: "Execution", desc: "Professional implementation" },
                { step: "5", title: "Completion", desc: "Final delivery and follow-up" }
              ].map((item, index) => (
                <div key={index} className={`flex ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'} items-center mb-16 last:mb-0`}>
                  <div className="md:w-1/2 mb-6 md:mb-0 md:px-10">
                    <div className="bg-white p-6 rounded-lg shadow-md">
                      <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                      <p className="text-gray-600">{item.desc}</p>
                    </div>
                  </div>
                  <div className="md:w-1/2 flex justify-center">
                    <div className="w-16 h-16 rounded-full bg-indigo-600 text-white flex items-center justify-center text-2xl font-bold">
                      {item.step}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    );
  };
  
  export default Services;