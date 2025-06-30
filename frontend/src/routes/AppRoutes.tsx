import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

// Layouts
import MainLayout from '../components/layout/MainLayout';
import AuthLayout from '../components/layout/AuthLayout';

// Pages
import Index from '../pages/misc/Index';
import NotFound from '../pages/misc/NotFound';

// Auth Pages
import Login from '../pages/auth/Login';
import Register from '../pages/auth/Register';
import ForgotPassword from '../pages/auth/ForgotPassword';
import ResetPassword from '../pages/auth/ResetPassword';

// Dashboard Pages
import MentorDashboard from '../pages/dashboard/MentorDashboard';
import StudentDashboard from '../pages/dashboard/StudentDashboard';

// Mentor Pages
import MentorList from '../pages/mentors/MentorList';
import MentorProfile from '../pages/mentors/MentorProfile';

// Student Pages
import StudentProfile from '../pages/students/StudentProfile';
import LearningRequestForm from '../pages/students/LearningRequestForm';

// Course Pages
import CourseList from '../pages/courses/CourseList';
import CourseDetail from '../pages/courses/CourseDetail';

// Other Pages
import BookingPage from '../pages/appointments/BookingPage';
import TimeSlots from '../pages/appointments/TimeSlots';
import ChatRoom from '../pages/chat/ChatRoom';
import WalletPage from '../pages/wallet/WalletPage';
import AddFunds from '../pages/wallet/AddFunds';
import Transactions from '../pages/wallet/Transactions';
import LeaveReview from '../pages/reviews/LeaveReview';
import ReviewList from '../pages/reviews/ReviewList';
import AccountSettings from '../pages/settings/AccountSettings';

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode; allowedRoles?: string[] }> = ({ 
  children, 
  allowedRoles 
}) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  
  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white"></div>
    </div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Index />} />
        <Route path="mentors" element={<MentorList />} />
        <Route path="mentors/:id" element={<MentorProfile />} />
        <Route path="courses" element={<CourseList />} />
        <Route path="courses/:id" element={<CourseDetail />} />
      </Route>

      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="forgot-password" element={<ForgotPassword />} />
        <Route path="reset-password" element={<ResetPassword />} />
      </Route>

      {/* Protected Routes */}
      <Route path="/" element={<MainLayout />}>
        {/* Dashboard Routes */}
        <Route 
          path="dashboard/mentor" 
          element={
            <ProtectedRoute allowedRoles={['mentor']}>
              <MentorDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="dashboard/student" 
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <StudentDashboard />
            </ProtectedRoute>
          } 
        />

        {/* Student Routes */}
        <Route 
          path="students/profile" 
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <StudentProfile />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="students/learning-request" 
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <LearningRequestForm />
            </ProtectedRoute>
          } 
        />

        {/* Appointment Routes */}
        <Route 
          path="appointments/booking" 
          element={
            <ProtectedRoute>
              <BookingPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="appointments/slots" 
          element={
            <ProtectedRoute>
              <TimeSlots />
            </ProtectedRoute>
          } 
        />

        {/* Chat Routes */}
        <Route 
          path="chat" 
          element={
            <ProtectedRoute>
              <ChatRoom />
            </ProtectedRoute>
          } 
        />

        {/* Wallet Routes */}
        <Route 
          path="wallet" 
          element={
            <ProtectedRoute>
              <WalletPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="wallet/add-funds" 
          element={
            <ProtectedRoute>
              <AddFunds />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="wallet/transactions" 
          element={
            <ProtectedRoute>
              <Transactions />
            </ProtectedRoute>
          } 
        />

        {/* Review Routes */}
        <Route 
          path="reviews" 
          element={
            <ProtectedRoute>
              <ReviewList />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="reviews/new/:id" 
          element={
            <ProtectedRoute>
              <LeaveReview />
            </ProtectedRoute>
          } 
        />

        {/* Settings */}
        <Route 
          path="settings" 
          element={
            <ProtectedRoute>
              <AccountSettings />
            </ProtectedRoute>
          } 
        />
      </Route>

      {/* 404 Route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRoutes;
