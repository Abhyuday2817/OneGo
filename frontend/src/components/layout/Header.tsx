
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import Avatar from '../ui/Avatar';
import Button from '../ui/Button';
import { ROUTES } from '../../utils/constants';

const Header: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="glass-effect border-b border-white/20 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to={ROUTES.HOME} className="flex items-center space-x-2">
            <div className="w-8 h-8 instagram-gradient rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">O</span>
            </div>
            <span className="text-white font-bold text-xl">OneGo</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to={ROUTES.MENTORS} className="text-white/80 hover:text-white transition-colors">
              Find Mentors
            </Link>
            <Link to={ROUTES.COURSES} className="text-white/80 hover:text-white transition-colors">
              Courses
            </Link>
            <Link to={ROUTES.CHAT} className="text-white/80 hover:text-white transition-colors">
              Messages
            </Link>
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link to={ROUTES.WALLET}>
                  <Button variant="outline" size="sm" className="text-white border-white/30">
                    Wallet
                  </Button>
                </Link>
                <div className="relative group">
                  <Avatar
                    src={user?.profile_picture}
                    name={`${user?.first_name} ${user?.last_name}`}
                    online={true}
                  />
                  <div className="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                    <div className="p-2">
                      <Link
                        to={user?.role === 'mentor' ? ROUTES.MENTOR_DASHBOARD : ROUTES.STUDENT_DASHBOARD}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
                      >
                        Dashboard
                      </Link>
                      <Link
                        to={ROUTES.SETTINGS}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
                      >
                        Settings
                      </Link>
                      <button
                        onClick={logout}
                        className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 rounded"
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to={ROUTES.LOGIN}>
                  <Button variant="ghost" size="sm" className="text-white">
                    Login
                  </Button>
                </Link>
                <Link to={ROUTES.REGISTER}>
                  <Button variant="gradient" size="sm">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
