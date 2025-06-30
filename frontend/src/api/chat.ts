
import axiosInstance from './axios';

export interface Message {
  id: number;
  sender: number;
  receiver: number;
  content: string;
  timestamp: string;
}

export const chatAPI = {
  getMessages: async (userId: number): Promise<Message[]> => {
    const response = await axiosInstance.get(`/chat/messages/?user=${userId}`);
    return response.data;
  },

  sendMessage: async (data: Partial<Message>): Promise<Message> => {
    const response = await axiosInstance.post('/chat/messages/', data);
    return response.data;
  },
};
