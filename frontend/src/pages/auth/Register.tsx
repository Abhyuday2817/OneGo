
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { ROUTES } from '../../utils/constants';
import { validateEmail, validatePassword, validateUsername, formatError } from '../../utils/helpers';

const Register: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    role: 'student' as 'student' | 'mentor',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.username) {
      newErrors.username = 'Username is required';
    } else if (!validateUsername(formData.username)) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }
    
    if (!formData.password1) {
      newErrors.password1 = 'Password is required';
    } else if (!validatePassword(formData.password1)) {
      newErrors.password1 = 'Password must be at least 8 characters';
    }
    
    if (!formData.password2) {
      newErrors.password2 = 'Please confirm your password';
    } else if (formData.password1 !== formData.password2) {
      newErrors.password2 = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    try {
      setLoading(true);
      setErrors({});
      
      await register(formData);
      navigate(ROUTES.HOME);
    } catch (error: any) {
      console.error('Registration error:', error);
      setErrors({ general: formatError(error) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 w-full max-w-md border border-white/20">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white mb-2">Create Account</h1>
          <p className="text-white/70">Join OneGo and start your learning journey</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {errors.general && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3">
              <p className="text-red-300 text-sm">{errors.general}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-white">First Name</label>
              <Input
                type="text"
                name="first_name"
                placeholder="John"
                value={formData.first_name}
                onChange={handleChange}
                className="bg-white/10 border-white/20 text-white placeholder-white/50"
              />
              {errors.first_name && <p className="text-red-300 text-sm">{errors.first_name}</p>}
            </div>
            <div className="space-y-1">
              <label className="block text-sm font-medium text-white">Last Name</label>
              <Input
                type="text"
                name="last_name"
                placeholder="Doe"
                value={formData.last_name}
                onChange={handleChange}
                className="bg-white/10 border-white/20 text-white placeholder-white/50"
              />
              {errors.last_name && <p className="text-red-300 text-sm">{errors.last_name}</p>}
            </div>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">Username</label>
            <Input
              type="text"
              name="username"
              placeholder="johndoe"
              value={formData.username}
              onChange={handleChange}
              className="bg-white/10 border-white/20 text-white placeholder-white/50"
            />
            {errors.username && <p className="text-red-300 text-sm">{errors.username}</p>}
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">Email</label>
            <Input
              type="email"
              name="email"
              placeholder="john@example.com"
              value={formData.email}
              onChange={handleChange}
              className="bg-white/10 border-white/20 text-white placeholder-white/50"
            />
            {errors.email && <p className="text-red-300 text-sm">{errors.email}</p>}
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">I want to join as</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="block w-full rounded-lg border border-white/20 bg-white/10 px-3 py-2 text-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="student">Student</option>
              <option value="mentor">Mentor</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">Password</label>
            <Input
              type="password"
              name="password1"
              placeholder="Enter password"
              value={formData.password1}
              onChange={handleChange}
              className="bg-white/10 border-white/20 text-white placeholder-white/50"
            />
            {errors.password1 && <p className="text-red-300 text-sm">{errors.password1}</p>}
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">Confirm Password</label>
            <Input
              type="password"
              name="password2"
              placeholder="Confirm password"
              value={formData.password2}
              onChange={handleChange}
              className="bg-white/10 border-white/20 text-white placeholder-white/50"
            />
            {errors.password2 && <p className="text-red-300 text-sm">{errors.password2}</p>}
          </div>

          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-white/70">
            Already have an account?{' '}
            <Link to={ROUTES.LOGIN} className="text-blue-400 hover:underline font-semibold">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
