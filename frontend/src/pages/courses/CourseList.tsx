
import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const CourseList: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-white mb-4">Explore Courses</h1>
        <p className="text-white/70">Discover courses from expert mentors</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, index) => (
          <Card key={index} hover className="glass-effect">
            <div className="h-40 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg mb-4"></div>
            <h3 className="text-xl font-bold text-white mb-2">
              Course Title {index + 1}
            </h3>
            <p className="text-white/70 text-sm mb-4">
              Learn the fundamentals and advanced concepts in this comprehensive course.
            </p>
            <div className="flex items-center justify-between mb-4">
              <span className="text-white font-bold">$99</span>
              <div className="flex items-center space-x-1">
                <span className="text-yellow-400">★</span>
                <span className="text-white">4.8</span>
              </div>
            </div>
            <Button variant="gradient" size="sm" className="w-full">
              Enroll Now
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default CourseList;
