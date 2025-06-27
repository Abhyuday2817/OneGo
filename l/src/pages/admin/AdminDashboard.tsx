
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Users, 
  BookOpen, 
  DollarSign, 
  TrendingUp, 
  AlertTriangle,
  MessageSquare,
  Star,
  Activity
} from 'lucide-react';

const AdminDashboard = () => {
  const stats = [
    {
      title: 'Total Users',
      value: '12,847',
      change: '+12.5%',
      icon: Users,
      color: 'bg-gradient-instagram'
    },
    {
      title: 'Active Courses',
      value: '2,456',
      change: '+8.2%',
      icon: BookOpen,
      color: 'bg-gradient-onlyfans'
    },
    {
      title: 'Revenue',
      value: '$485,293',
      change: '+23.1%',
      icon: DollarSign,
      color: 'bg-gradient-to-r from-green-500 to-emerald-600'
    },
    {
      title: 'Growth Rate',
      value: '18.5%',
      change: '+2.4%',
      icon: TrendingUp,
      color: 'bg-gradient-to-r from-purple-500 to-pink-500'
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'user',
      message: 'New user registration: john.doe@email.com',
      time: '2 minutes ago',
      severity: 'info'
    },
    {
      id: 2,
      type: 'course',
      message: 'Course published: Advanced React Patterns',
      time: '15 minutes ago',
      severity: 'success'
    },
    {
      id: 3,
      type: 'report',
      message: 'Content reported: Inappropriate comment on course',
      time: '1 hour ago',
      severity: 'warning'
    },
    {
      id: 4,
      type: 'payment',
      message: 'Payment processed: $299 for website development',
      time: '2 hours ago',
      severity: 'success'
    }
  ];

  const pendingReviews = [
    {
      id: 1,
      type: 'Course',
      title: 'Machine Learning Basics',
      author: 'Dr. Sarah Wilson',
      status: 'pending'
    },
    {
      id: 2,
      type: 'Gig',
      title: 'Logo Design Package',
      author: 'Mike Chen',
      status: 'pending'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          Admin Dashboard
        </h1>
        <p className="text-muted-foreground">
          Monitor platform activity and manage operations
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <Card key={index} className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 ${stat.color} rounded-full flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold gradient-text">{stat.value}</p>
                  <div className="flex items-center gap-2">
                    <p className="text-sm text-muted-foreground">{stat.title}</p>
                    <Badge className="bg-green-500 text-white text-xs">
                      {stat.change}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Activity */}
        <Card className="lg:col-span-2 glass-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start gap-3 p-3 border rounded-lg">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    activity.severity === 'success' ? 'bg-green-500' :
                    activity.severity === 'warning' ? 'bg-yellow-500' :
                    activity.severity === 'error' ? 'bg-red-500' :
                    'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm">{activity.message}</p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Pending Reviews */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Pending Reviews
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {pendingReviews.map((item) => (
                <div key={item.id} className="p-3 border rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <Badge variant="outline">{item.type}</Badge>
                    <Badge className="bg-yellow-500">{item.status}</Badge>
                  </div>
                  <h4 className="font-medium text-sm mb-1">{item.title}</h4>
                  <p className="text-xs text-muted-foreground">by {item.author}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <Card className="glass-card border-gradient-instagram">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              User Management
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Manage user accounts, roles, and permissions
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Active Users</span>
                <span className="font-semibold">11,234</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>New Today</span>
                <span className="font-semibold">127</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card border-gradient-onlyfans">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Content Moderation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Review reported content and moderate discussions
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Pending Reports</span>
                <span className="font-semibold">23</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Resolved Today</span>
                <span className="font-semibold">45</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card border-gradient-to-r from-purple-500 to-pink-500">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Star className="w-5 h-5" />
              Quality Control
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Monitor course quality and user satisfaction
            </p>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Avg Rating</span>
                <span className="font-semibold">4.8/5</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Quality Score</span>
                <span className="font-semibold">92%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;
