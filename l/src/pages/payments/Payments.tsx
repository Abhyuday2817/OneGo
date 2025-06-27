
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CreditCard, DollarSign, TrendingUp, Calendar, Download } from 'lucide-react';

const Payments = () => {
  const transactions = [
    {
      id: 1,
      type: 'payment',
      description: 'Consultation with Sarah Johnson',
      amount: -75,
      date: '2024-01-15',
      status: 'completed'
    },
    {
      id: 2,
      type: 'earning',
      description: 'Course purchase: React Masterclass',
      amount: 99,
      date: '2024-01-14',
      status: 'completed'
    },
    {
      id: 3,
      type: 'payment',
      description: 'Gig: Website Development',
      amount: -299,
      date: '2024-01-12',
      status: 'pending'
    }
  ];

  const stats = [
    {
      title: 'Total Earnings',
      value: '$2,847',
      icon: TrendingUp,
      color: 'bg-gradient-instagram'
    },
    {
      title: 'Total Spent',
      value: '$1,243',
      icon: DollarSign,
      color: 'bg-gradient-onlyfans'
    },
    {
      title: 'Pending',
      value: '$156',
      icon: Calendar,
      color: 'bg-gradient-to-r from-purple-500 to-pink-500'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-display font-bold gradient-text mb-2">
          Payments
        </h1>
        <p className="text-muted-foreground">
          Track your earnings, expenses, and payment history
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat, index) => (
          <Card key={index} className="glass-card">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 ${stat.color} rounded-full flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold gradient-text">{stat.value}</p>
                  <p className="text-sm text-muted-foreground">{stat.title}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="all" className="w-full">
        <div className="flex items-center justify-between mb-6">
          <TabsList>
            <TabsTrigger value="all">All Transactions</TabsTrigger>
            <TabsTrigger value="earnings">Earnings</TabsTrigger>
            <TabsTrigger value="payments">Payments</TabsTrigger>
          </TabsList>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>

        <TabsContent value="all">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Recent Transactions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {transactions.map((transaction) => (
                  <div key={transaction.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        transaction.type === 'earning' ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        <CreditCard className={`w-5 h-5 ${
                          transaction.type === 'earning' ? 'text-green-600' : 'text-red-600'
                        }`} />
                      </div>
                      <div>
                        <h3 className="font-semibold">{transaction.description}</h3>
                        <p className="text-sm text-muted-foreground">{transaction.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge 
                        className={transaction.status === 'completed' ? 'bg-green-500' : 'bg-yellow-500'}
                      >
                        {transaction.status}
                      </Badge>
                      <div className={`text-lg font-semibold ${
                        transaction.amount > 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.amount > 0 ? '+' : ''}${Math.abs(transaction.amount)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="earnings">
          <Card className="glass-card">
            <CardContent className="p-6">
              <p className="text-center text-muted-foreground">Earnings transactions will be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="payments">
          <Card className="glass-card">
            <CardContent className="p-6">
              <p className="text-center text-muted-foreground">Payment transactions will be displayed here</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Payments;
