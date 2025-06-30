
import React from 'react';
import { useParams } from 'react-router-dom';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const CourseDetail: React.FC = () => {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card glass className="p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <div className="h-64 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg mb-6"></div>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white mb-4">Course Title</h1>
            <p className="text-white/70 mb-6">
              This comprehensive course covers everything you need to know about the subject.
            </p>
            <div className="flex items-center space-x-4 mb-6">
              <span className="text-2xl font-bold text-white">$99</span>
              <div className="flex items-center space-x-1">
                <span className="text-yellow-400">★</span>
                <span className="text-white">4.8</span>
                <span className="text-white/50">(124 reviews)</span>
              </div>
            </div>
            <Button variant="gradient" size="lg" className="w-full">
              Enroll Now
            </Button>
          </div>
        </div>
      </Card>

      <Card glass>
        <h3 className="text-xl font-bold text-white mb-4">Course Content</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between p-3 bg-white/5 rounded">
            <span className="text-white">1. Introduction</span>
            <span className="text-white/50">5 min</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white/5 rounded">
            <span className="text-white">2. Getting Started</span>
            <span className="text-white/50">15 min</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-white/5 rounded">
            <span className="text-white">3. Advanced Concepts</span>
            <span className="text-white/50">25 min</span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default CourseDetail;
