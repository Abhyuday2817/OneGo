
import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../utils/constants';
import { formatCurrency } from '../../utils/helpers';

const MentorDashboard: React.FC = () => {
  // Mock data - replace with actual API calls
  const stats = {
    totalEarnings: 12450,
    thisMonthEarnings: 3200,
    totalStudents: 87,
    activeStudents: 23,
    coursesCreated: 5,
    averageRating: 4.8,
    completedSessions: 156,
    upcomingSessions: 8,
  };

  const recentSessions = [
    { id: 1, student: 'Alice Johnson', course: 'React Advanced', date: '2024-01-15', duration: '60 min', earnings: 120 },
    { id: 2, student: 'Bob Smith', course: '1-on-1 Consultation', date: '2024-01-14', duration: '45 min', earnings: 90 },
    { id: 3, student: 'Carol Davis', course: 'JavaScript Basics', date: '2024-01-13', duration: '30 min', earnings: 60 },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Mentor Dashboard</h1>
        <p className="text-white/70">Welcome back! Here's your performance overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-green-400 mb-2">
            {formatCurrency(stats.totalEarnings)}
          </div>
          <div className="text-white/70">Total Earnings</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-blue-400 mb-2">
            {formatCurrency(stats.thisMonthEarnings)}
          </div>
          <div className="text-white/70">This Month</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-purple-400 mb-2">
            {stats.totalStudents}
          </div>
          <div className="text-white/70">Total Students</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-yellow-400 mb-2">
            {stats.averageRating}⭐
          </div>
          <div className="text-white/70">Average Rating</div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card glass>
        <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link to={ROUTES.UPLOAD_COURSE}>
            <Button variant="gradient" className="w-full">
              📚 Upload New Course
            </Button>
          </Link>
          <Link to={ROUTES.AVAILABILITY}>
            <Button variant="outline" className="w-full text-white border-white/30">
              📅 Manage Availability
            </Button>
          </Link>
          <Link to={ROUTES.CHAT}>
            <Button variant="outline" className="w-full text-white border-white/30">
              💬 View Messages
            </Button>
          </Link>
        </div>
      </Card>

      {/* Recent Sessions */}
      <Card glass>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-white">Recent Sessions</h2>
          <Button variant="ghost" size="sm" className="text-blue-400">
            View All
          </Button>
        </div>
        <div className="space-y-4">
          {recentSessions.map((session) => (
            <div key={session.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
              <div>
                <h3 className="text-white font-medium">{session.student}</h3>
                <p className="text-white/70 text-sm">{session.course}</p>
              </div>
              <div className="text-right">
                <div className="text-green-400 font-semibold">
                  {formatCurrency(session.earnings)}
                </div>
                <div className="text-white/70 text-sm">{session.duration}</div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Performance Chart Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card glass>
          <h2 className="text-xl font-semibold text-white mb-4">Earnings Overview</h2>
          <div className="h-64 flex items-center justify-center text-white/50">
            📈 Chart will be implemented here
          </div>
        </Card>
        
        <Card glass>
          <h2 className="text-xl font-semibold text-white mb-4">Student Growth</h2>
          <div className="h-64 flex items-center justify-center text-white/50">
            📊 Chart will be implemented here
          </div>
        </Card>
      </div>
    </div>
  );
};

export default MentorDashboard;
