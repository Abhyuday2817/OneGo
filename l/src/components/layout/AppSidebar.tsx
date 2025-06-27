
import {
  Home,
  User,
  BookOpen,
  Calendar,
  MessageCircle,
  Briefcase,
  CreditCard,
  Star,
  Settings,
  Users,
  GraduationCap,
  Video,
  Shield,
  Award,
} from 'lucide-react';
import { NavLink } from 'react-router-dom';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
} from '@/components/ui/sidebar';
import { useAuth } from '@/contexts/AuthContext';

const menuItems = [
  {
    title: 'Dashboard',
    items: [
      { title: 'Overview', url: '/dashboard', icon: Home },
      { title: 'Profile', url: '/profile', icon: User },
    ],
  },
  {
    title: 'Learning',
    items: [
      { title: 'Courses', url: '/courses', icon: BookOpen },
      { title: 'My Courses', url: '/my-courses', icon: GraduationCap },
      { title: 'Sessions', url: '/sessions', icon: Video },
    ],
  },
  {
    title: 'Mentorship',
    items: [
      { title: 'Find Mentors', url: '/mentors', icon: Users },
      { title: 'Consultations', url: '/consultations', icon: Calendar },
      { title: 'My Consultations', url: '/my-consultations', icon: Calendar },
    ],
  },
  {
    title: 'Services',
    items: [
      { title: 'Gigs', url: '/gigs', icon: Briefcase },
      { title: 'My Gigs', url: '/my-gigs', icon: Briefcase },
    ],
  },
  {
    title: 'Communication',
    items: [
      { title: 'Messages', url: '/messages', icon: MessageCircle },
      { title: 'Chat', url: '/chat', icon: MessageCircle },
    ],
  },
  {
    title: 'Financial',
    items: [
      { title: 'Payments', url: '/payments', icon: CreditCard },
      { title: 'Wallet', url: '/wallet', icon: CreditCard },
    ],
  },
  {
    title: 'Reviews & Ratings',
    items: [
      { title: 'Reviews', url: '/reviews', icon: Star },
    ],
  },
];

const mentorItems = [
  { title: 'Mentor Dashboard', url: '/mentor/dashboard', icon: Shield },
  { title: 'Become Mentor', url: '/become-mentor', icon: Award },
];

const adminItems = [
  { title: 'Admin Dashboard', url: '/admin', icon: Shield },
  { title: 'User Management', url: '/admin/users', icon: Users },
  { title: 'Content Moderation', url: '/admin/moderation', icon: Shield },
];

export function AppSidebar() {
  const { user } = useAuth();

  return (
    <Sidebar className="border-r border-border/50 bg-card/50 backdrop-blur-sm">
      <SidebarHeader className="border-b border-border/50 p-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-instagram rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">O</span>
          </div>
          <span className="font-display font-bold text-xl gradient-text">OneGo</span>
        </div>
      </SidebarHeader>
      
      <SidebarContent className="px-2">
        {menuItems.map((section) => (
          <SidebarGroup key={section.title}>
            <SidebarGroupLabel className="text-muted-foreground font-medium">
              {section.title}
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {section.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild>
                      <NavLink
                        to={item.url}
                        className={({ isActive }) =>
                          `flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                            isActive
                              ? 'bg-gradient-instagram text-white shadow-lg'
                              : 'hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                          }`
                        }
                      >
                        <item.icon className="h-4 w-4" />
                        <span className="font-medium">{item.title}</span>
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}

        {/* Mentor Section */}
        {(user?.role === 'mentor' || user?.role === 'admin') && (
          <SidebarGroup>
            <SidebarGroupLabel className="text-muted-foreground font-medium">
              Mentor Tools
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {mentorItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild>
                      <NavLink
                        to={item.url}
                        className={({ isActive }) =>
                          `flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                            isActive
                              ? 'bg-gradient-onlyfans text-white shadow-lg'
                              : 'hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                          }`
                        }
                      >
                        <item.icon className="h-4 w-4" />
                        <span className="font-medium">{item.title}</span>
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        )}

        {/* Admin Section */}
        {user?.role === 'admin' && (
          <SidebarGroup>
            <SidebarGroupLabel className="text-muted-foreground font-medium">
              Administration
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {adminItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild>
                      <NavLink
                        to={item.url}
                        className={({ isActive }) =>
                          `flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                            isActive
                              ? 'bg-destructive text-destructive-foreground shadow-lg'
                              : 'hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                          }`
                        }
                      >
                        <item.icon className="h-4 w-4" />
                        <span className="font-medium">{item.title}</span>
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        )}

        {/* Settings */}
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <NavLink
                    to="/settings"
                    className={({ isActive }) =>
                      `flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                        isActive
                          ? 'bg-gradient-instagram text-white shadow-lg'
                          : 'hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                      }`
                    }
                  >
                    <Settings className="h-4 w-4" />
                    <span className="font-medium">Settings</span>
                  </NavLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
