
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Edit, Trash2, Eye, Plus, BarChart3, DollarSign, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

const MyGigs = () => {
  const [activeTab, setActiveTab] = useState('active');

  const activeGigs = [
    {
      id: 1,
      title: 'Professional Website Development',
      category: 'Web Development',
      price: 299,
      orders: 15,
      rating: 4.9,
      status: 'active',
      revenue: 4485,
      impressions: 1240
    },
    {
      id: 2,
      title: 'Logo Design & Branding',
      category: 'Graphic Design',
      price: 150,
      orders: 23,
      rating: 4.8,
      status: 'active',
      revenue: 3450,
      impressions: 890
    }
  ];

  const draftGigs = [
    {
      id: 3,
      title: 'SEO Optimization Service',
      category: 'Digital Marketing',
      price: 199,
      status: 'draft'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            My Gigs
          </h1>
          <p className="text-muted-foreground">
            Manage your services and track performance
          </p>
        </div>
        <Link to="/gigs/create">
          <Button className="btn-gradient">
            <Plus className="w-4 h-4 mr-2" />
            Create New Gig
          </Button>
        </Link>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="glass-card">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-instagram rounded-full flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">$7,935</p>
                <p className="text-sm text-muted-foreground">Total Revenue</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="glass-card">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-onlyfans rounded-full flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">38</p>
                <p className="text-sm text-muted-foreground">Active Orders</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="glass-card">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-instagram rounded-full flex items-center justify-center">
                <Eye className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">2,130</p>
                <p className="text-sm text-muted-foreground">Total Views</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="glass-card">
          <CardContent className="p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-onlyfans rounded-full flex items-center justify-center">
                <Clock className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-2xl font-bold gradient-text">4.8</p>
                <p className="text-sm text-muted-foreground">Avg Rating</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-8">
          <TabsTrigger value="active">Active Gigs</TabsTrigger>
          <TabsTrigger value="draft">Drafts</TabsTrigger>
          <TabsTrigger value="paused">Paused</TabsTrigger>
        </TabsList>

        <TabsContent value="active">
          <div className="grid gap-6">
            {activeGigs.map((gig) => (
              <Card key={gig.id} className="glass-card border-gradient-instagram">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-semibold mb-2">{gig.title}</h3>
                          <div className="flex items-center gap-2 mb-2">
                            <Badge className="bg-gradient-instagram text-white">
                              {gig.category}
                            </Badge>
                            <Badge variant="outline" className="text-green-600 border-green-600">
                              {gig.status}
                            </Badge>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold gradient-text mb-1">
                            ${gig.price}
                          </p>
                          <p className="text-sm text-muted-foreground">Starting price</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-muted-foreground">Orders</p>
                          <p className="font-semibold">{gig.orders}</p>
                        </div>
                        <div>
                          <p className="text-sm text-muted-foreground">Revenue</p>
                          <p className="font-semibold">${gig.revenue}</p>
                        </div>
                        <div>
                          <p className="text-sm text-muted-foreground">Rating</p>
                          <p className="font-semibold">{gig.rating}⭐</p>
                        </div>
                        <div>
                          <p className="text-sm text-muted-foreground">Views</p>
                          <p className="font-semibold">{gig.impressions}</p>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2 ml-6">
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button variant="outline" size="sm" className="text-red-500 hover:text-red-700">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="draft">
          <div className="grid gap-6">
            {draftGigs.map((gig) => (
              <Card key={gig.id} className="glass-card">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{gig.title}</h3>
                      <div className="flex items-center gap-2">
                        <Badge className="bg-gradient-instagram text-white">
                          {gig.category}
                        </Badge>
                        <Badge variant="outline" className="text-yellow-600 border-yellow-600">
                          {gig.status}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4 mr-2" />
                        Edit
                      </Button>
                      <Button className="btn-gradient" size="sm">
                        Publish
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="paused">
          <div className="text-center py-12">
            <p className="text-muted-foreground">No paused gigs</p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MyGigs;
