
import React from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Avatar from '../../components/ui/Avatar';
import { useAuth } from '../../hooks/useAuth';

const StudentProfile: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card glass className="p-8">
        <div className="flex items-center space-x-6">
          <Avatar
            src={user?.profile_picture}
            name={`${user?.first_name} ${user?.last_name}`}
            size="xl"
          />
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              {user?.first_name} {user?.last_name}
            </h1>
            <p className="text-blue-400 mb-4">Student</p>
            <Button variant="gradient">
              Edit Profile
            </Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card glass>
          <h3 className="text-xl font-bold text-white mb-4">Learning Goals</h3>
          <p className="text-white/70">
            Set your learning objectives and track your progress.
          </p>
        </Card>

        <Card glass>
          <h3 className="text-xl font-bold text-white mb-4">Completed Courses</h3>
          <p className="text-white/70">
            0 courses completed
          </p>
        </Card>
      </div>
    </div>
  );
};

export default StudentProfile;
