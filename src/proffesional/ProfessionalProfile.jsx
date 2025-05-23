// ProfessionalProfile.jsx
import React from 'react';
import ProfileHeader from './ProfileHeader';
import ProfileDetails from './ProfileDetails';
import PortfolioSection from './PortfolioSection';
import ReviewsSection from './ReviewsSection';

const ProfessionalProfile = () => {
  const profileData = {
    name: "John Doe",
    title: "Licensed Contractor",
    location: "Nairobi, Kenya",
    rating: 4.8,
    reviewCount: 42,
    bio: "With over 10 years of experience in home renovation and construction, I specialize in delivering high-quality work with attention to detail. My team and I are committed to completing projects on time and within budget.",
    services: ["Home Renovation", "Kitchen Remodeling", "Bathroom Remodeling", "Interior Design"],
    experience: "10+ years",
    certifications: ["Licensed Contractor (NCA)", "OSHA Certified"],
    portfolio: [
      { id: 1, title: "Modern Kitchen Remodel", image: "https://example.com/kitchen.jpg", description: "Complete kitchen renovation with custom cabinets" },
      { id: 2, title: "Bathroom Upgrade", image: "https://example.com/bathroom.jpg", description: "Luxury bathroom with walk-in shower" },
    ],
    reviews: [
      { id: 1, client: "Sarah Johnson", rating: 5, comment: "John did an amazing job on our kitchen remodel. Highly recommended!", date: "2023-06-15" },
      { id: 2, client: "Michael Brown", rating: 4, comment: "Quality work but took a bit longer than expected.", date: "2023-05-22" },
    ]
  };

  return (
    <div className="space-y-6">
      <ProfileHeader 
        name={profileData.name}
        title={profileData.title}
        location={profileData.location}
        rating={profileData.rating}
        reviewCount={profileData.reviewCount}
      />
      
      <ProfileDetails 
        bio={profileData.bio}
        services={profileData.services}
        experience={profileData.experience}
        certifications={profileData.certifications}
      />
      
      <PortfolioSection items={profileData.portfolio} />
      
      <ReviewsSection reviews={profileData.reviews} />
      
      <div className="flex justify-end">
        <button className="px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Edit Profile
        </button>
      </div>
    </div>
  );
};

export default ProfessionalProfile;