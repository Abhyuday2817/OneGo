
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Star, Calendar, MessageCircle, Video, MapPin } from 'lucide-react';

const MentorProfile = () => {
  const { id } = useParams();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Mentor Info */}
        <div className="lg:col-span-2">
          <Card className="glass-card border-gradient-instagram">
            <CardHeader>
              <div className="flex items-start gap-6">
                <Avatar className="w-24 h-24">
                  <AvatarImage src="/placeholder.svg" />
                  <AvatarFallback className="bg-gradient-instagram text-white text-2xl">
                    JD
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <CardTitle className="text-3xl gradient-text mb-2">
                    John Doe
                  </CardTitle>
                  <p className="text-muted-foreground mb-3">
                    Senior Software Engineer at Tech Corp
                  </p>
                  <div className="flex items-center gap-2 mb-3">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="font-semibold">4.9</span>
                    <span className="text-muted-foreground">(124 reviews)</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Badge className="bg-gradient-instagram text-white">React</Badge>
                    <Badge className="bg-gradient-onlyfans text-white">Node.js</Badge>
                    <Badge variant="outline">TypeScript</Badge>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-lg mb-2">About</h3>
                  <p className="text-muted-foreground">
                    Experienced software developer with 8+ years in full-stack development. 
                    Passionate about mentoring junior developers and helping them grow their careers.
                  </p>
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-2">Expertise</h3>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gradient-instagram rounded-full"></div>
                      <span>Frontend Development</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gradient-onlyfans rounded-full"></div>
                      <span>Backend Development</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gradient-instagram rounded-full"></div>
                      <span>System Design</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gradient-onlyfans rounded-full"></div>
                      <span>Career Guidance</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Booking Panel */}
        <div>
          <Card className="sticky top-4">
            <CardHeader>
              <CardTitle>Book a Session</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span>1-on-1 Consultation</span>
                  <span className="font-semibold">$50/hour</span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Code Review</span>
                  <span className="font-semibold">$30/hour</span>
                </div>
              </div>
              <Button className="w-full btn-gradient">
                <Calendar className="w-4 h-4 mr-2" />
                Book Consultation
              </Button>
              <Button variant="outline" className="w-full">
                <MessageCircle className="w-4 h-4 mr-2" />
                Send Message
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default MentorProfile;
