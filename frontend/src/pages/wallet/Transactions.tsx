
import React from 'react';
import Card from '../../components/ui/Card';

const Transactions: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Transaction History</h1>
        <p className="text-white/70">
          Your transaction history will appear here.
        </p>
      </Card>
    </div>
  );
};

export default Transactions;
