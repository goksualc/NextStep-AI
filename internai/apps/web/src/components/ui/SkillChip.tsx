'use client';

import React from 'react';

interface SkillChipProps {
  skill: string;
  type?: 'skill' | 'missing' | 'highlight';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  className?: string;
}

export const SkillChip: React.FC<SkillChipProps> = ({
  skill,
  type = 'skill',
  size = 'md',
  onClick,
  className = ''
}) => {
  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
    lg: 'px-4 py-2 text-base'
  };

  const typeClasses = {
    skill: 'bg-primary-100 text-primary-800 border-primary-200',
    missing: 'bg-orange-100 text-orange-800 border-orange-200',
    highlight: 'bg-blue-100 text-blue-800 border-blue-200'
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'skill':
        return '✓';
      case 'missing':
        return '📈';
      case 'highlight':
        return '⭐';
      default:
        return '';
    }
  };

  const baseClasses = `
    inline-flex items-center rounded-full font-medium border transition-all duration-200
    ${sizeClasses[size]}
    ${typeClasses[type]}
    ${onClick ? 'cursor-pointer hover:scale-105 hover:shadow-md' : ''}
    ${className}
  `;

  return (
    <span className={baseClasses} onClick={onClick}>
      {getIcon(type)}
      <span className="ml-1">{skill}</span>
    </span>
  );
};
