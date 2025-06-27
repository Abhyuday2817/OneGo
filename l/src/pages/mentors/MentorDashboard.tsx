
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Users, 
  Calendar, 
  DollarSign, 
  Star,
  TrendingUp,
  Clock,
  MessageCircle,
  BookOpen,
  Award,
  BarChart3
} from 'lucide-react';

const MentorDashboard = () => {
  const stats = [
    {
      title: 'Total Students',
      value: '124',
      icon: Users,
      color: 'from-instagram-500 to-instagram-600',
      change: '+12 this month'
    },
    {
      title: 'Sessions This Month',
      value: '28',
      icon: Calendar,
      color: 'from-onlyfans-500 to-onlyfans-600',
      change: '+8 from last month'
    },
    {
      title: 'Monthly Earnings',
      value: '$3,240',
      icon: DollarSign,
      color: 'from-emerald-500 to-emerald-600',
      change: '+15% increase'
    },
    {
      title: 'Average Rating',
      value: '4.9',
      icon: Star,
      color: 'from-yellow-500 to-yellow-600',
      change: '150 reviews'
    }
  ];

  const upcomingSessions = [
    {
      id: 1,
      studentName: 'Alex Johnson',
      topic: 'Career Strategy Session',
      time: 'Today, 3:00 PM',
      duration: '60 min',
      type: 'Video Call',
      studentAvatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face'
    },
    {
      id: 2,
      studentName: 'Sarah Wilson',
      topic: 'Technical Interview Prep',
      time: 'Tomorrow, 10:00 AM',
      duration: '45 min',
      type: 'Video Call',
      studentAvatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face'
    },
    {
      id: 3,
      studentName: 'Mike Chen',
      topic: 'Product Management Review',
      time: 'Jan 15, 2:00 PM',
      duration: '90 min',
      type: 'Video Call',
      studentAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face'
    }
  ];

  const recentReviews = [
    {
      studentName: 'Emma Davis',
      rating: 5,
      comment: 'Incredible insights and practical advice. Helped me land my dream job!',
      date: '2 days ago'
    },
    {
      studentName: 'Tom Rodriguez',
      rating: 5,
      comment: 'Very knowledgeable and patient. Great mentoring experience.',
      date: '1 week ago'
    },
    {
      studentName: 'Lisa Park',
      rating: 4,
      comment: 'Helpful session with actionable feedback. Would recommend!',
      date: '2 weeks ago'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-onlyfans rounded-xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-display font-bold mb-2">
              Mentor Dashboard 👨‍🏫
            </h1>
            <p className="text-white/80 text-lg">
              Track your mentoring impact and manage your sessions
            </p>
          </div>
          <div className="hidden md:block">
            <Badge className="bg-white/20 text-white border-white/30" variant="outline">
              <Award className="w-4 h-4 mr-1" />
              Top Mentor
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
        {/* Upcoming Sessions */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Upcoming Sessions
                </CardTitle>
                <CardDescription>Your scheduled mentoring sessions</CardDescription>
              </div>
              <Button variant="ghost" size="sm">
                View All
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {upcomingSessions.map((session) => (
              <div key={session.id} className="flex items-center space-x-4 p-4 rounded-lg border border-border hover:bg-muted/50 transition-colors group">
                <img
                  src={session.studentAvatar}
                  alt={session.studentName}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-sm truncate group-hover:text-primary transition-colors">
                    {session.topic}
                  </h3>
                  <p className="text-xs text-muted-foreground">with {session.studentName}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <Badge variant="outline" className="text-xs px-2 py-0">
                      {session.type}
                    </Badge>
                    <span className="text-xs text-muted-foreground">{session.time}</span>
                    <span className="text-xs text-muted-foreground">•</span>
                    <span className="text-xs text-muted-foreground">{session.duration}</span>
                  </div>
                </div>
                <div className="flex flex-col space-y-1">
                  <Button size="sm" className="btn-gradient text-white">
                    <MessageCircle className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
            <div className="pt-2">
              <Button className="w-full btn-gradient text-white">
                Manage Availability
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Reviews */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Star className="h-5 w-5" />
                  Recent Reviews
                </CardTitle>
                <CardDescription>What your mentees are saying</CardDescription>
              </div>
              <Button variant="ghost" size="sm">
                View All
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentReviews.map((review, index) => (
              <div key={index} className="p-4 rounded-lg border border-border space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-sm">{review.studentName}</h3>
                  <div className="flex items-center space-x-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-3 w-3 ${
                          i < review.rating
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                </div>
                <p className="text-sm text-muted-foreground italic">
                  "{review.comment}"
                </p>
                <p className="text-xs text-muted-foreground">{review.date}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Performance Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Performance Overview
          </CardTitle>
          <CardDescription>Your mentoring metrics over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Session Completion Rate</span>
                <span className="font-medium">96%</span>
              </div>
              <Progress value={96} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Student Satisfaction</span>
                <span className="font-medium">4.9/5</span>
              </div>
              <Progress value={98} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Response Rate</span>
                <span className="font-medium">89%</span>
              </div>
              <Progress value={89} className="h-2" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common mentor tasks and tools</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
              <Calendar className="h-6 w-6" />
              <span className="text-sm">Set Availability</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
              <BookOpen className="h-6 w-6" />
              <span className="text-sm">Create Course</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
              <MessageCircle className="h-6 w-6" />
              <span className="text-sm">Message Students</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2 w-full">
              <BarChart3 className="h-6 w-6" />
              <span className="text-sm">View Analytics</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default MentorDashboard;
