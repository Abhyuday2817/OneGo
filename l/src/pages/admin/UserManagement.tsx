
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Search, Filter, MoreVertical, UserPlus, Ban, Shield } from 'lucide-react';

const UserManagement = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const users = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john.doe@email.com',
      role: 'user',
      status: 'active',
      joined: '2024-01-15',
      courses: 5,
      revenue: 0,
      avatar: '/placeholder.svg'
    },
    {
      id: 2,
      name: 'Sarah Johnson',
      email: 'sarah.j@email.com',
      role: 'mentor',
      status: 'active',
      joined: '2023-12-01',
      courses: 12,
      revenue: 4580,
      avatar: '/placeholder.svg'
    },
    {
      id: 3,
      name: 'Mike Chen',
      email: 'mike.chen@email.com',
      role: 'admin',
      status: 'active',
      joined: '2023-11-15',
      courses: 0,
      revenue: 0,
      avatar: '/placeholder.svg'
    }
  ];

  const UserCard = ({ user }) => (
    <Card className="glass-card mb-4">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Avatar className="w-16 h-16">
              <AvatarImage src={user.avatar} />
              <AvatarFallback className="bg-gradient-instagram text-white">
                {user.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-lg">{user.name}</h3>
              <p className="text-muted-foreground">{user.email}</p>
              <div className="flex items-center gap-2 mt-2">
                <Badge 
                  className={
                    user.role === 'admin' ? 'bg-red-500' :
                    user.role === 'mentor' ? 'bg-gradient-instagram text-white' :
                    'bg-gradient-onlyfans text-white'
                  }
                >
                  {user.role}
                </Badge>
                <Badge 
                  className={user.status === 'active' ? 'bg-green-500' : 'bg-gray-500'}
                >
                  {user.status}
                </Badge>
              </div>
            </div>
          </div>

          <div className="text-right">
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-sm text-muted-foreground">Joined</p>
                <p className="font-semibold">{user.joined}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Courses</p>
                <p className="font-semibold">{user.courses}</p>
              </div>
            </div>
            {user.revenue > 0 && (
              <div className="mb-4">
                <p className="text-sm text-muted-foreground">Revenue</p>
                <p className="font-semibold gradient-text">${user.revenue}</p>
              </div>
            )}
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Shield className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="sm">
                <Ban className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-display font-bold gradient-text mb-2">
              User Management
            </h1>
            <p className="text-muted-foreground">
              Manage users, roles, and permissions
            </p>
          </div>
          <Button className="btn-gradient">
            <UserPlus className="w-4 h-4 mr-2" />
            Add User
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">12,847</div>
            <p className="text-sm text-muted-foreground">Total Users</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">11,234</div>
            <p className="text-sm text-muted-foreground">Active Users</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">2,456</div>
            <p className="text-sm text-muted-foreground">Mentors</p>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold gradient-text mb-2">127</div>
            <p className="text-sm text-muted-foreground">New Today</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </Button>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full grid-cols-4 mb-8">
          <TabsTrigger value="all">All Users</TabsTrigger>
          <TabsTrigger value="users">Students</TabsTrigger>
          <TabsTrigger value="mentors">Mentors</TabsTrigger>
          <TabsTrigger value="admins">Admins</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <div>
            {users.map((user) => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="users">
          <div>
            {users.filter(u => u.role === 'user').map((user) => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="mentors">
          <div>
            {users.filter(u => u.role === 'mentor').map((user) => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="admins">
          <div>
            {users.filter(u => u.role === 'admin').map((user) => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default UserManagement;
