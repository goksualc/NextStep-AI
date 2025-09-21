'use client';

import React from 'react';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';

export default function Matches() {
  const hasMatches = false; // This would come from your state/API

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Your Matches</h1>
          <p className="text-gray-600 mt-1">
            AI-powered job matches tailored to your profile
          </p>
        </div>
        <Button>
          🔄 Refresh Matches
        </Button>
      </div>

      {hasMatches ? (
        /* Matches Grid - This would show when there are matches */
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Match cards would go here */}
        </div>
      ) : (
        /* Empty State */
        <Card padding="lg" className="text-center">
          <div className="max-w-md mx-auto space-y-6">
            {/* Icon */}
            <div className="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto">
              <span className="text-4xl">🎯</span>
            </div>

            {/* Content */}
            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-gray-900">
                No matches yet
              </h3>
              <p className="text-gray-600">
                We&apos;re working hard to find the perfect internship opportunities for you. 
                Upload your resume and complete your profile to get better matches.
              </p>
            </div>

            {/* Actions */}
            <div className="space-y-3">
              <Button size="lg" className="w-full">
                📄 Upload Resume
              </Button>
              <Button variant="outline" size="lg" className="w-full">
                🔍 Search Jobs Manually
              </Button>
            </div>

            {/* Help Text */}
            <div className="text-sm text-gray-500 pt-4 border-t border-gray-100">
              <p>
                <strong>Tip:</strong> Complete your profile and upload your resume to get 
                personalized matches within 24 hours.
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* How Matching Works */}
      <Card>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-gray-900">
            How Our Matching Works
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">📊</span>
              </div>
              <h4 className="font-semibold text-gray-900">Profile Analysis</h4>
              <p className="text-sm text-gray-600">
                We analyze your skills, experience, and preferences to understand what you&apos;re looking for.
              </p>
            </div>

            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">🤖</span>
              </div>
              <h4 className="font-semibold text-gray-900">AI Matching</h4>
              <p className="text-sm text-gray-600">
                Our AI compares your profile with thousands of internship opportunities to find the best fits.
              </p>
            </div>

            <div className="text-center space-y-3">
              <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">📈</span>
              </div>
              <h4 className="font-semibold text-gray-900">Smart Ranking</h4>
              <p className="text-sm text-gray-600">
                Matches are ranked by compatibility, company culture fit, and your career goals.
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}