
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { ROUTES } from '../../utils/constants';
import { cn } from '@/lib/utils';

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();

  const mentorLinks = [
    { name: 'Dashboard', path: ROUTES.MENTOR_DASHBOARD, icon: '📊' },
    { name: 'My Courses', path: '/mentors/courses', icon: '📚' },
    { name: 'Upload Course', path: ROUTES.UPLOAD_COURSE, icon: '⬆️' },
    { name: 'Availability', path: ROUTES.AVAILABILITY, icon: '📅' },
    { name: 'Sessions', path: '/mentors/sessions', icon: '🎥' },
    { name: 'Reviews', path: ROUTES.REVIEWS, icon: '⭐' },
    { name: 'Earnings', path: '/mentors/earnings', icon: '💰' },
  ];

  const studentLinks = [
    { name: 'Dashboard', path: ROUTES.STUDENT_DASHBOARD, icon: '📊' },
    { name: 'My Courses', path: '/students/courses', icon: '📚' },
    { name: 'Find Mentors', path: ROUTES.MENTORS, icon: '👨‍🏫' },
    { name: 'Learning Request', path: ROUTES.LEARNING_REQUEST, icon: '📝' },
    { name: 'Sessions', path: '/students/sessions', icon: '🎥' },
    { name: 'Progress', path: '/students/progress', icon: '📈' },
  ];

  const commonLinks = [
    { name: 'Messages', path: ROUTES.CHAT, icon: '💬' },
    { name: 'Wallet', path: ROUTES.WALLET, icon: '💳' },
    { name: 'Settings', path: ROUTES.SETTINGS, icon: '⚙️' },
  ];

  const links = user?.role === 'mentor' ? mentorLinks : studentLinks;

  return (
    <aside className="glass-effect w-64 min-h-screen border-r border-white/20">
      <div className="p-6">
        <div className="space-y-8">
          {/* Main Navigation */}
          <div>
            <h3 className="text-white/60 text-xs font-semibold uppercase tracking-wider mb-4">
              Main
            </h3>
            <nav className="space-y-1">
              {links.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={cn(
                    'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                    location.pathname === link.path
                      ? 'bg-white/20 text-white'
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  )}
                >
                  <span className="mr-3">{link.icon}</span>
                  {link.name}
                </Link>
              ))}
            </nav>
          </div>

          {/* Common Links */}
          <div>
            <h3 className="text-white/60 text-xs font-semibold uppercase tracking-wider mb-4">
              General
            </h3>
            <nav className="space-y-1">
              {commonLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={cn(
                    'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                    location.pathname === link.path
                      ? 'bg-white/20 text-white'
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  )}
                >
                  <span className="mr-3">{link.icon}</span>
                  {link.name}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
