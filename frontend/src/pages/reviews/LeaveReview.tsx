
import React from 'react';
import Card from '../../components/ui/Card';

const LeaveReview: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Leave a Review</h1>
        <p className="text-white/70">
          Share your experience with this mentor or course.
        </p>
      </Card>
    </div>
  );
};

export default LeaveReview;
