
import React from 'react';
import Card from '../../components/ui/Card';

const BookingPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Book a Session</h1>
        <p className="text-white/70">
          Choose your preferred time slot and book a session with your mentor.
        </p>
      </Card>
    </div>
  );
};

export default BookingPage;
