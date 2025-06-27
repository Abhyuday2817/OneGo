
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Progress } from '@/components/ui/progress';
import { 
  Play, 
  Clock, 
  Users, 
  Star, 
  BookOpen, 
  Award,
  CheckCircle,
  Lock
} from 'lucide-react';

const CourseDetail = () => {
  const { id } = useParams();

  const course = {
    title: 'Complete React Development Masterclass',
    description: 'Master React from basics to advanced concepts with hands-on projects',
    instructor: 'Sarah Johnson',
    rating: 4.8,
    students: 1234,
    duration: '12 hours',
    lessons: 45,
    price: 99,
    level: 'Intermediate',
    category: 'Development'
  };

  const modules = [
    {
      title: 'Getting Started with React',
      lessons: 8,
      duration: '2 hours',
      completed: true
    },
    {
      title: 'Components and Props',
      lessons: 6,
      duration: '1.5 hours',
      completed: true
    },
    {
      title: 'State and Lifecycle',
      lessons: 7,
      duration: '2 hours',
      completed: false
    },
    {
      title: 'Advanced Patterns',
      lessons: 9,
      duration: '3 hours',
      completed: false
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Course Content */}
        <div className="lg:col-span-2">
          {/* Course Header */}
          <div className="mb-8">
            <div className="flex flex-wrap gap-2 mb-4">
              <Badge className="bg-gradient-instagram text-white">{course.category}</Badge>
              <Badge variant="outline">{course.level}</Badge>
            </div>
            <h1 className="text-4xl font-display font-bold gradient-text mb-4">
              {course.title}
            </h1>
            <p className="text-lg text-muted-foreground mb-6">
              {course.description}
            </p>
            
            {/* Course Stats */}
            <div className="flex flex-wrap gap-6 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="font-semibold text-foreground">{course.rating}</span>
                <span>({course.students} students)</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>{course.duration}</span>
              </div>
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                <span>{course.lessons} lessons</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                <span>{course.students} enrolled</span>
              </div>
            </div>
          </div>

          {/* Course Modules */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                Course Content
              </CardTitle>
              <Progress value={50} className="w-full" />
              <p className="text-sm text-muted-foreground">2 of 4 modules completed</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {modules.map((module, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:bg-muted/30 transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          {module.completed ? (
                            <CheckCircle className="w-5 h-5 text-green-500" />
                          ) : (
                            <Lock className="w-5 h-5 text-muted-foreground" />
                          )}
                          <h3 className="font-semibold">{module.title}</h3>
                        </div>
                        <div className="flex gap-4 text-sm text-muted-foreground ml-8">
                          <span>{module.lessons} lessons</span>
                          <span>{module.duration}</span>
                        </div>
                      </div>
                      <Button 
                        variant={module.completed ? "default" : "outline"} 
                        size="sm"
                        className={module.completed ? "btn-gradient" : ""}
                      >
                        <Play className="w-4 h-4 mr-2" />
                        {module.completed ? "Continue" : "Start"}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div>
          <Card className="sticky top-4 glass-card border-gradient-instagram">
            <CardHeader>
              <div className="text-center">
                <div className="text-3xl font-bold gradient-text mb-2">
                  ${course.price}
                </div>
                <p className="text-muted-foreground">One-time payment</p>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button className="w-full btn-gradient">
                <Award className="w-4 h-4 mr-2" />
                Enroll Now
              </Button>
              <Button variant="outline" className="w-full">
                Add to Wishlist
              </Button>
              
              {/* Instructor Info */}
              <div className="pt-4 border-t">
                <h3 className="font-semibold mb-3">Your Instructor</h3>
                <div className="flex items-center gap-3">
                  <Avatar>
                    <AvatarImage src="/placeholder.svg" />
                    <AvatarFallback className="bg-gradient-instagram text-white">
                      SJ
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium">{course.instructor}</p>
                    <p className="text-sm text-muted-foreground">
                      Senior React Developer
                    </p>
                  </div>
                </div>
              </div>

              {/* What's Included */}
              <div className="pt-4 border-t">
                <h3 className="font-semibold mb-3">What's Included</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Lifetime access</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Certificate of completion</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Source code files</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Direct instructor support</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default CourseDetail;
