
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, Download, ArrowLeft, Share2 } from 'lucide-react';
import { Link } from 'react-router-dom';

const PaymentSuccess = () => {
  const paymentDetails = {
    amount: 75,
    service: 'Consultation with Sarah Johnson',
    date: '2024-01-15',
    transactionId: 'TXN-2024-001',
    paymentMethod: '**** 4242'
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <Card className="glass-card border-gradient-instagram">
          <CardHeader className="text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-12 h-12 text-green-600" />
            </div>
            <CardTitle className="text-3xl gradient-text mb-2">
              Payment Successful!
            </CardTitle>
            <p className="text-muted-foreground">
              Your payment has been processed successfully
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Payment Details */}
            <div className="bg-muted/50 rounded-lg p-6">
              <h3 className="font-semibold text-lg mb-4">Payment Details</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Service</span>
                  <span className="font-medium">{paymentDetails.service}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Amount</span>
                  <span className="font-semibold text-2xl gradient-text">
                    ${paymentDetails.amount}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Date</span>
                  <span className="font-medium">{paymentDetails.date}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Transaction ID</span>
                  <span className="font-medium font-mono">{paymentDetails.transactionId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Payment Method</span>
                  <span className="font-medium">{paymentDetails.paymentMethod}</span>
                </div>
              </div>
            </div>

            {/* Status */}
            <div className="text-center">
              <Badge className="bg-green-500 text-white mb-4">
                Payment Confirmed
              </Badge>
              <p className="text-sm text-muted-foreground">
                You will receive a confirmation email shortly
              </p>
            </div>

            {/* Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Button variant="outline" className="w-full">
                <Download className="w-4 h-4 mr-2" />
                Download Receipt
              </Button>
              <Button variant="outline" className="w-full">
                <Share2 className="w-4 h-4 mr-2" />
                Share Receipt
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link to="/dashboard" className="w-full">
                <Button variant="outline" className="w-full">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back to Dashboard
                </Button>
              </Link>
              <Link to="/my-consultations" className="w-full">
                <Button className="w-full btn-gradient">
                  View Consultation
                </Button>
              </Link>
            </div>

            {/* What's Next */}
            <div className="bg-gradient-to-r from-instagram-500/10 to-onlyfans-500/10 rounded-lg p-6 text-center">
              <h3 className="font-semibold mb-2">What's Next?</h3>
              <p className="text-sm text-muted-foreground">
                You'll receive a calendar invite for your consultation session. 
                The mentor will contact you 15 minutes before the scheduled time.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PaymentSuccess;
