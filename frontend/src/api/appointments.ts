
import axiosInstance from './axios';

export interface Appointment {
  id: number;
  mentor: number;
  student: number;
  start_time: string;
  end_time: string;
  status: string;
}

export const appointmentAPI = {
  getAppointments: async (): Promise<Appointment[]> => {
    const response = await axiosInstance.get('/appointments/');
    return response.data;
  },

  createAppointment: async (data: Partial<Appointment>): Promise<Appointment> => {
    const response = await axiosInstance.post('/appointments/', data);
    return response.data;
  },
};
