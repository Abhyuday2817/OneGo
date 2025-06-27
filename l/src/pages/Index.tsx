
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  BookOpen, 
  Users, 
  Calendar, 
  Star, 
  ArrowRight, 
  PlayCircle,
  Award,
  TrendingUp,
  MessageCircle,
  Shield
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Index = () => {
  const features = [
    {
      icon: Users,
      title: 'Expert Mentors',
      description: 'Connect with industry professionals and get personalized guidance',
      color: 'from-instagram-500 to-instagram-600'
    },
    {
      icon: BookOpen,
      title: 'Premium Courses',
      description: 'Access curated courses designed by top professionals',
      color: 'from-onlyfans-500 to-onlyfans-600'
    },
    {
      icon: Calendar,
      title: 'Flexible Scheduling',
      description: 'Book consultations that fit your schedule',
      color: 'from-emerald-500 to-emerald-600'
    },
    {
      icon: MessageCircle,
      title: 'Real-time Chat',
      description: 'Stay connected with mentors and peers',
      color: 'from-violet-500 to-violet-600'
    }
  ];

  const stats = [
    { label: 'Active Mentors', value: '2,500+', icon: Users },
    { label: 'Courses Available', value: '1,200+', icon: BookOpen },
    { label: 'Students Enrolled', value: '50,000+', icon: TrendingUp },
    { label: 'Success Rate', value: '95%', icon: Award }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-instagram rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-lg">O</span>
            </div>
            <span className="font-display font-bold text-2xl gradient-text">OneGo</span>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#features" className="nav-link text-muted-foreground hover:text-foreground">Features</a>
            <a href="#courses" className="nav-link text-muted-foreground hover:text-foreground">Courses</a>
            <a href="#mentors" className="nav-link text-muted-foreground hover:text-foreground">Mentors</a>
            <a href="#pricing" className="nav-link text-muted-foreground hover:text-foreground">Pricing</a>
          </nav>

          <div className="flex items-center space-x-4">
            <Link to="/auth/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link to="/auth/register">
              <Button className="btn-gradient text-white">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-hero overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center text-white max-w-4xl mx-auto">
            <Badge className="mb-6 bg-white/20 text-white border-white/30" variant="outline">
              <Star className="w-4 h-4 mr-1" />
              Trusted by 50,000+ professionals
            </Badge>
            
            <h1 className="text-5xl md:text-7xl font-display font-bold mb-6 leading-tight">
              Accelerate Your
              <span className="block bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
                Professional Growth
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-8 text-white/90 max-w-3xl mx-auto leading-relaxed">
              Connect with expert mentors, take premium courses, and unlock your potential with our comprehensive learning platform.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/auth/register">
                <Button size="lg" className="bg-white text-gray-900 hover:bg-white/90 px-8 py-4 text-lg font-semibold">
                  Start Learning Today
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 px-8 py-4">
                <PlayCircle className="mr-2 h-5 w-5" />
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-gradient-instagram rounded-full flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="h-8 w-8 text-white" />
                </div>
                <div className="text-3xl font-bold text-foreground mb-2">{stat.value}</div>
                <div className="text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <Badge className="mb-4" variant="outline">Features</Badge>
            <h2 className="text-4xl md:text-5xl font-display font-bold mb-6">
              Everything you need to
              <span className="gradient-text"> succeed</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Our platform provides all the tools and resources you need to advance your career and achieve your goals.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-300 border-0 bg-gradient-to-br from-background to-muted/30">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-instagram">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-3xl mx-auto text-white">
            <h2 className="text-4xl md:text-5xl font-display font-bold mb-6">
              Ready to transform your career?
            </h2>
            <p className="text-xl mb-8 text-white/90">
              Join thousands of professionals who have accelerated their growth with OneGo.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/auth/register">
                <Button size="lg" className="bg-white text-gray-900 hover:bg-white/90 px-8 py-4">
                  Get Started Free
                </Button>
              </Link>
              <Link to="/courses">
                <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10 px-8 py-4">
                  Browse Courses
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-background border-t">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-instagram rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">O</span>
                </div>
                <span className="font-display font-bold text-xl gradient-text">OneGo</span>
              </div>
              <p className="text-muted-foreground">
                Empowering professionals to achieve their career goals through expert mentorship and premium education.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="/courses" className="hover:text-foreground">Courses</a></li>
                <li><a href="/mentors" className="hover:text-foreground">Mentors</a></li>
                <li><a href="/gigs" className="hover:text-foreground">Gigs</a></li>
                <li><a href="/consultations" className="hover:text-foreground">Consultations</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="/about" className="hover:text-foreground">About</a></li>
                <li><a href="/careers" className="hover:text-foreground">Careers</a></li>
                <li><a href="/contact" className="hover:text-foreground">Contact</a></li>
                <li><a href="/blog" className="hover:text-foreground">Blog</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-muted-foreground">
                <li><a href="/help" className="hover:text-foreground">Help Center</a></li>
                <li><a href="/privacy" className="hover:text-foreground">Privacy</a></li>
                <li><a href="/terms" className="hover:text-foreground">Terms</a></li>
                <li><a href="/status" className="hover:text-foreground">Status</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t mt-8 pt-8 text-center text-muted-foreground">
            <p>&copy; 2024 OneGo. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
