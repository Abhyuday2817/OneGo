
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Calendar, Clock, Video, Star, MessageCircle, RefreshCw } from 'lucide-react';

const MyConsultations = () => {
  const [activeTab, setActiveTab] = useState('upcoming');

  const upcomingConsultations = [
    {
      id: 1,
      mentor: 'Sarah Johnson',
      title: 'Product Strategy Discussion',
      date: '2024-01-20',
      time: '10:00 AM',
      duration: 60,
      price: 75,
      type: 'video'
    }
  ];

  const pastConsultations = [
    {
      id: 2,
      mentor: 'Mike Chen',
      title: 'Code Review & Best Practices',
      date: '2024-01-10',
      time: '2:00 PM',
      duration: 45,
      price: 60,
      rating: 5,
      review: 'Excellent session with great insights!'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          My Consultations
        </h1>
        <p className="text-muted-foreground">
          Track your mentoring sessions and progress
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 mb-8">
          <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
          <TabsTrigger value="past">Past Sessions</TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming">
          <div className="space-y-6">
            {upcomingConsultations.map((consultation) => (
              <Card key={consultation.id} className="glass-card border-gradient-instagram">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <Avatar className="w-16 h-16">
                        <AvatarImage src="/placeholder.svg" />
                        <AvatarFallback className="bg-gradient-instagram text-white">
                          {consultation.mentor.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h3 className="text-xl font-semibold">{consultation.title}</h3>
                        <p className="text-muted-foreground">with {consultation.mentor}</p>
                        <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            {consultation.date}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {consultation.time}
                          </div>
                          <div className="flex items-center gap-1">
                            <Video className="w-4 h-4" />
                            {consultation.duration} min
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge className="bg-green-500">Confirmed</Badge>
                      <div className="flex gap-2">
                        <Button variant="outline">
                          <MessageCircle className="w-4 h-4 mr-2" />
                          Message
                        </Button>
                        <Button className="btn-gradient">
                          <Video className="w-4 h-4 mr-2" />
                          Join Call
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="past">
          <div className="space-y-6">
            {pastConsultations.map((consultation) => (
              <Card key={consultation.id} className="glass-card">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <Avatar className="w-16 h-16">
                        <AvatarImage src="/placeholder.svg" />
                        <AvatarFallback className="bg-gradient-instagram text-white">
                          {consultation.mentor.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h3 className="text-xl font-semibold">{consultation.title}</h3>
                        <p className="text-muted-foreground">with {consultation.mentor}</p>
                        <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            {consultation.date}
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            {consultation.time}
                          </div>
                        </div>
                        {consultation.rating && (
                          <div className="flex items-center gap-2 mt-2">
                            <div className="flex items-center gap-1">
                              {[...Array(consultation.rating)].map((_, i) => (
                                <Star key={i} className="w-4 h-4 text-yellow-500 fill-current" />
                              ))}
                            </div>
                            <span className="text-sm text-muted-foreground">
                              "{consultation.review}"
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Badge variant="outline">Completed</Badge>
                      <Button variant="outline">
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Book Again
                      </Button>
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

export default MyConsultations;
