
import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { ROUTES } from '../../utils/constants';

const Index: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated && user) {
      const dashboardRoute = user.role === 'mentor' 
        ? ROUTES.MENTOR_DASHBOARD 
        : ROUTES.STUDENT_DASHBOARD;
      navigate(dashboardRoute);
    }
  }, [isAuthenticated, user, navigate]);

  const features = [
    {
      icon: '👨‍🏫',
      title: 'Expert Mentors',
      description: 'Connect with experienced professionals in your field'
    },
    {
      icon: '📚',
      title: 'Quality Courses',
      description: 'Access premium courses created by industry experts'
    },
    {
      icon: '💬',
      title: 'Live Sessions',
      description: '1-on-1 mentoring sessions with real-time interaction'
    },
    {
      icon: '🎯',
      title: 'Personalized Learning',
      description: 'Tailored learning paths based on your goals'
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 animate-float">
            Learn From The
            <span className="bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
              {' '}Best Mentors
            </span>
          </h1>
          <p className="text-xl text-white/80 mb-10 max-w-2xl mx-auto">
            Connect with industry experts, take personalized courses, and accelerate your career with OneGo
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to={ROUTES.REGISTER}>
              <Button variant="gradient" size="lg" className="px-8">
                Get Started Free
              </Button>
            </Link>
            <Link to={ROUTES.MENTORS}>
              <Button variant="outline" size="lg" className="px-8 text-white border-white/30">
                Browse Mentors
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            Why Choose OneGo?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} glass hover className="text-center">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-white/70">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white/5">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-4xl font-bold text-white mb-2">10K+</div>
              <div className="text-white/70">Active Students</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">500+</div>
              <div className="text-white/70">Expert Mentors</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white mb-2">1K+</div>
              <div className="text-white/70">Courses Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <Card glass className="p-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Start Learning?
            </h2>
            <p className="text-white/80 mb-8 text-lg">
              Join thousands of students already learning with OneGo
            </p>
            <Link to={ROUTES.REGISTER}>
              <Button variant="gradient" size="lg" className="px-12">
                Start Your Journey
              </Button>
            </Link>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;
