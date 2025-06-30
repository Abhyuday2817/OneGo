
import axiosInstance from './axios';

export interface Mentor {
  id: number;
  user: {
    first_name: string;
    last_name: string;
    email: string;
  };
  bio: string;
  hourly_rate: number;
  average_rating: number;
  total_reviews: number;
  skills: string[];
  languages: string[];
  availability: any;
}

export const mentorAPI = {
  getMentors: async (): Promise<Mentor[]> => {
    const response = await axiosInstance.get('/mentors/');
    return response.data;
  },

  getMentor: async (id: number): Promise<Mentor> => {
    const response = await axiosInstance.get(`/mentors/${id}/`);
    return response.data;
  },

  updateMentorProfile: async (id: number, data: Partial<Mentor>): Promise<Mentor> => {
    const response = await axiosInstance.patch(`/mentors/${id}/`, data);
    return response.data;
  },
};
