// src/api/auth.ts

import axiosInstance from './axios';

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name?: string;
  last_name?: string;
  role: 'mentor' | 'student';
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_verified: boolean;
  profile_picture?: string;
  created_at: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

export const authAPI = {
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await axiosInstance.post('/auth/login/', data);
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await axiosInstance.post('/auth/register/', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      await axiosInstance.post('/auth/logout/', { refresh: refreshToken });
    }
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await axiosInstance.post('/auth/refresh/', { refresh });
    return response.data;
  },

  forgotPassword: async (email: string): Promise<void> => {
    await axiosInstance.post('/auth/password/reset/', { email });
  },

  resetPassword: async (token: string, password: string): Promise<void> => {
    await axiosInstance.post('/auth/password/reset/confirm/', {
      token,
      password,
    });
  },

  verifyEmail: async (token: string): Promise<void> => {
    await axiosInstance.post('/auth/verify-email/', { token });
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await axiosInstance.get('/auth/user/');
    return response.data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await axiosInstance.patch('/auth/user/', data);
    return response.data;
  },
};
