
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Calendar, Clock, Video, Star, Filter } from 'lucide-react';

const Consultations = () => {
  const consultations = [
    {
      id: 1,
      mentor: 'Sarah Johnson',
      title: 'Career Growth Strategy',
      date: '2024-01-15',
      time: '10:00 AM',
      duration: 60,
      price: 75,
      status: 'upcoming',
      type: 'video'
    },
    {
      id: 2,
      mentor: 'Mike Chen',
      title: 'Code Review Session',
      date: '2024-01-12',
      time: '2:00 PM',
      duration: 45,
      price: 60,
      status: 'completed',
      type: 'video'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Consultations
          </h1>
          <p className="text-muted-foreground">
            Manage your one-on-one sessions with mentors
          </p>
        </div>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          Filter
        </Button>
      </div>

      <div className="grid gap-6">
        {consultations.map((consultation) => (
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
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <Badge 
                      className={consultation.status === 'upcoming' ? 'bg-green-500' : 'bg-gray-500'}
                    >
                      {consultation.status}
                    </Badge>
                    <p className="text-lg font-semibold gradient-text mt-2">
                      ${consultation.price}
                    </p>
                  </div>
                  <Button className="btn-gradient">
                    {consultation.status === 'upcoming' ? 'Join Call' : 'View Details'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Consultations;
