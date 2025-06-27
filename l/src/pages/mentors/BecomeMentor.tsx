
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Users, DollarSign, Clock } from 'lucide-react';

const BecomeMentor = () => {
  const [formData, setFormData] = useState({
    expertise: '',
    experience: '',
    bio: '',
    hourlyRate: ''
  });

  const benefits = [
    {
      icon: DollarSign,
      title: 'Earn Extra Income',
      description: 'Set your own rates and earn money sharing your expertise'
    },
    {
      icon: Users,
      title: 'Build Your Network',
      description: 'Connect with motivated professionals and expand your reach'
    },
    {
      icon: Clock,
      title: 'Flexible Schedule',
      description: 'Mentor on your own time with complete flexibility'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-display font-bold gradient-text mb-4">
            Become a Mentor
          </h1>
          <p className="text-xl text-muted-foreground">
            Share your expertise and help others grow while earning extra income
          </p>
        </div>

        {/* Benefits Section */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {benefits.map((benefit, index) => (
            <Card key={index} className="glass-card text-center">
              <CardHeader>
                <div className="w-16 h-16 bg-gradient-instagram rounded-full flex items-center justify-center mx-auto mb-4">
                  <benefit.icon className="h-8 w-8 text-white" />
                </div>
                <CardTitle className="text-xl">{benefit.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{benefit.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Application Form */}
        <Card className="glass-card border-gradient-instagram">
          <CardHeader>
            <CardTitle className="text-2xl gradient-text">Mentor Application</CardTitle>
            <p className="text-muted-foreground">
              Fill out this form to start your journey as a mentor
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Areas of Expertise
                </label>
                <Input
                  placeholder="e.g., React, Product Management, Data Science"
                  value={formData.expertise}
                  onChange={(e) => setFormData({...formData, expertise: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">
                  Years of Experience
                </label>
                <Input
                  placeholder="e.g., 5+ years"
                  value={formData.experience}
                  onChange={(e) => setFormData({...formData, experience: e.target.value})}
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">
                Professional Bio
              </label>
              <Textarea
                placeholder="Tell us about your background, experience, and what you're passionate about..."
                rows={4}
                value={formData.bio}
                onChange={(e) => setFormData({...formData, bio: e.target.value})}
              />
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Hourly Rate (USD)
                </label>
                <Input
                  type="number"
                  placeholder="50"
                  value={formData.hourlyRate}
                  onChange={(e) => setFormData({...formData, hourlyRate: e.target.value})}
                />
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button className="flex-1 btn-gradient">
                <CheckCircle className="w-4 h-4 mr-2" />
                Submit Application
              </Button>
              <Button variant="outline" className="flex-1">
                Save as Draft
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Requirements */}
        <Card className="mt-8 glass-card">
          <CardHeader>
            <CardTitle>Requirements</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>3+ years of professional experience</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Strong communication skills</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Passion for helping others</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Reliable internet connection</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Available for regular sessions</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Professional background verification</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default BecomeMentor;
