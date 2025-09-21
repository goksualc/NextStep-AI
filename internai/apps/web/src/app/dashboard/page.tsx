'use client';

import React, { useState } from 'react';
import { Card, Button, FileDrop, Input } from '@/components';
import { useUserStore } from '@/lib/store';
import { analyzeProfile, APIError } from '@/lib/api';

export default function Dashboard() {
  const { profile, setSkills, setLoading, setError, isLoading, error } = useUserStore();
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileUpload = (file: File) => {
    setSelectedFile(file);
  };

  const handleAnalyzeProfile = async () => {
    if (!linkedinUrl && !selectedFile) {
      setError('Please provide either a LinkedIn URL or upload a resume');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeProfile({
        linkedinUrl: linkedinUrl || undefined,
        resumeFile: selectedFile || undefined,
      });

      setSkills(result.skills);

      // Clear form
      setLinkedinUrl('');
      setSelectedFile(null);
    } catch (err) {
      if (err instanceof APIError) {
        setError(`Analysis failed: ${err.message}`);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setLoading(false);
    }
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
          Welcome back, {profile.name || 'John'}! 👋
        </h1>
        <p className="text-lg text-gray-600">
          Let&apos;s find your next amazing internship opportunity.
        </p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

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
              <p className="text-2xl font-bold text-gray-900">
                {profile.skills?.length ? Math.min(95, 60 + (profile.skills.length * 5)) : 0}%
              </p>
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
              <p className="text-sm font-medium text-gray-500">Skills Identified</p>
              <p className="text-2xl font-bold text-gray-900">
                {profile.skills?.length || 0}
              </p>
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
        {/* Analyze Profile */}
        <Card>
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Analyze Your Profile
              </h3>
              <p className="text-gray-600">
                Upload your resume or provide your LinkedIn URL to extract skills and get better matches.
              </p>
            </div>

            <div className="space-y-4">
              <Input
                label="LinkedIn Profile URL (Optional)"
                type="url"
                placeholder="https://linkedin.com/in/yourprofile"
                value={linkedinUrl}
                onChange={(e) => setLinkedinUrl(e.target.value)}
                helperText="We&apos;ll analyze your LinkedIn profile to extract relevant skills"
              />

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Or Upload Resume (Optional)
                </label>
                <FileDrop
                  onFileSelect={handleFileUpload}
                  accept=".pdf,.doc,.docx"
                  maxSize={5}
                />
              </div>

              <Button
                onClick={handleAnalyzeProfile}
                size="lg"
                className="w-full"
                disabled={isLoading || (!linkedinUrl && !selectedFile)}
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                    Analyzing...
                  </>
                ) : (
                  '🔍 Analyze Profile'
                )}
              </Button>
            </div>
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

      {/* Skills Display */}
      {profile.skills && profile.skills.length > 0 && (
        <Card>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">
              Your Skills
            </h3>
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </Card>
      )}

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
