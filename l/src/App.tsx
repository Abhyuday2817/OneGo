
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { SidebarProvider } from "@/components/ui/sidebar";

// Layout Components
import MainLayout from "@/layouts/MainLayout";
import AuthLayout from "@/layouts/AuthLayout";

// Pages
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

// Auth Pages
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import ForgotPassword from "./pages/auth/ForgotPassword";

// Dashboard Pages
import Dashboard from "./pages/dashboard/Dashboard";
import Profile from "./pages/dashboard/Profile";
import Settings from "./pages/dashboard/Settings";

// Mentor Pages
import MentorDashboard from "./pages/mentors/MentorDashboard";
import MentorProfile from "./pages/mentors/MentorProfile";
import FindMentors from "./pages/mentors/FindMentors";
import BecomeMentor from "./pages/mentors/BecomeMentor";

// Course Pages
import Courses from "./pages/courses/Courses";
import CourseDetail from "./pages/courses/CourseDetail";
import CreateCourse from "./pages/courses/CreateCourse";
import MyCourses from "./pages/courses/MyCourses";

// Consultation Pages
import Consultations from "./pages/consultations/Consultations";
import BookConsultation from "./pages/consultations/BookConsultation";
import MyConsultations from "./pages/consultations/MyConsultations";

// Gig Pages
import Gigs from "./pages/gigs/Gigs";
import GigDetail from "./pages/gigs/GigDetail";
import CreateGig from "./pages/gigs/CreateGig";
import MyGigs from "./pages/gigs/MyGigs";

// Session Pages
import Sessions from "./pages/sessions/Sessions";
import SessionRoom from "./pages/sessions/SessionRoom";

// Chat Pages
import Chat from "./pages/chat/Chat";
import Messages from "./pages/chat/Messages";

// Payment Pages
import Payments from "./pages/payments/Payments";
import Wallet from "./pages/payments/Wallet";
import PaymentSuccess from "./pages/payments/PaymentSuccess";

// Review Pages
import Reviews from "./pages/reviews/Reviews";
import WriteReview from "./pages/reviews/WriteReview";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import UserManagement from "./pages/admin/UserManagement";
import ContentModeration from "./pages/admin/ContentModeration";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <AuthProvider>
        <SidebarProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Index />} />
              
              {/* Auth Routes */}
              <Route path="/auth" element={<AuthLayout />}>
                <Route path="login" element={<Login />} />
                <Route path="register" element={<Register />} />
                <Route path="forgot-password" element={<ForgotPassword />} />
              </Route>

              {/* Protected Routes */}
              <Route path="/" element={<MainLayout />}>
                {/* Dashboard */}
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="profile" element={<Profile />} />
                <Route path="settings" element={<Settings />} />

                {/* Mentors */}
                <Route path="mentors" element={<FindMentors />} />
                <Route path="mentors/:id" element={<MentorProfile />} />
                <Route path="mentor/dashboard" element={<MentorDashboard />} />
                <Route path="become-mentor" element={<BecomeMentor />} />

                {/* Courses */}
                <Route path="courses" element={<Courses />} />
                <Route path="courses/:id" element={<CourseDetail />} />
                <Route path="courses/create" element={<CreateCourse />} />
                <Route path="my-courses" element={<MyCourses />} />

                {/* Consultations */}
                <Route path="consultations" element={<Consultations />} />
                <Route path="consultations/book/:mentorId" element={<BookConsultation />} />
                <Route path="my-consultations" element={<MyConsultations />} />

                {/* Gigs */}
                <Route path="gigs" element={<Gigs />} />
                <Route path="gigs/:id" element={<GigDetail />} />
                <Route path="gigs/create" element={<CreateGig />} />
                <Route path="my-gigs" element={<MyGigs />} />

                {/* Sessions */}
                <Route path="sessions" element={<Sessions />} />
                <Route path="sessions/:id" element={<SessionRoom />} />

                {/* Chat */}
                <Route path="chat" element={<Chat />} />
                <Route path="messages" element={<Messages />} />

                {/* Payments */}
                <Route path="payments" element={<Payments />} />
                <Route path="wallet" element={<Wallet />} />
                <Route path="payment/success" element={<PaymentSuccess />} />

                {/* Reviews */}
                <Route path="reviews" element={<Reviews />} />
                <Route path="reviews/write/:type/:id" element={<WriteReview />} />

                {/* Admin */}
                <Route path="admin" element={<AdminDashboard />} />
                <Route path="admin/users" element={<UserManagement />} />
                <Route path="admin/moderation" element={<ContentModeration />} />
              </Route>

              {/* Catch-all route */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </SidebarProvider>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
