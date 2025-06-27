
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  BookOpen, 
  Calendar, 
  Users, 
  TrendingUp, 
  Clock, 
  Star,
  Award,
  MessageCircle,
  ArrowRight,
  PlayCircle
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();

  const stats = [
    {
      title: 'Courses Enrolled',
      value: '12',
      icon: BookOpen,
      color: 'from-instagram-500 to-instagram-600',
      change: '+2 this month'
    },
    {
      title: 'Hours Learned',
      value: '124',
      icon: Clock,
      color: 'from-onlyfans-500 to-onlyfans-600',
      change: '+18 this week'
    },
    {
      title: 'Mentorship Sessions',
      value: '8',
      icon: Users,
      color: 'from-emerald-500 to-emerald-600',
      change: '3 upcoming'
    },
    {
      title: 'Achievement Score',
      value: '85%',
      icon: Award,
      color: 'from-violet-500 to-violet-600',
      change: '+5% this month'
    }
  ];

  const recentCourses = [
    {
      id: 1,
      title: 'Advanced React Development',
      instructor: 'Sarah Wilson',
      progress: 75,
      duration: '6 hours left',
      thumbnail: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300&h=200&fit=crop'
    },
    {
      id: 2,
      title: 'Product Management Fundamentals',
      instructor: 'Mike Johnson',
      progress: 45,
      duration: '12 hours left',
      thumbnail: 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=300&h=200&fit=crop'
    },
    {
      id: 3,
      title: 'UX Design Principles',
      instructor: 'Emily Chen',
      progress: 90,
      duration: '2 hours left',
      thumbnail: 'https://images.unsplash.com/photo-1649972904349-6e44c42644a7?w=300&h=200&fit=crop'
    }
  ];

  const upcomingSessions = [
    {
      id: 1,
      title: 'Career Strategy Session',
      mentor: 'Dr. Alex Rodriguez',
      time: 'Today, 3:00 PM',
      type: 'Video Call',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face'
    },
    {
      id: 2,
      title: 'Technical Interview Prep',
      mentor: 'Jennifer Lee',
      time: 'Tomorrow, 10:00 AM',
      type: 'Video Call',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-hero rounded-xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-display font-bold mb-2">
              Welcome back, {user?.name}! 👋
            </h1>
            <p className="text-white/80 text-lg">
              Ready to continue your learning journey? You're doing great!
            </p>
          </div>
          <div className="hidden md:block">
            <Badge className="bg-white/20 text-white border-white/30" variant="outline">
              <Star className="w-4 h-4 mr-1" />
              Premium Member
            </Badge>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card key={index} className="group hover:shadow-lg transition-all duration-300">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg bg-gradient-to-r ${stat.color}`}>
                  <stat.icon className="h-5 w-5 text-white" />
                </div>
                <TrendingUp className="h-4 w-4 text-green-500" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{stat.value}</div>
              <div className="text-sm text-muted-foreground mb-2">{stat.title}</div>
              <div className="text-xs text-green-600 font-medium">{stat.change}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Continue Learning */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-5 w-5" />
                  Continue Learning
                </CardTitle>
                <CardDescription>Pick up where you left off</CardDescription>
              </div>
              <Link to="/my-courses">
                <Button variant="ghost" size="sm">
                  View All
                  <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentCourses.map((course) => (
              <div key={course.id} className="flex items-center space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-colors group">
                <img
                  src={course.thumbnail}
                  alt={course.title}
                  className="w-16 h-16 rounded-lg object-cover"
                />
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-sm truncate group-hover:text-primary transition-colors">
                    {course.title}
                  </h3>
                  <p className="text-xs text-muted-foreground mb-2">by {course.instructor}</p>
                  <div className="flex items-center space-x-2">
                    <Progress value={course.progress} className="h-2 flex-1" />
                    <span className="text-xs text-muted-foreground">{course.progress}%</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{course.duration}</p>
                </div>
                <Button size="sm" variant="ghost" className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <PlayCircle className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Upcoming Sessions */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Upcoming Sessions
                </CardTitle>
                <CardDescription>Your scheduled mentorship sessions</CardDescription>
              </div>
              <Link to="/my-consultations">
                <Button variant="ghost" size="sm">
                  View All
                  <ArrowRight className="h-4 w-4 ml-1" />
                </Button>
              </Link>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {upcomingSessions.map((session) => (
              <div key={session.id} className="flex items-center space-x-4 p-3 rounded-lg hover:bg-muted/50 transition-colors group">
                <img
                  src={session.avatar}
                  alt={session.mentor}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-sm truncate group-hover:text-primary transition-colors">
                    {session.title}
                  </h3>
                  <p className="text-xs text-muted-foreground">with {session.mentor}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <Badge variant="outline" className="text-xs px-2 py-0">
                      {session.type}
                    </Badge>
                    <span className="text-xs text-muted-foreground">{session.time}</span>
                  </div>
                </div>
                <Button size="sm" variant="outline" className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <MessageCircle className="h-4 w-4" />
                </Button>
              </div>
            ))}
            <div className="pt-2">
              <Link to="/consultations">
                <Button className="w-full btn-gradient text-white">
                  Book New Session
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks to accelerate your growth</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link to="/courses">
              <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
                <BookOpen className="h-6 w-6" />
                <span className="text-sm">Browse Courses</span>
              </Button>
            </Link>
            <Link to="/mentors">
              <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
                <Users className="h-6 w-6" />
                <span className="text-sm">Find Mentors</span>
              </Button>
            </Link>
            <Link to="/gigs">
              <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
                <Award className="h-6 w-6" />
                <span className="text-sm">Explore Gigs</span>
              </Button>
            </Link>
            <Link to="/chat">
              <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
                <MessageCircle className="h-6 w-6" />
                <span className="text-sm">Start Chat</span>
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
