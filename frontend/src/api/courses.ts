
import axiosInstance from './axios';

export interface Course {
  id: number;
  title: string;
  description: string;
  price: number;
  mentor: number;
  thumbnail: string;
  created_at: string;
}

export const courseAPI = {
  getCourses: async (): Promise<Course[]> => {
    const response = await axiosInstance.get('/courses/');
    return response.data;
  },

  getCourse: async (id: number): Promise<Course> => {
    const response = await axiosInstance.get(`/courses/${id}/`);
    return response.data;
  },

  createCourse: async (data: Partial<Course>): Promise<Course> => {
    const response = await axiosInstance.post('/courses/', data);
    return response.data;
  },
};
