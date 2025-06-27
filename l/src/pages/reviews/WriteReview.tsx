
import { useParams } from 'react-router-dom';
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Star, Send } from 'lucide-react';

const WriteReview = () => {
  const { type, id } = useParams();
  const [rating, setRating] = useState(0);
  const [review, setReview] = useState('');

  const serviceDetails = {
    mentor: 'Sarah Johnson',
    service: 'Career Consultation',
    date: '2024-01-15',
    duration: '60 minutes'
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Write a Review
          </h1>
          <p className="text-muted-foreground">
            Share your experience to help others
          </p>
        </div>

        <Card className="glass-card border-gradient-instagram">
          <CardHeader>
            <CardTitle>Review Your Experience</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Service Details */}
            <div className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg">
              <Avatar className="w-16 h-16">
                <AvatarImage src="/placeholder.svg" />
                <AvatarFallback className="bg-gradient-instagram text-white">
                  SJ
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-semibold text-lg">{serviceDetails.service}</h3>
                <p className="text-muted-foreground">with {serviceDetails.mentor}</p>
                <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                  <span>{serviceDetails.date}</span>
                  <span>{serviceDetails.duration}</span>
                </div>
              </div>
            </div>

            {/* Rating */}
            <div>
              <label className="block text-sm font-medium mb-3">
                How would you rate this experience?
              </label>
              <div className="flex items-center gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setRating(star)}
                    className="transition-colors"
                  >
                    <Star
                      className={`w-8 h-8 ${
                        star <= rating 
                          ? 'text-yellow-500 fill-current' 
                          : 'text-gray-300 hover:text-yellow-400'
                      }`}
                    />
                  </button>
                ))}
                {rating > 0 && (
                  <span className="ml-2 font-medium">
                    {rating === 1 && 'Poor'}
                    {rating === 2 && 'Fair'}
                    {rating === 3 && 'Good'}
                    {rating === 4 && 'Very Good'}
                    {rating === 5 && 'Excellent'}
                  </span>
                )}
              </div>
            </div>

            {/* Written Review */}
            <div>
              <label className="block text-sm font-medium mb-2">
                Share your experience (optional)
              </label>
              <Textarea
                placeholder="Tell others about your experience..."
                value={review}
                onChange={(e) => setReview(e.target.value)}
                rows={4}
              />
              <p className="text-xs text-muted-foreground mt-2">
                Your review will be visible to other users
              </p>
            </div>

            {/* Tips */}
            <div className="bg-gradient-to-r from-instagram-500/10 to-onlyfans-500/10 rounded-lg p-4">
              <h4 className="font-semibold mb-2">Tips for a helpful review:</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Be specific about what you liked or didn't like</li>
                <li>• Mention the mentor's communication style</li>
                <li>• Share what you learned or achieved</li>
                <li>• Be honest and constructive</li>
              </ul>
            </div>

            {/* Submit */}
            <div className="flex gap-4">
              <Button 
                className="flex-1 btn-gradient"
                disabled={rating === 0}
              >
                <Send className="w-4 h-4 mr-2" />
                Submit Review
              </Button>
              <Button variant="outline" className="flex-1">
                Skip Review
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default WriteReview;
