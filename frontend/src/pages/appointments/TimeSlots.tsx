
import React from 'react';
import Card from '../../components/ui/Card';

const TimeSlots: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Available Time Slots</h1>
        <p className="text-white/70">
          Select from available time slots below.
        </p>
      </Card>
    </div>
  );
};

export default TimeSlots;
