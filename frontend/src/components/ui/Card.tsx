
import React from 'react';
import { cn } from '@/lib/utils';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glass?: boolean;
}

const Card: React.FC<CardProps> = ({
  children,
  className,
  hover = false,
  glass = false,
}) => {
  return (
    <div
      className={cn(
        'rounded-xl p-6 shadow-lg transition-all duration-300',
        glass ? 'glass-effect' : 'bg-white',
        hover && 'hover:shadow-xl hover:scale-105',
        className
      )}
    >
      {children}
    </div>
  );
};

export default Card;
