
import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

const WalletPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">My Wallet</h1>
        <div className="text-center mb-6">
          <div className="text-4xl font-bold text-white mb-2">$250.00</div>
          <div className="text-white/70">Available Balance</div>
        </div>
        <div className="flex space-x-4 justify-center">
          <Button variant="gradient">Add Funds</Button>
          <Button variant="outline" className="text-white border-white/30">
            Withdraw
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default WalletPage;
