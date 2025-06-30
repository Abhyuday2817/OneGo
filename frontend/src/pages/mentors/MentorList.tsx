
import React, { useState } from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import Avatar from '../../components/ui/Avatar';
import { useFetch } from '../../hooks/useFetch';

const MentorList: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const { data: mentors, loading } = useFetch('/api/mentors/');

  const categories = ['all', 'programming', 'design', 'business', 'marketing', 'languages'];

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-40 bg-gray-300 rounded mb-4"></div>
            <div className="h-4 bg-gray-300 rounded mb-2"></div>
            <div className="h-4 bg-gray-300 rounded w-3/4"></div>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-white mb-4">Find Your Perfect Mentor</h1>
        <p className="text-white/70">Connect with expert mentors to accelerate your learning journey</p>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="flex-1">
          <Input
            type="text"
            placeholder="Search mentors..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-white/10 border-white/20 text-white placeholder-white/50"
          />
        </div>
        <select 
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white"
        >
          {categories.map(category => (
            <option key={category} value={category} className="text-gray-900">
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Mentor Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Mock mentor data for now */}
        {[...Array(9)].map((_, index) => (
          <Card key={index} hover className="glass-effect">
            <div className="text-center mb-4">
              <Avatar
                name={`Mentor ${index + 1}`}
                size="xl"
                className="mx-auto mb-4"
              />
              <h3 className="text-xl font-bold text-white mb-1">
                John Mentor {index + 1}
              </h3>
              <p className="text-blue-400 text-sm">Full Stack Developer</p>
            </div>
            
            <div className="text-white/70 text-sm mb-4">
              <p>5+ years of experience in web development. Specialized in React, Node.js, and cloud technologies.</p>
            </div>
            
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-1">
                <span className="text-yellow-400">★</span>
                <span className="text-white">4.9</span>
                <span className="text-white/50">(124 reviews)</span>
              </div>
              <div className="text-white font-bold">
                $50/hr
              </div>
            </div>
            
            <div className="flex space-x-2">
              <Button variant="gradient" size="sm" className="flex-1">
                Book Session
              </Button>
              <Button variant="outline" size="sm" className="text-white border-white/30">
                View Profile
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default MentorList;
