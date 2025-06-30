
import React from 'react';
import { useParams } from 'react-router-dom';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Avatar from '../../components/ui/Avatar';

const MentorProfile: React.FC = () => {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <Card glass className="p-8">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <Avatar
            name="John Mentor"
            size="xl"
            className="w-24 h-24"
          />
          <div className="text-center md:text-left flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">John Mentor</h1>
            <p className="text-blue-400 text-lg mb-4">Senior Full Stack Developer</p>
            <div className="flex items-center justify-center md:justify-start space-x-4 mb-4">
              <div className="flex items-center space-x-1">
                <span className="text-yellow-400">★</span>
                <span className="text-white">4.9</span>
                <span className="text-white/50">(124 reviews)</span>
              </div>
              <div className="text-white/70">
                500+ sessions completed
              </div>
            </div>
            <div className="flex space-x-4">
              <Button variant="gradient" size="lg">
                Book Session - $50/hr
              </Button>
              <Button variant="outline" className="text-white border-white/30">
                Send Message
              </Button>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">About</h3>
            <p className="text-white/70 mb-4">
              I'm a passionate full-stack developer with over 5 years of experience building scalable web applications. 
              I specialize in React, Node.js, and cloud technologies, and I love helping others learn and grow in their programming journey.
            </p>
            <p className="text-white/70">
              My teaching approach focuses on practical, hands-on learning. I believe in building real projects 
              together and explaining concepts in a way that's easy to understand and remember.
            </p>
          </Card>

          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">Skills & Expertise</h3>
            <div className="flex flex-wrap gap-2">
              {['React', 'Node.js', 'TypeScript', 'Python', 'AWS', 'Docker', 'MongoDB', 'PostgreSQL'].map(skill => (
                <span key={skill} className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </Card>

          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">Recent Reviews</h3>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="border-b border-white/10 pb-4 last:border-b-0">
                  <div className="flex items-center space-x-3 mb-2">
                    <Avatar name={`Student ${i + 1}`} size="sm" />
                    <div>
                      <div className="text-white font-medium">Student {i + 1}</div>
                      <div className="flex items-center space-x-1">
                        <span className="text-yellow-400">★★★★★</span>
                        <span className="text-white/50 text-sm">2 days ago</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-white/70 text-sm">
                    Great mentor! Very patient and explains concepts clearly. 
                    Helped me understand React hooks and state management.
                  </p>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">Availability</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-white/70">Monday</span>
                <span className="text-white">9:00 AM - 5:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">Tuesday</span>
                <span className="text-white">9:00 AM - 5:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">Wednesday</span>
                <span className="text-white">9:00 AM - 5:00 PM</span>
              </div>
            </div>
          </Card>

          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">Languages</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-white/70">English</span>
                <span className="text-white">Native</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">Spanish</span>
                <span className="text-white">Fluent</span>
              </div>
            </div>
          </Card>

          <Card glass>
            <h3 className="text-xl font-bold text-white mb-4">Response Time</h3>
            <p className="text-white">Usually responds within 1 hour</p>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default MentorProfile;
