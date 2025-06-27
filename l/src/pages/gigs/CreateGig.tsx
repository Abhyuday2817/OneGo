
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Upload, Plus, X, Save, Eye } from 'lucide-react';

const CreateGig = () => {
  const [gigData, setGigData] = useState({
    title: '',
    description: '',
    category: '',
    tags: [],
    price: '',
    deliveryTime: ''
  });

  const [packages, setPackages] = useState([
    { name: 'Basic', price: '', delivery: '', features: [''] }
  ]);

  const addPackage = () => {
    setPackages([...packages, { name: '', price: '', delivery: '', features: [''] }]);
  };

  const addFeature = (packageIndex) => {
    const newPackages = [...packages];
    newPackages[packageIndex].features.push('');
    setPackages(newPackages);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-4">
            Create New Gig
          </h1>
          <p className="text-muted-foreground text-lg">
            Showcase your skills and start earning by offering services
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Gig Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Gig Title</label>
                  <Input
                    placeholder="I will..."
                    value={gigData.title}
                    onChange={(e) => setGigData({...gigData, title: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Description</label>
                  <Textarea
                    placeholder="Describe your service in detail..."
                    rows={4}
                    value={gigData.description}
                    onChange={(e) => setGigData({...gigData, description: e.target.value})}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Category</label>
                    <Select value={gigData.category} onValueChange={(value) => setGigData({...gigData, category: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="web-development">Web Development</SelectItem>
                        <SelectItem value="graphic-design">Graphic Design</SelectItem>
                        <SelectItem value="digital-marketing">Digital Marketing</SelectItem>
                        <SelectItem value="writing">Writing & Translation</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Delivery Time</label>
                    <Select value={gigData.deliveryTime} onValueChange={(value) => setGigData({...gigData, deliveryTime: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select delivery time" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="24-hours">24 Hours</SelectItem>
                        <SelectItem value="3-days">3 Days</SelectItem>
                        <SelectItem value="7-days">7 Days</SelectItem>
                        <SelectItem value="14-days">14 Days</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Gallery */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Gig Gallery</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                    <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground mb-4">Upload main image</p>
                    <Button variant="outline">Choose Image</Button>
                  </div>
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                    <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground mb-4">Upload additional images</p>
                    <Button variant="outline">Choose Images</Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Packages */}
            <Card className="glass-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Pricing Packages</CardTitle>
                  <Button onClick={addPackage} size="sm" className="btn-gradient">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Package
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {packages.map((pkg, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="font-semibold">Package {index + 1}</h3>
                      {packages.length > 1 && (
                        <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-700">
                          <X className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <Input placeholder="Package name" />
                      <Input placeholder="Price ($)" type="number" />
                      <Input placeholder="Delivery time" />
                    </div>
                    <div className="space-y-2">
                      <label className="block text-sm font-medium">Features</label>
                      {pkg.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex gap-2">
                          <Input placeholder="Feature description" className="flex-1" />
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => addFeature(index)}
                          >
                            <Plus className="w-4 h-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="glass-card border-gradient-instagram">
              <CardHeader>
                <CardTitle>Gig Preview</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                  <Upload className="w-8 h-8 text-muted-foreground" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    {gigData.title || 'Your gig title will appear here'}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {gigData.description || 'Your gig description will appear here...'}
                  </p>
                </div>
                {gigData.category && (
                  <Badge className="bg-gradient-instagram text-white">
                    {gigData.category}
                  </Badge>
                )}
                <div className="text-2xl font-bold gradient-text">
                  Starting at ${gigData.price || '0'}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-3">
              <Button className="w-full btn-gradient">
                <Save className="w-4 h-4 mr-2" />
                Publish Gig
              </Button>
              <Button variant="outline" className="w-full">
                <Eye className="w-4 h-4 mr-2" />
                Preview Gig
              </Button>
              <Button variant="ghost" className="w-full">
                Save as Draft
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateGig;
