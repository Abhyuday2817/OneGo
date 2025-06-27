
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { CreditCard, DollarSign, ArrowUpRight, ArrowDownLeft, Plus, Minus } from 'lucide-react';

const Wallet = () => {
  const balance = 2847.50;
  const pendingEarnings = 156.75;

  const recentTransactions = [
    {
      id: 1,
      type: 'credit',
      description: 'Course sale: React Development',
      amount: 99,
      date: '2024-01-15'
    },
    {
      id: 2,
      type: 'debit',
      description: 'Consultation payment',
      amount: -75,
      date: '2024-01-14'
    },
    {
      id: 3,
      type: 'credit',
      description: 'Gig completion: Logo Design',
      amount: 150,
      date: '2024-01-13'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-2">
            Wallet
          </h1>
          <p className="text-muted-foreground">
            Manage your balance and transactions
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Wallet Balance */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="glass-card border-gradient-instagram">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <CreditCard className="w-6 h-6" />
                  Wallet Balance
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <div className="text-5xl font-bold gradient-text mb-4">
                    ${balance.toFixed(2)}
                  </div>
                  <div className="flex items-center justify-center gap-2 text-muted-foreground mb-6">
                    <Badge variant="outline">
                      ${pendingEarnings.toFixed(2)} pending
                    </Badge>
                  </div>
                  <div className="flex gap-4 justify-center">
                    <Button className="btn-gradient">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Funds
                    </Button>
                    <Button variant="outline">
                      <Minus className="w-4 h-4 mr-2" />
                      Withdraw
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recent Transactions */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentTransactions.map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          transaction.type === 'credit' ? 'bg-green-100' : 'bg-red-100'
                        }`}>
                          {transaction.type === 'credit' ? (
                            <ArrowDownLeft className="w-5 h-5 text-green-600" />
                          ) : (
                            <ArrowUpRight className="w-5 h-5 text-red-600" />
                          )}
                        </div>
                        <div>
                          <h3 className="font-medium">{transaction.description}</h3>
                          <p className="text-sm text-muted-foreground">{transaction.date}</p>
                        </div>
                      </div>
                      <div className={`font-semibold ${
                        transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.type === 'credit' ? '+' : ''}${Math.abs(transaction.amount)}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Add Funds</label>
                  <div className="flex gap-2">
                    <Input placeholder="Amount" type="number" />
                    <Button className="btn-gradient">Add</Button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Withdraw</label>
                  <div className="flex gap-2">
                    <Input placeholder="Amount" type="number" />
                    <Button variant="outline">Withdraw</Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Payment Methods</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3 p-3 border rounded-lg">
                  <CreditCard className="w-5 h-5 text-muted-foreground" />
                  <div className="flex-1">
                    <p className="font-medium">**** 4242</p>
                    <p className="text-sm text-muted-foreground">Expires 12/26</p>
                  </div>
                  <Badge variant="outline">Primary</Badge>
                </div>
                <Button variant="outline" className="w-full">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Payment Method
                </Button>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Quick Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">This Month</span>
                  <span className="font-semibold text-green-600">+$1,247</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Last Month</span>
                  <span className="font-semibold">$983</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Total Earned</span>
                  <span className="font-semibold gradient-text">$12,843</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Wallet;
