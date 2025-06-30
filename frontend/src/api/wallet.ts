
import axiosInstance from './axios';

export interface Transaction {
  id: number;
  user: number;
  amount: number;
  type: 'deposit' | 'withdrawal' | 'payment';
  description: string;
  created_at: string;
}

export const walletAPI = {
  getBalance: async (): Promise<{ balance: number }> => {
    const response = await axiosInstance.get('/wallet/balance/');
    return response.data;
  },

  getTransactions: async (): Promise<Transaction[]> => {
    const response = await axiosInstance.get('/wallet/transactions/');
    return response.data;
  },

  addFunds: async (amount: number): Promise<void> => {
    await axiosInstance.post('/wallet/add-funds/', { amount });
  },
};
