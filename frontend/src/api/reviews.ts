
import axiosInstance from './axios';

export interface Review {
  id: number;
  reviewer: number;
  mentor: number;
  course?: number;
  rating: number;
  comment: string;
  created_at: string;
}

export const reviewAPI = {
  getReviews: async (mentorId?: number, courseId?: number): Promise<Review[]> => {
    const params = new URLSearchParams();
    if (mentorId) params.append('mentor', mentorId.toString());
    if (courseId) params.append('course', courseId.toString());
    
    const response = await axiosInstance.get(`/reviews/?${params}`);
    return response.data;
  },

  createReview: async (data: Partial<Review>): Promise<Review> => {
    const response = await axiosInstance.post('/reviews/', data);
    return response.data;
  },
};
