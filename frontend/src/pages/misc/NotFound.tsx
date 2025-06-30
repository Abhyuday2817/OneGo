
import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../../components/ui/Button';
import { ROUTES } from '../../utils/constants';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-white/20 mb-4">404</h1>
          <h2 className="text-3xl font-bold text-white mb-4">Page Not Found</h2>
          <p className="text-white/70 text-lg mb-8">
            The page you're looking for doesn't exist or has been moved.
          </p>
        </div>
        
        <div className="space-x-4">
          <Link to={ROUTES.HOME}>
            <Button variant="gradient" size="lg">
              Go Home
            </Button>
          </Link>
          <button 
            onClick={() => window.history.back()}
            className="px-6 py-3 text-white/70 hover:text-white transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
