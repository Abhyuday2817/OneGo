
// 📄 /services/socket.js
import { io } from 'socket.io-client';

export const socket = io('https://your-realtime-server.com'); // Replace with actual server URL

socket.on('connect', () => {
  console.log('🔌 Connected to socket server');
});
