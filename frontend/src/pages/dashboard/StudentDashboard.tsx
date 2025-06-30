
import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../utils/constants';
import { formatCurrency } from '../../utils/helpers';

const StudentDashboard: React.FC = () => {
  // Mock data - replace with actual API calls
  const stats = {
    coursesEnrolled: 12,
    coursesCompleted: 8,
    hoursLearned: 145,
    sessionsAttended: 24,
    walletBalance: 450,
    achievements: 15,
  };

  const recentCourses = [
    { id: 1, title: 'React Advanced Patterns', mentor: 'John Doe', progress: 75, lastAccessed: '2 hours ago' },
    { id: 2, title: 'Node.js Masterclass', mentor: 'Jane Smith', progress: 45, lastAccessed: '1 day ago' },
    { id: 3, title: 'UI/UX Design Fundamentals', mentor: 'Mike Johnson', progress: 90, lastAccessed: '3 days ago' },
  ];

  const upcomingSessions = [
    { id: 1, mentor: 'Sarah Wilson', topic: 'JavaScript Interview Prep', date: 'Today, 3:00 PM', duration: '1 hour' },
    { id: 2, mentor: 'David Brown', topic: 'React Hooks Deep Dive', date: 'Tomorrow, 10:00 AM', duration: '45 min' },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Student Dashboard</h1>
        <p className="text-white/70">Welcome back! Continue your learning journey.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-blue-400 mb-2">
            {stats.coursesEnrolled}
          </div>
          <div className="text-white/70">Courses Enrolled</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-green-400 mb-2">
            {stats.coursesCompleted}
          </div>
          <div className="text-white/70">Completed</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-purple-400 mb-2">
            {stats.hoursLearned}h
          </div>
          <div className="text-white/70">Hours Learned</div>
        </Card>
        
        <Card glass className="text-center">
          <div className="text-3xl font-bold text-yellow-400 mb-2">
            {formatCurrency(stats.walletBalance)}
          </div>
          <div className="text-white/70">Wallet Balance</div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card glass>
        <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Link to={ROUTES.COURSES}>
            <Button variant="gradient" className="w-full">
              📚 Browse Courses
            </Button>
          </Link>
          <Link to={ROUTES.MENTORS}>
            <Button variant="outline" className="w-full text-white border-white/30">
              👨‍🏫 Find Mentors
            </Button>
          </Link>
          <Link to={ROUTES.LEARNING_REQUEST}>
            <Button variant="outline" className="w-full text-white border-white/30">
              📝 Post Request
            </Button>
          </Link>
          <Link to={ROUTES.WALLET}>
            <Button variant="outline" className="w-full text-white border-white/30">
              💳 Manage Wallet
            </Button>
          </Link>
        </div>
      </Card>

      {/* Continue Learning */}
      <Card glass>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-white">Continue Learning</h2>
          <Button variant="ghost" size="sm" className="text-blue-400">
            View All Courses
          </Button>
        </div>
        <div className="space-y-4">
          {recentCourses.map((course) => (
            <div key={course.id} className="p-4 bg-white/5 rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-white font-medium">{course.title}</h3>
                  <p className="text-white/70 text-sm">by {course.mentor}</p>
                </div>
                <span className="text-white/70 text-sm">{course.lastAccessed}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex-1 mr-4">
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>
                <span className="text-white/70 text-sm">{course.progress}%</span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Upcoming Sessions */}
      <Card glass>
        <h2 className="text-xl font-semibold text-white mb-4">Upcoming Sessions</h2>
        {upcomingSessions.length > 0 ? (
          <div className="space-y-4">
            {upcomingSessions.map((session) => (
              <div key={session.id} className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
                <div>
                  <h3 className="text-white font-medium">{session.topic}</h3>
                  <p className="text-white/70 text-sm">with {session.mentor}</p>
                </div>
                <div className="text-right">
                  <div className="text-blue-400 font-medium">{session.date}</div>
                  <div className="text-white/70 text-sm">{session.duration}</div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-white/70 mb-4">No upcoming sessions</p>
            <Link to={ROUTES.MENTORS}>
              <Button variant="outline" className="text-white border-white/30">
                Book a Session
              </Button>
            </Link>
          </div>
        )}
      </Card>
    </div>
  );
};

export default StudentDashboard;
