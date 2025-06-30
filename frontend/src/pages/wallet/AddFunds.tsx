
import React from 'react';
import Card from '../../components/ui/Card';

const AddFunds: React.FC = () => {
  return (
    <div className="max-w-2xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Add Funds</h1>
        <p className="text-white/70">
          Add money to your wallet to book sessions and purchase courses.
        </p>
      </Card>
    </div>
  );
};

export default AddFunds;
