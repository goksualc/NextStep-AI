'use client';

import React, { useState } from 'react';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';
import { FileDrop } from '@/components/FileDrop';

export default function Dashboard() {
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = (file: File) => {
    setIsUploading(true);
    // TODO: Implement file upload logic
    console.log('Uploading file:', file.name);
    setTimeout(() => {
      setIsUploading(false);
    }, 2000);
  };

  const handleFindMatches = () => {
    // TODO: Implement find matches logic
    console.log('Finding matches...');
  };

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, John! 👋
        </h1>
        <p className="text-lg text-gray-600">
          Let&apos;s find your next amazing internship opportunity.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Profile Score</p>
              <p className="text-2xl font-bold text-gray-900">85%</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Active Matches</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">📝</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Applications</p>
              <p className="text-2xl font-bold text-gray-900">8</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center">
                <span className="text-2xl">💼</span>
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Interviews</p>
              <p className="text-2xl font-bold text-gray-900">3</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Resume */}
        <Card>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Upload Resume
              </h3>
              <p className="text-gray-600">
                Upload your latest resume to get better matches and personalized recommendations.
              </p>
            </div>
            
            <FileDrop
              onFileSelect={handleFileUpload}
              accept=".pdf,.doc,.docx"
              maxSize={5}
            />
            
            {isUploading && (
              <div className="flex items-center space-x-2 text-sm text-primary-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary-600 border-t-transparent"></div>
                <span>Processing your resume...</span>
              </div>
            )}
          </div>
        </Card>

        {/* Find Matches */}
        <Card>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Find New Matches
              </h3>
              <p className="text-gray-600">
                Discover new internship opportunities that match your skills and interests.
              </p>
            </div>
            
            <div className="space-y-4">
              <Button 
                onClick={handleFindMatches}
                size="lg"
                className="w-full"
              >
                🔍 Search for Matches
              </Button>
              
              <div className="text-sm text-gray-500">
                <p>Last search: 2 hours ago</p>
                <p>Found 12 new opportunities</p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-gray-900">
            Recent Activity
          </h3>
          
          <div className="space-y-3">
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-xl">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-green-600 text-sm">✓</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  Application submitted to TechCorp
                </p>
                <p className="text-xs text-gray-500">2 hours ago</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-xl">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-blue-600 text-sm">🎯</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  New match found: DataCorp Internship
                </p>
                <p className="text-xs text-gray-500">4 hours ago</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-xl">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-purple-600 text-sm">💡</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  Career advice: Update your LinkedIn profile
                </p>
                <p className="text-xs text-gray-500">1 day ago</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}