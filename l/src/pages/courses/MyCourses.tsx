
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Play, BookOpen, Clock, Star, Plus, Edit, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';

const MyCourses = () => {
  const [activeTab, setActiveTab] = useState('enrolled');

  const enrolledCourses = [
    {
      id: 1,
      title: 'Complete React Development',
      instructor: 'Sarah Johnson',
      progress: 75,
      totalLessons: 45,
      completedLessons: 34,
      rating: 4.8,
      thumbnail: '/placeholder.svg'
    },
    {
      id: 2,
      title: 'Advanced JavaScript Concepts',
      instructor: 'Mike Chen',
      progress: 30,
      totalLessons: 32,
      completedLessons: 10,
      rating: 4.9,
      thumbnail: '/placeholder.svg'
    }
  ];

  const createdCourses = [
    {
      id: 3,
      title: 'UI/UX Design Fundamentals',
      students: 234,
      revenue: 2340,
      rating: 4.7,
      status: 'published',
      thumbnail: '/placeholder.svg'
    },
    {
      id: 4,
      title: 'Figma for Beginners',
      students: 87,
      revenue: 870,
      rating: 4.5,
      status: 'draft',
      thumbnail: '/placeholder.svg'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            My Courses
          </h1>
          <p className="text-muted-foreground">
            Manage your learning journey and created content
          </p>
        </div>
        <Link to="/courses/create">
          <Button className="btn-gradient">
            <Plus className="w-4 h-4 mr-2" />
            Create Course
          </Button>
        </Link>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-8">
          <TabsTrigger value="enrolled" className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Enrolled Courses
          </TabsTrigger>
          <TabsTrigger value="created" className="flex items-center gap-2">
            <Edit className="w-4 h-4" />
            Created Courses
          </TabsTrigger>
        </TabsList>

        <TabsContent value="enrolled">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {enrolledCourses.map((course) => (
              <Card key={course.id} className="group hover:shadow-xl transition-all duration-300 glass-card">
                <CardHeader className="p-0">
                  <div className="aspect-video bg-muted rounded-t-lg overflow-hidden">
                    <img 
                      src={course.thumbnail} 
                      alt={course.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div>
                      <CardTitle className="text-lg group-hover:gradient-text transition-colors">
                        {course.title}
                      </CardTitle>
                      <p className="text-sm text-muted-foreground">
                        by {course.instructor}
                      </p>
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>Progress</span>
                        <span>{course.progress}%</span>
                      </div>
                      <Progress value={course.progress} className="h-2" />
                      <p className="text-xs text-muted-foreground">
                        {course.completedLessons} of {course.totalLessons} lessons completed
                      </p>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1">
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        <span className="text-sm font-medium">{course.rating}</span>
                      </div>
                      <Link to={`/courses/${course.id}`}>
                        <Button className="btn-gradient">
                          <Play className="w-4 h-4 mr-2" />
                          Continue
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="created">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {createdCourses.map((course) => (
              <Card key={course.id} className="group hover:shadow-xl transition-all duration-300 glass-card">
                <CardHeader className="p-0">
                  <div className="aspect-video bg-muted rounded-t-lg overflow-hidden relative">
                    <img 
                      src={course.thumbnail} 
                      alt={course.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <Badge 
                      className={`absolute top-2 right-2 ${
                        course.status === 'published' 
                          ? 'bg-green-500' 
                          : 'bg-yellow-500'
                      }`}
                    >
                      {course.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="space-y-4">
                    <div>
                      <CardTitle className="text-lg group-hover:gradient-text transition-colors">
                        {course.title}
                      </CardTitle>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Students</p>
                        <p className="font-semibold">{course.students}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Revenue</p>
                        <p className="font-semibold">${course.revenue}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1">
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        <span className="text-sm font-medium">{course.rating}</span>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button variant="outline" size="sm" className="text-red-500 hover:text-red-700">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MyCourses;
