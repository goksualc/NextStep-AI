'use client';

import React from 'react';

interface ProgressBarProps {
  value: number; // 0-100
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  size = 'md',
  showLabel = true,
  label,
  className = ''
}) => {
  // Clamp value between 0 and 100
  const clampedValue = Math.min(100, Math.max(0, value));

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  };

  const getColorClasses = (value: number) => {
    if (value >= 90) return 'bg-gradient-to-r from-green-500 to-green-600';
    if (value >= 80) return 'bg-gradient-to-r from-blue-500 to-blue-600';
    if (value >= 70) return 'bg-gradient-to-r from-yellow-500 to-yellow-600';
    if (value >= 60) return 'bg-gradient-to-r from-orange-500 to-orange-600';
    return 'bg-gradient-to-r from-red-500 to-red-600';
  };

  const getScoreLabel = (value: number) => {
    if (value >= 90) return 'Excellent Match';
    if (value >= 80) return 'Great Match';
    if (value >= 70) return 'Good Match';
    if (value >= 60) return 'Fair Match';
    return 'Poor Match';
  };

  return (
    <div className={`w-full ${className}`}>
      {/* Label and Score */}
      {showLabel && (
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">
            {label || 'Match Score'}
          </span>
          <div className="flex items-center space-x-2">
            <span className="text-sm font-bold text-gray-900">
              {clampedValue.toFixed(1)}%
            </span>
            <span className={`text-xs px-2 py-1 rounded-full font-medium ${
              clampedValue >= 90 ? 'bg-green-100 text-green-800' :
              clampedValue >= 80 ? 'bg-blue-100 text-blue-800' :
              clampedValue >= 70 ? 'bg-yellow-100 text-yellow-800' :
              clampedValue >= 60 ? 'bg-orange-100 text-orange-800' :
              'bg-red-100 text-red-800'
            }`}>
              {getScoreLabel(clampedValue)}
            </span>
          </div>
        </div>
      )}

      {/* Progress Bar */}
      <div className={`w-full bg-gray-200 rounded-full overflow-hidden ${sizeClasses[size]}`}>
        <div
          className={`h-full transition-all duration-500 ease-out rounded-full ${getColorClasses(clampedValue)}`}
          style={{ width: `${clampedValue}%` }}
        />
      </div>
    </div>
  );
};
