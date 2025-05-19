const About = () => {
    return (
      <div className="min-h-screen py-16">
        {/* About Hero */}
        <section className="bg-indigo-50 py-20">
          <div className="container mx-auto px-6 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 text-indigo-800">About Jagedo</h1>
            <p className="text-xl text-gray-700 max-w-3xl mx-auto">
              We're a team of passionate professionals dedicated to delivering exceptional services.
            </p>
          </div>
        </section>
  
        {/* Our Story */}
        <section className="py-20">
          <div className="container mx-auto px-6">
            <div className="flex flex-col md:flex-row items-center">
              <div className="md:w-1/2 mb-10 md:mb-0 md:pr-10">
                <h2 className="text-3xl font-bold mb-6">Our Story</h2>
                <p className="text-gray-700 mb-4">
                  Founded in 2015, Jagedo started as a small team with big dreams. Over the years, we've grown into a trusted partner for businesses across various industries.
                </p>
                <p className="text-gray-700 mb-4">
                  Our journey has been marked by innovation, dedication, and a commitment to excellence that has helped our clients achieve remarkable success.
                </p>
                <p className="text-gray-700">
                  Today, we continue to push boundaries and set new standards in our field.
                </p>
              </div>
              <div className="md:w-1/2 bg-gray-100 h-64 md:h-96 rounded-lg shadow-md">
                {/* Placeholder for company image */}
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  [Company Timeline/Image]
                </div>
              </div>
            </div>
          </div>
        </section>
  
        {/* Team Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-16">Meet Our Team</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { name: "Alex Johnson", role: "CEO & Founder", bio: "Visionary leader with 15+ years experience." },
                { name: "Sarah Williams", role: "CTO", bio: "Technology expert driving innovation." },
                { name: "Michael Chen", role: "Head of Operations", bio: "Ensures seamless service delivery." }
              ].map((member, index) => (
                <div key={index} className="bg-white p-6 rounded-lg shadow-md text-center">
                  <div className="w-32 h-32 mx-auto bg-gray-200 rounded-full mb-4 overflow-hidden">
                    {/* Placeholder for team member photo */}
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                      [Photo]
                    </div>
                  </div>
                  <h3 className="text-xl font-semibold mb-1">{member.name}</h3>
                  <p className="text-indigo-600 mb-3">{member.role}</p>
                  <p className="text-gray-600">{member.bio}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
  
        {/* Values Section */}
        <section className="py-20">
          <div className="container mx-auto px-6">
            <h2 className="text-3xl font-bold text-center mb-16">Our Core Values</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { title: "Integrity", desc: "We do what's right, not what's easy." },
                { title: "Innovation", desc: "Constantly pushing boundaries." },
                { title: "Excellence", desc: "Quality in everything we do." }
              ].map((value, index) => (
                <div key={index} className="bg-white p-6 rounded-lg shadow-md text-center border-t-4 border-indigo-500">
                  <h3 className="text-xl font-semibold mb-3">{value.title}</h3>
                  <p className="text-gray-600">{value.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    );
  };
  
  export default About;