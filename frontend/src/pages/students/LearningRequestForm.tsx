
import React, { useState } from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

const LearningRequestForm: React.FC = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    budget: '',
    timeline: '',
    skills: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Learning request submitted:', formData);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card glass className="p-8">
        <h1 className="text-2xl font-bold text-white mb-6">Create Learning Request</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Project Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="What do you want to learn?"
            className="bg-white/10 border-white/20 text-white placeholder-white/50"
          />

          <div className="space-y-1">
            <label className="block text-sm font-medium text-white">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe your learning goals and requirements..."
              rows={4}
              className="block w-full rounded-lg border border-white/20 bg-white/10 px-3 py-2 text-white placeholder-white/50 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <Input
            label="Budget"
            name="budget"
            value={formData.budget}
            onChange={handleChange}
            placeholder="Your budget range"
            className="bg-white/10 border-white/20 text-white placeholder-white/50"
          />

          <Input
            label="Timeline"
            name="timeline"
            value={formData.timeline}
            onChange={handleChange}
            placeholder="When do you want to complete this?"
            className="bg-white/10 border-white/20 text-white placeholder-white/50"
          />

          <Button type="submit" variant="gradient" size="lg" className="w-full">
            Post Learning Request
          </Button>
        </form>
      </Card>
    </div>
  );
};

export default LearningRequestForm;
