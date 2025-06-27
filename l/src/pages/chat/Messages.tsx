
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { MessageCircle, Clock, Star } from 'lucide-react';
import { Link } from 'react-router-dom';

const Messages = () => {
  const messageThreads = [
    {
      id: 1,
      participant: 'Sarah Johnson',
      lastMessage: 'Looking forward to our next session!',
      time: '2 hours ago',
      unread: 3,
      type: 'consultation',
      avatar: '/placeholder.svg'
    },
    {
      id: 2,
      participant: 'Mike Chen',
      lastMessage: 'The code review was very helpful',
      time: '1 day ago',
      unread: 0,
      type: 'mentoring',
      avatar: '/placeholder.svg'
    },
    {
      id: 3,
      participant: 'Emily Rodriguez',
      lastMessage: 'Project completed successfully!',
      time: '3 days ago',
      unread: 1,
      type: 'gig',
      avatar: '/placeholder.svg'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Messages
          </h1>
          <p className="text-muted-foreground">
            Stay connected with your mentors and clients
          </p>
        </div>

        <div className="space-y-4">
          {messageThreads.map((thread) => (
            <Card key={thread.id} className="glass-card hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="p-6">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <Avatar className="w-16 h-16">
                      <AvatarImage src={thread.avatar} />
                      <AvatarFallback className="bg-gradient-instagram text-white">
                        {thread.participant.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    {thread.unread > 0 && (
                      <div className="absolute -top-1 -right-1 w-6 h-6 bg-gradient-instagram rounded-full flex items-center justify-center">
                        <span className="text-white text-xs font-bold">{thread.unread}</span>
                      </div>
                    )}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-semibold text-lg">{thread.participant}</h3>
                        <div className="flex items-center gap-2">
                          <Badge 
                            className={
                              thread.type === 'consultation' ? 'bg-gradient-instagram text-white' :
                              thread.type === 'mentoring' ? 'bg-gradient-onlyfans text-white' :
                              'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                            }
                          >
                            {thread.type}
                          </Badge>
                          <div className="flex items-center gap-1 text-sm text-muted-foreground">
                            <Clock className="w-4 h-4" />
                            {thread.time}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Star className="w-4 h-4 text-yellow-500 fill-current" />
                        <span className="text-sm">4.9</span>
                      </div>
                    </div>
                    
                    <p className="text-muted-foreground mb-4">
                      {thread.lastMessage}
                    </p>

                    <div className="flex gap-2">
                      <Link to="/chat" className="flex-1">
                        <Button className="w-full btn-gradient">
                          <MessageCircle className="w-4 h-4 mr-2" />
                          Open Chat
                        </Button>
                      </Link>
                      <Button variant="outline">
                        Archive
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Empty State */}
        {messageThreads.length === 0 && (
          <Card className="glass-card">
            <CardContent className="p-12 text-center">
              <MessageCircle className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">No messages yet</h3>
              <p className="text-muted-foreground">
                Start connecting with mentors and clients to see your conversations here.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Messages;
