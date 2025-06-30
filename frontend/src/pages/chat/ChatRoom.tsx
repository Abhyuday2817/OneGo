
import React from 'react';
import Card from '../../components/ui/Card';

const ChatRoom: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Messages</h1>
        <p className="text-white/70">
          Your conversations will appear here.
        </p>
      </Card>
    </div>
  );
};

export default ChatRoom;
