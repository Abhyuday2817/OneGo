
import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { ROUTES } from '../../utils/constants';

const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link to={ROUTES.HOME} className="inline-flex items-center space-x-2">
            <div className="w-12 h-12 instagram-gradient rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-2xl">O</span>
            </div>
            <span className="text-white font-bold text-3xl">OneGo</span>
          </Link>
        </div>

        {/* Auth Form */}
        <div className="glass-effect rounded-2xl p-8 shadow-2xl">
          <Outlet />
        </div>

        {/* Footer */}
        <div className="text-center mt-6">
          <p className="text-white/60 text-sm">
            By continuing, you agree to our{' '}
            <Link to="/terms" className="text-blue-400 hover:underline">
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link to="/privacy" className="text-blue-400 hover:underline">
              Privacy Policy
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
