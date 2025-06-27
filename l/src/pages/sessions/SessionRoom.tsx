
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { 
  Video, 
  VideoOff, 
  Mic, 
  MicOff, 
  Phone, 
  MessageCircle, 
  Users,
  Settings,
  Share2
} from 'lucide-react';

const SessionRoom = () => {
  const { id } = useParams();

  const participants = [
    { id: 1, name: 'Sarah Johnson', role: 'Host', avatar: '/placeholder.svg' },
    { id: 2, name: 'You', role: 'Participant', avatar: '/placeholder.svg' },
    { id: 3, name: 'Mike Chen', role: 'Participant', avatar: '/placeholder.svg' },
    { id: 4, name: 'Emily Davis', role: 'Participant', avatar: '/placeholder.svg' }
  ];

  return (
    <div className="h-screen bg-background flex flex-col">
      {/* Header */}
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">React Development Workshop</h1>
            <p className="text-sm text-muted-foreground">Hosted by Sarah Johnson</p>
          </div>
          <div className="flex items-center gap-2">
            <Badge className="bg-green-500">Live</Badge>
            <Badge variant="outline">
              <Users className="w-3 h-3 mr-1" />
              {participants.length} participants
            </Badge>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Video Area */}
        <div className="flex-1 p-4">
          <div className="h-full bg-black rounded-lg relative overflow-hidden">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center text-white">
                <Video className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg">Session video will appear here</p>
              </div>
            </div>
            
            {/* Host Badge */}
            <div className="absolute top-4 left-4">
              <Badge className="bg-gradient-instagram text-white">
                Sarah Johnson (Host)
              </Badge>
            </div>

            {/* Controls */}
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
              <div className="flex items-center gap-4 bg-black/50 backdrop-blur-sm rounded-lg p-4">
                <Button size="sm" variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  <Mic className="w-4 h-4" />
                </Button>
                <Button size="sm" variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  <Video className="w-4 h-4" />
                </Button>
                <Button size="sm" variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  <Settings className="w-4 h-4" />
                </Button>
                <Button size="sm" variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
                  <Share2 className="w-4 h-4" />
                </Button>
                <Button size="sm" variant="destructive">
                  <Phone className="w-4 h-4 mr-2" />
                  Leave
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-80 border-l bg-muted/20">
          <div className="h-full flex flex-col">
            {/* Participants */}
            <Card className="flex-1 m-4 glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  Participants ({participants.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {participants.map((participant) => (
                  <div key={participant.id} className="flex items-center gap-3">
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={participant.avatar} />
                      <AvatarFallback className="bg-gradient-instagram text-white text-xs">
                        {participant.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{participant.name}</p>
                      <p className="text-xs text-muted-foreground">{participant.role}</p>
                    </div>
                    {participant.role === 'Host' && (
                      <Badge variant="outline" className="text-xs">Host</Badge>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Chat */}
            <Card className="flex-1 m-4 glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center gap-2">
                  <MessageCircle className="w-5 h-5" />
                  Chat
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mb-4">
                  <div className="text-sm">
                    <span className="font-medium">Sarah Johnson:</span>
                    <span className="text-muted-foreground ml-2">Welcome everyone!</span>
                  </div>
                  <div className="text-sm">
                    <span className="font-medium">Mike Chen:</span>
                    <span className="text-muted-foreground ml-2">Thanks for hosting this session</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <input 
                    placeholder="Type a message..." 
                    className="flex-1 px-3 py-2 text-sm border rounded-md bg-background"
                  />
                  <Button size="sm" className="btn-gradient">Send</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionRoom;
