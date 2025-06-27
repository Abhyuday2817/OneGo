
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertTriangle, Eye, Ban, Check, X, Flag } from 'lucide-react';

const ContentModeration = () => {
  const [activeTab, setActiveTab] = useState('reports');

  const reports = [
    {
      id: 1,
      type: 'course',
      title: 'Inappropriate content in React course',
      reporter: 'John Doe',
      reported: 'Mike Chen',
      content: 'This course contains inappropriate language and examples.',
      severity: 'medium',
      status: 'pending',
      date: '2024-01-15'
    },
    {
      id: 2,
      type: 'comment',
      title: 'Spam comment on consultation',
      reporter: 'Sarah Johnson',
      reported: 'Jane Smith',
      content: 'User is posting promotional links in comments.',
      severity: 'low',
      status: 'pending',
      date: '2024-01-14'
    },
    {
      id: 3,
      type: 'gig',
      title: 'Misleading gig description',
      reporter: 'Emily Davis',
      reported: 'Alex Wilson',
      content: 'Gig promises results that are not deliverable.',
      severity: 'high',
      status: 'pending',
      date: '2024-01-13'
    }
  ];

  const reviewItems = [
    {
      id: 1,
      type: 'course',
      title: 'Advanced Python Programming',
      author: 'Dr. Sarah Wilson',
      submitted: '2024-01-15',
      status: 'pending'
    },
    {
      id: 2,
      type: 'gig',
      title: 'Logo Design Professional Package',
      author: 'Mike Chen',
      submitted: '2024-01-14',
      status: 'pending'
    }
  ];

  const ReportCard = ({ report }) => (
    <Card className="glass-card mb-4">
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge 
                className={
                  report.severity === 'high' ? 'bg-red-500' :
                  report.severity === 'medium' ? 'bg-yellow-500' :
                  'bg-blue-500'
                }
              >
                {report.severity}
              </Badge>
              <Badge variant="outline">{report.type}</Badge>
              <Badge className="bg-gray-500">{report.status}</Badge>
            </div>
            <h3 className="font-semibold text-lg mb-2">{report.title}</h3>
            <p className="text-muted-foreground mb-4">{report.content}</p>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span>Reported by: {report.reporter}</span>
              <span>Against: {report.reported}</span>
              <span>Date: {report.date}</span>
            </div>
          </div>
          <div className="flex items-center gap-2 ml-4">
            <Button variant="outline" size="sm">
              <Eye className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="sm" className="text-green-600">
              <Check className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="sm" className="text-red-600">
              <X className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="sm" className="text-red-600">
              <Ban className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const ReviewCard = ({ item }) => (
    <Card className="glass-card mb-4">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Avatar>
              <AvatarImage src="/placeholder.svg" />
              <AvatarFallback className="bg-gradient-instagram text-white">
                {item.author.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-lg">{item.title}</h3>
              <p className="text-muted-foreground">by {item.author}</p>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="outline">{item.type}</Badge>
                <Badge className="bg-yellow-500">{item.status}</Badge>
                <span className="text-sm text-muted-foreground">
                  Submitted: {item.submitted}
                </span>
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <Eye className="w-4 h-4 mr-2" />
              Review
            </Button>
            <Button className="btn-gradient" size="sm">
              <Check className="w-4 h-4 mr-2" />
              Approve
            </Button>
            <Button variant="outline" size="sm" className="text-red-600">
              <X className="w-4 h-4 mr-2" />
              Reject
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          Content Moderation
        </h1>
        <p className="text-muted-foreground">
          Review reports and moderate platform content
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">23</div>
            <p className="text-sm text-muted-foreground">Pending Reports</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">145</div>
            <p className="text-sm text-muted-foreground">Resolved Today</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">8</div>
            <p className="text-sm text-muted-foreground">Pending Reviews</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">97%</div>
            <p className="text-sm text-muted-foreground">Response Rate</p>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-8">
          <TabsTrigger value="reports">
            <Flag className="w-4 h-4 mr-2" />
            Reports
          </TabsTrigger>
          <TabsTrigger value="reviews">
            <Eye className="w-4 h-4 mr-2" />
            Content Review
          </TabsTrigger>
          <TabsTrigger value="actions">
            <AlertTriangle className="w-4 h-4 mr-2" />
            Actions Taken
          </TabsTrigger>
        </TabsList>

        <TabsContent value="reports">
          <div>
            {reports.map((report) => (
              <ReportCard key={report.id} report={report} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="reviews">
          <div>
            {reviewItems.map((item) => (
              <ReviewCard key={item.id} item={item} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="actions">
          <Card className="glass-card">
            <CardContent className="p-6">
              <p className="text-center text-muted-foreground">
                Recent moderation actions will be displayed here
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ContentModeration;
