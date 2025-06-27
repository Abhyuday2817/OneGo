
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Search, Filter, Star, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

const FindMentors = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const mentors = [
    {
      id: 1,
      name: 'Sarah Johnson',
      role: 'Product Manager at Google',
      rating: 4.9,
      reviews: 87,
      price: 75,
      skills: ['Product Strategy', 'User Research', 'Leadership'],
      location: 'San Francisco, CA'
    },
    {
      id: 2,
      name: 'Mike Chen',
      role: 'Senior Developer at Netflix',
      rating: 4.8,
      reviews: 143,
      price: 60,
      skills: ['React', 'Node.js', 'System Design'],
      location: 'Los Angeles, CA'
    },
    {
      id: 3,
      name: 'Emily Rodriguez',
      role: 'UX Designer at Airbnb',
      rating: 4.9,
      reviews: 92,
      price: 55,
      skills: ['UI/UX', 'Figma', 'Design Systems'],
      location: 'New York, NY'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-4">
          Find Your Perfect Mentor
        </h1>
        <p className="text-muted-foreground text-lg">
          Connect with industry experts and accelerate your career growth
        </p>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search mentors by name, skill, or company..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </Button>
      </div>

      {/* Mentors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mentors.map((mentor) => (
          <Card key={mentor.id} className="group hover:shadow-xl transition-all duration-300 glass-card">
            <CardHeader>
              <div className="flex items-start gap-4">
                <Avatar className="w-16 h-16">
                  <AvatarImage src="/placeholder.svg" />
                  <AvatarFallback className="bg-gradient-instagram text-white">
                    {mentor.name.split(' ').map(n => n[0]).join('')}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <CardTitle className="text-lg group-hover:gradient-text transition-colors">
                    {mentor.name}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground mb-2">
                    {mentor.role}
                  </p>
                  <div className="flex items-center gap-1 mb-2">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm font-semibold">{mentor.rating}</span>
                    <span className="text-sm text-muted-foreground">
                      ({mentor.reviews} reviews)
                    </span>
                  </div>
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <MapPin className="w-3 h-3" />
                    {mentor.location}
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex flex-wrap gap-1">
                  {mentor.skills.map((skill, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-semibold gradient-text">
                    ${mentor.price}/hour
                  </span>
                  <Link to={`/mentors/${mentor.id}`}>
                    <Button className="btn-gradient">
                      View Profile
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default FindMentors;
