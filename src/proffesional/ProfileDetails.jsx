// ProfilePage.jsx
import React from 'react';
import ProfileDetails from './ProfileDetails';

const ProfilePage = () => {
  // Mock data for a professional profile (e.g., therapist, consultant, etc.)
  const profileData = {
    bio: "Licensed mental health professional with 8+ years of experience helping clients navigate anxiety, depression, and life transitions. I believe in a client-centered approach that empowers individuals to build resilience and achieve personal growth.",
    services: [
      "Individual Therapy",
      "Couples Counseling",
      "Anxiety Treatment",
      "Depression Therapy",
      "Trauma Therapy",
      "Life Coaching",
      "Stress Management"
    ],
    experience: "8 years of clinical experience across private practice and community mental health settings. Previously worked at Harborview Counseling Center and Sunrise Mental Health Clinic.",
    certifications: [
      "Licensed Clinical Social Worker (LCSW)",
      "Certified Cognitive Behavioral Therapist",
      "Trauma-Focused CBT Certification",
      "Gottman Method Couples Therapy (Level 1)",
      "Mindfulness-Based Stress Reduction Certification"
    ]
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Profile Sidebar */}
        <div className="md:w-1/3">
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="p-6 text-center">
              <div className="mx-auto h-32 w-32 rounded-full overflow-hidden bg-gray-200 mb-4">
                <img 
                  src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-1.2.1&auto=format&fit=crop&w=256&h=256&q=80" 
                  alt="Profile"
                  className="h-full w-full object-cover"
                />
              </div>
              <h1 className="text-xl font-bold text-gray-900">Dr. Sarah Johnson</h1>
              <p className="text-indigo-600">Clinical Psychologist</p>
              <div className="mt-4 flex justify-center space-x-4">
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition">
                  Contact
                </button>
                <button className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition">
                  Book Session
                </button>
              </div>
            </div>
            <div className="border-t border-gray-200 px-6 py-4">
              <h3 className="text-sm font-medium text-gray-900">Availability</h3>
              <p className="mt-1 text-sm text-gray-600">
                Mon-Fri: 9am - 5pm<br />
                Sat: 10am - 2pm<br />
                Online sessions available
              </p>
            </div>
          </div>
        </div>

        {/* Main Profile Content */}
        <div className="md:w-2/3">
          <ProfileDetails {...profileData} />
          
          {/* Additional Section - Testimonials */}
          <div className="bg-white shadow rounded-lg p-6 mt-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Client Testimonials</h2>
            <div className="space-y-4">
              <div className="border-l-4 border-indigo-200 pl-4 py-2">
                <p className="text-gray-600 italic">"Sarah helped me through one of the toughest periods of my life. Her approach is both professional and deeply compassionate."</p>
                <p className="text-sm text-gray-900 mt-1">— Michael T.</p>
              </div>
              <div className="border-l-4 border-indigo-200 pl-4 py-2">
                <p className="text-gray-600 italic">"The tools I learned in our sessions have made a lasting difference in how I manage stress and relationships."</p>
                <p className="text-sm text-gray-900 mt-1">— Jessica L.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;