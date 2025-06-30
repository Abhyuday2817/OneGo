
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const ROUTES = {
  // Auth
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/reset-password',
  
  // Dashboard
  MENTOR_DASHBOARD: '/dashboard/mentor',
  STUDENT_DASHBOARD: '/dashboard/student',
  
  // Mentors
  MENTORS: '/mentors',
  MENTOR_PROFILE: '/mentors/:id',
  UPLOAD_COURSE: '/mentors/upload-course',
  AVAILABILITY: '/mentors/availability',
  
  // Students
  STUDENT_PROFILE: '/students/profile',
  LEARNING_REQUEST: '/students/learning-request',
  
  // Courses
  COURSES: '/courses',
  COURSE_DETAIL: '/courses/:id',
  PROGRESS: '/courses/:id/progress',
  CERTIFICATE: '/courses/:id/certificate',
  
  // Appointments
  BOOKING: '/appointments/booking',
  TIME_SLOTS: '/appointments/slots',
  SESSION_SUMMARY: '/appointments/summary/:id',
  
  // Chat
  CHAT: '/chat',
  CHAT_ROOM: '/chat/:roomId',
  
  // Wallet
  WALLET: '/wallet',
  ADD_FUNDS: '/wallet/add-funds',
  TRANSACTIONS: '/wallet/transactions',
  WITHDRAW: '/wallet/withdraw',
  
  // Reviews
  REVIEWS: '/reviews',
  LEAVE_REVIEW: '/reviews/new/:id',
  
  // Settings
  SETTINGS: '/settings',
  
  // Misc
  HOME: '/',
  NOT_FOUND: '/404'
};

export const USER_ROLES = {
  STUDENT: 'student',
  MENTOR: 'mentor',
  ADMIN: 'admin'
};

export const PAYMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  REFUNDED: 'refunded'
};

export const SESSION_STATUS = {
  SCHEDULED: 'scheduled',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};

export const COURSE_CATEGORIES = [
  'Programming',
  'Design',
  'Business',
  'Marketing',
  'Music',
  'Language',
  'Health',
  'Photography',
  'Writing',
  'Other'
];
