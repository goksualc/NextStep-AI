import React from 'react';
import { Card } from './Card';
import { Button } from './Button';

interface MatchCardProps {
  title: string;
  company: string;
  location: string;
  score: number;
  onWriteCoverLetter: () => void;
  description?: string;
  type?: string;
  postedDate?: string;
}

export const MatchCard: React.FC<MatchCardProps> = ({
  title,
  company,
  location,
  score,
  onWriteCoverLetter,
  description,
  type = 'Internship',
  postedDate
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-yellow-600 bg-yellow-100';
    if (score >= 70) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return 'Excellent Match';
    if (score >= 80) return 'Great Match';
    if (score >= 70) return 'Good Match';
    return 'Fair Match';
  };

  return (
    <Card className="hover:shadow-soft-lg transition-shadow duration-200">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-900 mb-1">
              {title}
            </h3>
            <p className="text-lg text-gray-600">{company}</p>
          </div>
          <div className="text-right">
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(score)}`}>
              {score}%
            </div>
            <p className="text-xs text-gray-500 mt-1">{getScoreLabel(score)}</p>
          </div>
        </div>

        {/* Details */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Location</p>
            <p className="font-medium text-gray-900">{location}</p>
          </div>
          <div>
            <p className="text-gray-500">Type</p>
            <p className="font-medium text-gray-900">{type}</p>
          </div>
          {postedDate && (
            <div>
              <p className="text-gray-500">Posted</p>
              <p className="font-medium text-gray-900">{postedDate}</p>
            </div>
          )}
        </div>

        {/* Description */}
        {description && (
          <p className="text-gray-700 text-sm leading-relaxed">
            {description}
          </p>
        )}

        {/* Actions */}
        <div className="flex space-x-3 pt-2">
          <Button 
            onClick={onWriteCoverLetter}
            className="flex-1"
          >
            Write Cover Letter
          </Button>
          <Button 
            variant="outline"
            className="flex-1"
          >
            View Details
          </Button>
        </div>
      </div>
    </Card>
  );
};
