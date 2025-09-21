import React, { useState } from 'react';
import { Card } from './Card';
import { Button } from './Button';
import { Modal } from './Modal';
import { writeCoverLetter, APIError } from '@/lib/api';
import { useUserStore } from '@/lib/store';
import { JobItem } from '@/lib/types';

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
  const { profile } = useUserStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [coverLetter, setCoverLetter] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  const handleWriteCoverLetter = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const jobItem: JobItem = {
        id: Math.random().toString(36).substr(2, 9), // Generate a random ID
        source: 'linkedin',
        title,
        company,
        location,
        url: `https://example.com/job/${title.toLowerCase().replace(/\s+/g, '-')}`,
        desc: description
      };

      const result = await writeCoverLetter({
        job: jobItem,
        profile: profile
      });

      setCoverLetter(result.cover_letter);
      setIsModalOpen(true);
      onWriteCoverLetter(); // Call the parent callback
    } catch (err) {
      if (err instanceof APIError) {
        setError(`Failed to generate cover letter: ${err.message}`);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopyCoverLetter = async () => {
    try {
      await navigator.clipboard.writeText(coverLetter);
      // You could add a toast notification here
      console.log('Cover letter copied to clipboard');
    } catch (err) {
      console.error('Failed to copy cover letter:', err);
    }
  };

  return (
    <>
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
              onClick={handleWriteCoverLetter}
              className="flex-1"
              disabled={isGenerating}
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                  Generating...
                </>
              ) : (
                'Write Cover Letter'
              )}
            </Button>
            <Button 
              variant="outline"
              className="flex-1"
            >
              View Details
            </Button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}
        </div>
      </Card>

      {/* Cover Letter Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Generated Cover Letter"
        size="xl"
      >
        <div className="space-y-4">
          <div className="bg-gray-50 rounded-xl p-4 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm text-gray-900 font-sans">
              {coverLetter}
            </pre>
          </div>
          
          <div className="flex space-x-3">
            <Button onClick={handleCopyCoverLetter} className="flex-1">
              📋 Copy to Clipboard
            </Button>
            <Button 
              variant="outline" 
              onClick={() => setIsModalOpen(false)}
              className="flex-1"
            >
              Close
            </Button>
          </div>
          
          <div className="text-xs text-gray-500">
            <p><strong>Note:</strong> This is an AI-generated draft. Please review and customize it before sending.</p>
          </div>
        </div>
      </Modal>
    </>
  );
};