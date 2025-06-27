
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, Clock, RefreshCw, Shield, MessageCircle, Heart } from 'lucide-react';

const GigDetail = () => {
  const { id } = useParams();

  const gig = {
    title: 'Website Design & Development',
    description: 'I will create a modern, responsive website for your business with custom design and functionality.',
    creator: {
      name: 'Emily Rodriguez',
      avatar: '/placeholder.svg',
      rating: 4.9,
      reviews: 87,
      level: 'Top Rated',
      responseTime: '1 hour'
    },
    gallery: ['/placeholder.svg', '/placeholder.svg', '/placeholder.svg'],
    packages: [
      {
        name: 'Basic',
        price: 299,
        delivery: '3 days',
        features: ['Responsive Design', '3 Pages', 'Basic SEO', 'Mobile Optimized']
      },
      {
        name: 'Standard',
        price: 599,
        delivery: '5 days',
        features: ['Everything in Basic', '5 Pages', 'Contact Form', 'CMS Integration', 'Social Media Integration']
      },
      {
        name: 'Premium',
        price: 999,
        delivery: '7 days',
        features: ['Everything in Standard', '10 Pages', 'E-commerce', 'Advanced SEO', 'Analytics Setup', '30 Days Support']
      }
    ]
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          {/* Gallery */}
          <div className="aspect-video bg-muted rounded-lg overflow-hidden mb-8">
            <img 
              src={gig.gallery[0]} 
              alt={gig.title}
              className="w-full h-full object-cover"
            />
          </div>

          {/* Gig Info */}
          <div className="mb-8">
            <h1 className="text-3xl font-display font-bold gradient-text mb-4">
              {gig.title}
            </h1>
            
            {/* Creator Info */}
            <div className="flex items-center gap-4 mb-6">
              <Avatar className="w-12 h-12">
                <AvatarImage src={gig.creator.avatar} />
                <AvatarFallback className="bg-gradient-instagram text-white">
                  ER
                </AvatarFallback>
              </Avatar>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{gig.creator.name}</h3>
                  <Badge className="bg-gradient-instagram text-white">{gig.creator.level}</Badge>
                </div>
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    {gig.creator.rating} ({gig.creator.reviews} reviews)
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    Responds in {gig.creator.responseTime}
                  </div>
                </div>
              </div>
            </div>

            <p className="text-muted-foreground text-lg leading-relaxed">
              {gig.description}
            </p>
          </div>

          {/* Tabs */}
          <Tabs defaultValue="details" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="details">Details</TabsTrigger>
              <TabsTrigger value="reviews">Reviews</TabsTrigger>
              <TabsTrigger value="about">About Seller</TabsTrigger>
            </TabsList>
            
            <TabsContent value="details" className="space-y-4">
              <Card className="glass-card">
                <CardHeader>
                  <CardTitle>What You'll Get</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span>Professional website design</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span>Responsive mobile-first approach</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span>SEO optimization</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-500" />
                      <span>Cross-browser compatibility</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="reviews">
              <Card className="glass-card">
                <CardContent className="p-6">
                  <p className="text-muted-foreground">Reviews will be displayed here...</p>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="about">
              <Card className="glass-card">
                <CardContent className="p-6">
                  <p className="text-muted-foreground">Seller information will be displayed here...</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar - Packages */}
        <div className="space-y-6">
          {gig.packages.map((pkg, index) => (
            <Card key={index} className={`glass-card ${index === 1 ? 'border-gradient-instagram' : ''}`}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{pkg.name}</CardTitle>
                  {index === 1 && <Badge className="bg-gradient-instagram text-white">Popular</Badge>}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold gradient-text mb-2">
                    ${pkg.price}
                  </div>
                  <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    {pkg.delivery} delivery
                  </div>
                </div>

                <ul className="space-y-2 text-sm">
                  {pkg.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-green-500 flex-shrink-0" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <div className="space-y-2">
                  <Button className="w-full btn-gradient">
                    Continue (${pkg.price})
                  </Button>
                  <Button variant="outline" className="w-full">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Contact Seller
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}

          {/* Seller Actions */}
          <div className="flex gap-2">
            <Button variant="outline" className="flex-1">
              <Heart className="w-4 h-4 mr-2" />
              Save
            </Button>
            <Button variant="outline" className="flex-1">
              <RefreshCw className="w-4 h-4 mr-2" />
              Share
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GigDetail;
