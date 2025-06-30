
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { ROUTES } from '../utils/constants';

const Index = () => {
  const { user, logout, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 w-full max-w-md border border-white/20 text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Welcome to OneGo!</h1>
          <p className="text-white/70 mb-6">Hello, {user.first_name} {user.last_name}!</p>
          <p className="text-white/70 mb-6">Role: {user.role}</p>
          <Button 
            onClick={logout} 
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
          >
            Logout
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 w-full max-w-md border border-white/20 text-center">
        <h1 className="text-2xl font-bold text-white mb-4">Welcome to OneGo</h1>
        <p className="text-white/70 mb-8">Your learning and mentorship platform</p>
        
        <div className="space-y-4">
          <Link to={ROUTES.LOGIN} className="block">
            <Button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white">
              Sign In
            </Button>
          </Link>
          
          <Link to={ROUTES.REGISTER} className="block">
            <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Create Account
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Index;
