
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Search, Filter, Star, Clock, DollarSign } from 'lucide-react';
import { Link } from 'react-router-dom';

const Gigs = () => {
  const gigs = [
    {
      id: 1,
      title: 'Website Design & Development',
      description: 'I will create a modern, responsive website for your business',
      creator: 'Emily Rodriguez',
      rating: 4.9,
      reviews: 87,
      startingPrice: 299,
      deliveryTime: '3 days',
      tags: ['Web Design', 'React', 'UI/UX'],
      image: '/placeholder.svg'
    },
    {
      id: 2,
      title: 'Logo Design & Branding',
      description: 'Professional logo design with complete brand identity package',
      creator: 'David Kim',
      rating: 4.8,
      reviews: 156,
      startingPrice: 150,
      deliveryTime: '2 days',
      tags: ['Logo Design', 'Branding', 'Graphic Design'],
      image: '/placeholder.svg'
    },
    {
      id: 3,
      title: 'SEO Optimization & Marketing',
      description: 'Boost your website ranking with proven SEO strategies',
      creator: 'Sarah Johnson',
      rating: 4.9,
      reviews: 234,
      startingPrice: 199,
      deliveryTime: '5 days',
      tags: ['SEO', 'Marketing', 'Analytics'],
      image: '/placeholder.svg'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-4">
          Explore Gigs
        </h1>
        <p className="text-muted-foreground text-lg">
          Find professional services from talented freelancers
        </p>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search gigs..."
            className="pl-10"
          />
        </div>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </Button>
      </div>

      {/* Gigs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {gigs.map((gig) => (
          <Card key={gig.id} className="group hover:shadow-xl transition-all duration-300 glass-card">
            <CardHeader className="p-0">
              <div className="aspect-video bg-muted rounded-t-lg overflow-hidden">
                <img 
                  src={gig.image} 
                  alt={gig.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-4">
                <div>
                  <CardTitle className="text-lg group-hover:gradient-text transition-colors mb-2">
                    {gig.title}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {gig.description}
                  </p>
                </div>

                <div className="flex items-center gap-3">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="/placeholder.svg" />
                    <AvatarFallback className="bg-gradient-instagram text-white text-xs">
                      {gig.creator.split(' ').map(n => n[0]).join('')}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="text-sm font-medium">{gig.creator}</p>
                    <div className="flex items-center gap-1">
                      <Star className="w-3 h-3 text-yellow-500 fill-current" />
                      <span className="text-xs">{gig.rating} ({gig.reviews})</span>
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1">
                  {gig.tags.map((tag, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>

                <div className="flex items-center justify-between pt-2 border-t">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    {gig.deliveryTime}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Starting at</span>
                    <span className="text-lg font-bold gradient-text">
                      ${gig.startingPrice}
                    </span>
                  </div>
                </div>

                <Link to={`/gigs/${gig.id}`} className="block">
                  <Button className="w-full btn-gradient">
                    View Details
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Gigs;
