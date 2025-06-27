
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Video, Calendar, Clock, Users } from 'lucide-react';

const Sessions = () => {
  const sessions = [
    {
      id: 1,
      title: 'React Development Workshop',
      mentor: 'Sarah Johnson',
      date: '2024-01-20',
      time: '10:00 AM',
      duration: 90,
      participants: 15,
      maxParticipants: 20,
      status: 'upcoming'
    },
    {
      id: 2,
      title: 'UI/UX Design Masterclass',
      mentor: 'Emily Rodriguez',
      date: '2024-01-18',
      time: '2:00 PM',
      duration: 120,
      participants: 8,
      maxParticipants: 12,
      status: 'completed'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          Live Sessions
        </h1>
        <p className="text-muted-foreground">
          Join interactive group sessions and workshops
        </p>
      </div>

      <div className="grid gap-6">
        {sessions.map((session) => (
          <Card key={session.id} className="glass-card border-gradient-instagram">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold mb-2">{session.title}</h3>
                      <p className="text-muted-foreground mb-2">
                        Hosted by {session.mentor}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {session.date}
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {session.time} ({session.duration} min)
                        </div>
                        <div className="flex items-center gap-1">
                          <Users className="w-4 h-4" />
                          {session.participants}/{session.maxParticipants} participants
                        </div>
                      </div>
                    </div>
                    <Badge 
                      className={session.status === 'upcoming' ? 'bg-green-500' : 'bg-gray-500'}
                    >
                      {session.status}
                    </Badge>
                  </div>
                </div>
                <div className="ml-6">
                  <Button className="btn-gradient">
                    <Video className="w-4 h-4 mr-2" />
                    {session.status === 'upcoming' ? 'Join Session' : 'View Recording'}
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

export default Sessions;
