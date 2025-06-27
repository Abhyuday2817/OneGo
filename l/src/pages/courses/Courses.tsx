
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  Search, 
  Filter, 
  Star, 
  Clock, 
  Users, 
  PlayCircle,
  BookOpen,
  TrendingUp,
  Award
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Courses = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { name: 'All Courses', count: 1240, active: true },
    { name: 'Technology', count: 450, active: false },
    { name: 'Business', count: 320, active: false },
    { name: 'Design', count: 180, active: false },
    { name: 'Marketing', count: 150, active: false },
    { name: 'Personal Development', count: 140, active: false },
  ];

  const featuredCourses = [
    {
      id: 1,
      title: 'Complete React Developer Course 2024',
      instructor: 'Sarah Wilson',
      instructorAvatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=250&fit=crop',
      price: '$89.99',
      originalPrice: '$149.99',
      rating: 4.9,
      reviews: 2840,
      students: 15420,
      duration: '42 hours',
      level: 'Intermediate',
      category: 'Technology',
      bestseller: true,
      tags: ['React', 'JavaScript', 'Frontend']
    },
    {
      id: 2,
      title: 'Product Management Fundamentals',
      instructor: 'Mike Johnson',
      instructorAvatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=250&fit=crop',
      price: '$79.99',
      originalPrice: '$129.99',
      rating: 4.8,
      reviews: 1560,
      students: 8930,
      duration: '28 hours',
      level: 'Beginner',
      category: 'Business',
      bestseller: false,
      tags: ['Product Management', 'Strategy', 'Leadership']
    },
    {
      id: 3,
      title: 'Advanced UX/UI Design Masterclass',
      instructor: 'Emily Chen',
      instructorAvatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1649972904349-6e44c42644a7?w=400&h=250&fit=crop',
      price: '$99.99',
      originalPrice: '$179.99',
      rating: 4.9,
      reviews: 3210,
      students: 12450,
      duration: '36 hours',
      level: 'Advanced',
      category: 'Design',
      bestseller: true,
      tags: ['UX Design', 'UI Design', 'Figma']
    },
    {
      id: 4,
      title: 'Digital Marketing Strategy 2024',
      instructor: 'David Brown',
      instructorAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&h=250&fit=crop',
      price: '$69.99',
      originalPrice: '$119.99',
      rating: 4.7,
      reviews: 890,
      students: 5670,
      duration: '24 hours',
      level: 'Intermediate',
      category: 'Marketing',
      bestseller: false,
      tags: ['Digital Marketing', 'SEO', 'Social Media']
    },
    {
      id: 5,
      title: 'Leadership & Team Management',
      instructor: 'Jessica Lee',
      instructorAvatar: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?w=400&h=250&fit=crop',
      price: '$84.99',
      originalPrice: '$139.99',
      rating: 4.8,
      reviews: 1240,
      students: 7890,
      duration: '32 hours',
      level: 'Intermediate',
      category: 'Personal Development',
      bestseller: false,
      tags: ['Leadership', 'Management', 'Communication']
    },
    {
      id: 6,
      title: 'Full Stack Web Development Bootcamp',
      instructor: 'Alex Rodriguez',
      instructorAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&h=100&fit=crop&crop=face',
      thumbnail: 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=250&fit=crop',
      price: '$129.99',
      originalPrice: '$199.99',
      rating: 4.9,
      reviews: 4560,
      students: 23400,
      duration: '65 hours',
      level: 'Beginner',
      category: 'Technology',
      bestseller: true,
      tags: ['Full Stack', 'Node.js', 'MongoDB']
    }
  ];

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Beginner': return 'bg-green-100 text-green-800';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'Advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-hero rounded-xl p-8 text-white">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-4xl font-display font-bold mb-4">
            Discover Amazing Courses
          </h1>
          <p className="text-white/80 text-lg mb-6">
            Learn from industry experts and advance your career with our comprehensive course library
          </p>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-1">
              <BookOpen className="h-4 w-4" />
              <span>1,240+ Courses</span>
            </div>
            <div className="flex items-center space-x-1">
              <Users className="h-4 w-4" />
              <span>50,000+ Students</span>
            </div>
            <div className="flex items-center space-x-1">
              <Award className="h-4 w-4" />
              <span>Expert Instructors</span>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search courses, instructors, topics..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 pr-4 bg-background"
          />
        </div>
        <Button variant="outline" className="flex items-center space-x-2">
          <Filter className="h-4 w-4" />
          <span>Filters</span>
        </Button>
      </div>

      {/* Categories */}
      <div className="flex flex-wrap gap-2">
        {categories.map((category, index) => (
          <Badge
            key={index}
            variant={category.active ? "default" : "outline"}
            className={`cursor-pointer px-4 py-2 ${
              category.active 
                ? 'bg-gradient-instagram text-white' 
                : 'hover:bg-muted/50'
            }`}
          >
            {category.name} ({category.count})
          </Badge>
        ))}
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {featuredCourses.map((course) => (
          <Card key={course.id} className="group hover:shadow-xl transition-all duration-300 overflow-hidden">
            <div className="relative">
              <img
                src={course.thumbnail}
                alt={course.title}
                className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
              />
              {course.bestseller && (
                <Badge className="absolute top-3 left-3 bg-gradient-instagram text-white">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  Bestseller
                </Badge>
              )}
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center">
                <Button
                  size="sm"
                  className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-white/90 text-black hover:bg-white"
                >
                  <PlayCircle className="h-4 w-4 mr-1" />
                  Preview
                </Button>
              </div>
            </div>
            
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between mb-2">
                <Badge className={getLevelColor(course.level)} variant="secondary">
                  {course.level}
                </Badge>
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-400 fill-current" />
                  <span className="text-sm font-medium">{course.rating}</span>
                  <span className="text-sm text-muted-foreground">({course.reviews})</span>
                </div>
              </div>
              <CardTitle className="text-lg leading-tight group-hover:text-primary transition-colors">
                {course.title}
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <img
                  src={course.instructorAvatar}
                  alt={course.instructor}
                  className="w-6 h-6 rounded-full object-cover"
                />
                <span className="text-sm text-muted-foreground">{course.instructor}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{course.duration}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Users className="h-4 w-4" />
                  <span>{course.students.toLocaleString()}</span>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-1">
                {course.tags.slice(0, 3).map((tag, index) => (
                  <Badge key={index} variant="outline" className="text-xs">
                    {tag}
                  </Badge>
                ))}
              </div>
              
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-primary">{course.price}</span>
                  <span className="text-sm text-muted-foreground line-through">
                    {course.originalPrice}
                  </span>
                </div>
                <Link to={`/courses/${course.id}`}>
                  <Button className="btn-gradient text-white">
                    Enroll Now
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Load More */}
      <div className="text-center">
        <Button variant="outline" className="px-8">
          Load More Courses
        </Button>
      </div>
    </div>
  );
};

export default Courses;
