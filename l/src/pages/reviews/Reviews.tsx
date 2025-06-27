
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Star, Filter, ThumbsUp, MessageCircle } from 'lucide-react';

const Reviews = () => {
  const receivedReviews = [
    {
      id: 1,
      reviewer: 'Mike Chen',
      rating: 5,
      comment: 'Excellent mentor! Sarah provided great insights and practical advice.',
      service: 'Career Consultation',
      date: '2024-01-15',
      helpful: 12
    },
    {
      id: 2,
      reviewer: 'Emily Davis',
      rating: 4,
      comment: 'Very knowledgeable and patient. Helped me understand complex concepts.',
      service: 'React Course',
      date: '2024-01-12',
      helpful: 8
    }
  ];

  const givenReviews = [
    {
      id: 3,
      reviewee: 'John Doe',
      rating: 5,
      comment: 'Great developer! Delivered exactly what I needed on time.',
      service: 'Website Development',
      date: '2024-01-10'
    }
  ];

  const ReviewCard = ({ review, type = 'received' }) => (
    <Card className="glass-card mb-4">
      <CardContent className="p-6">
        <div className="flex items-start gap-4">
          <Avatar>
            <AvatarImage src="/placeholder.svg" />
            <AvatarFallback className="bg-gradient-instagram text-white">
              {review[type === 'received' ? 'reviewer' : 'reviewee']?.split(' ').map(n => n[0]).join('')}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <div>
                <h3 className="font-semibold">
                  {review[type === 'received' ? 'reviewer' : 'reviewee']}
                </h3>
                <div className="flex items-center gap-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-4 h-4 ${
                          i < review.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <Badge variant="outline">{review.service}</Badge>
                </div>
              </div>
              <span className="text-sm text-muted-foreground">{review.date}</span>
            </div>
            <p className="text-muted-foreground mb-4">{review.comment}</p>
            {type === 'received' && review.helpful && (
              <div className="flex items-center gap-4">
                <Button variant="ghost" size="sm">
                  <ThumbsUp className="w-4 h-4 mr-1" />
                  {review.helpful} helpful
                </Button>
                <Button variant="ghost" size="sm">
                  <MessageCircle className="w-4 h-4 mr-1" />
                  Reply
                </Button>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-display font-bold gradient-text mb-2">
              Reviews
            </h1>
            <p className="text-muted-foreground">
              Manage your reviews and feedback
            </p>
          </div>
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </Button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="glass-card">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold gradient-text mb-2">4.9</div>
              <p className="text-sm text-muted-foreground">Average Rating</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold gradient-text mb-2">127</div>
              <p className="text-sm text-muted-foreground">Total Reviews</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold gradient-text mb-2">98%</div>
              <p className="text-sm text-muted-foreground">Positive</p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold gradient-text mb-2">15</div>
              <p className="text-sm text-muted-foreground">This Month</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="received" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="received">Reviews Received</TabsTrigger>
            <TabsTrigger value="given">Reviews Given</TabsTrigger>
          </TabsList>

          <TabsContent value="received">
            <div>
              {receivedReviews.map((review) => (
                <ReviewCard key={review.id} review={review} type="received" />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="given">
            <div>
              {givenReviews.map((review) => (
                <ReviewCard key={review.id} review={review} type="given" />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Reviews;
