
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Upload, Plus, X, Save, Eye } from 'lucide-react';

const CreateCourse = () => {
  const [courseData, setCourseData] = useState({
    title: '',
    description: '',
    category: '',
    level: '',
    price: '',
    duration: ''
  });

  const [modules, setModules] = useState([
    { title: '', description: '', lessons: [] }
  ]);

  const addModule = () => {
    setModules([...modules, { title: '', description: '', lessons: [] }]);
  };

  const removeModule = (index) => {
    setModules(modules.filter((_, i) => i !== index));
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold gradient-text mb-4">
            Create New Course
          </h1>
          <p className="text-muted-foreground text-lg">
            Share your knowledge and create an engaging learning experience
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Basic Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Course Title</label>
                  <Input
                    placeholder="Enter course title"
                    value={courseData.title}
                    onChange={(e) => setCourseData({...courseData, title: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Description</label>
                  <Textarea
                    placeholder="Describe what students will learn..."
                    rows={4}
                    value={courseData.description}
                    onChange={(e) => setCourseData({...courseData, description: e.target.value})}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Category</label>
                    <Select value={courseData.category} onValueChange={(value) => setCourseData({...courseData, category: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="development">Development</SelectItem>
                        <SelectItem value="design">Design</SelectItem>
                        <SelectItem value="business">Business</SelectItem>
                        <SelectItem value="marketing">Marketing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Level</label>
                    <Select value={courseData.level} onValueChange={(value) => setCourseData({...courseData, level: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="beginner">Beginner</SelectItem>
                        <SelectItem value="intermediate">Intermediate</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Price (USD)</label>
                    <Input
                      type="number"
                      placeholder="99"
                      value={courseData.price}
                      onChange={(e) => setCourseData({...courseData, price: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">Duration</label>
                    <Input
                      placeholder="e.g., 10 hours"
                      value={courseData.duration}
                      onChange={(e) => setCourseData({...courseData, duration: e.target.value})}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Course Thumbnail */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Course Thumbnail</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                  <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-4">
                    Upload a course thumbnail (recommended: 1920x1080)
                  </p>
                  <Button variant="outline">
                    Choose Image
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Course Modules */}
            <Card className="glass-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Course Modules</CardTitle>
                  <Button onClick={addModule} size="sm" className="btn-gradient">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Module
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {modules.map((module, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="font-semibold">Module {index + 1}</h3>
                      {modules.length > 1 && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeModule(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                    <div className="space-y-3">
                      <Input
                        placeholder="Module title"
                        value={module.title}
                        onChange={(e) => {
                          const newModules = [...modules];
                          newModules[index].title = e.target.value;
                          setModules(newModules);
                        }}
                      />
                      <Textarea
                        placeholder="Module description"
                        rows={2}
                        value={module.description}
                        onChange={(e) => {
                          const newModules = [...modules];
                          newModules[index].description = e.target.value;
                          setModules(newModules);
                        }}
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card className="glass-card border-gradient-instagram">
              <CardHeader>
                <CardTitle>Course Preview</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
                  <Upload className="w-8 h-8 text-muted-foreground" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">
                    {courseData.title || 'Course Title'}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {courseData.description || 'Course description will appear here...'}
                  </p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {courseData.category && (
                    <Badge className="bg-gradient-instagram text-white">
                      {courseData.category}
                    </Badge>
                  )}
                  {courseData.level && (
                    <Badge variant="outline">{courseData.level}</Badge>
                  )}
                </div>
                <div className="text-2xl font-bold gradient-text">
                  ${courseData.price || '0'}
                </div>
              </CardContent>
            </Card>

            <div className="space-y-3">
              <Button className="w-full btn-gradient">
                <Save className="w-4 h-4 mr-2" />
                Publish Course
              </Button>
              <Button variant="outline" className="w-full">
                <Eye className="w-4 h-4 mr-2" />
                Preview Course
              </Button>
              <Button variant="ghost" className="w-full">
                Save as Draft
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateCourse;
