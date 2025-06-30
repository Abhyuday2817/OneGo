
import axiosInstance from './axios';

export interface Student {
  id: number;
  user: {
    first_name: string;
    last_name: string;
    email: string;
  };
  learning_goals: string;
  interests: string[];
}

export const studentAPI = {
  getStudentProfile: async (id: number): Promise<Student> => {
    const response = await axiosInstance.get(`/students/${id}/`);
    return response.data;
  },

  updateStudentProfile: async (id: number, data: Partial<Student>): Promise<Student> => {
    const response = await axiosInstance.patch(`/students/${id}/`, data);
    return response.data;
  },
};
