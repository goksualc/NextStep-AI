'use client';

import React, { useState, useEffect } from 'react';
import { Card, Button, MatchCard, ProgressBar, SkillChip } from '@/components';
import { useUserStore } from '@/lib/store';
import { matchJobs, getSampleJobs, APIError } from '@/lib/api';
import { JobItem, MatchResult } from '@/lib/types';

interface Agent {
  key: string;
  name: string;
  id: string;
}

interface AgentsResponse {
  agents: Agent[];
  status: string;
  count: number;
}

export default function Matches() {
  const { profile } = useUserStore();
  const [matches, setMatches] = useState<MatchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [coralAgents, setCoralAgents] = useState<Agent[]>([]);
  const [showCoralBanner, setShowCoralBanner] = useState(false);

  // Check for Coral agents on component mount
  useEffect(() => {
    const checkCoralAgents = async () => {
      try {
        const response = await fetch('http://localhost:8000/v1/agents');
        if (response.ok) {
          const data: AgentsResponse = await response.json();
          setCoralAgents(data.agents);
          setShowCoralBanner(data.agents.length > 0);
        }
      } catch (err) {
        // Silently fail - banner won't show if agents can't be fetched
        console.log('Could not fetch Coral agents for banner');
      }
    };

    checkCoralAgents();
  }, []);

  const handleLoadSampleJobs = async () => {
    if (!profile.skills || profile.skills.length === 0) {
      setError('Please analyze your profile first to get personalized matches');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Load sample jobs from API
      const sampleJobs = await getSampleJobs();

      // Call the match API
      const results = await matchJobs({
        profile: profile,
        jobs: sampleJobs
      });

      setMatches(results);
    } catch (err) {
      if (err instanceof APIError) {
        setError(`Matching failed: ${err.message}`);
      } else {
        setError('An unexpected error occurred while loading matches');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleWriteCoverLetter = async (job: JobItem) => {
    // This will be handled by the MatchCard component
    console.log('Writing cover letter for:', job.title);
  };

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
        <Button
          onClick={handleLoadSampleJobs}
          disabled={isLoading || !profile.skills || profile.skills.length === 0}
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
              Loading...
            </>
          ) : (
            '🔄 Load Sample Jobs'
          )}
        </Button>
      </div>

      {/* Coral Banner */}
      {showCoralBanner && (
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                  <span className="text-blue-600 text-lg">🤖</span>
                </div>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-blue-900">
                  Powered by Coral
                </h3>
                <p className="text-sm text-blue-700">
                  {coralAgents.length} AI agents running on distributed infrastructure
                </p>
              </div>
            </div>
            <div className="flex-shrink-0">
              <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                <div className="w-2 h-2 bg-blue-400 rounded-full mr-2 animate-pulse"></div>
                Active
              </div>
            </div>
          </div>
        </Card>
      )}

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

      {matches.length > 0 ? (
        /* Matches Grid */
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {matches.map((match, index) => (
            <MatchCard
              key={match.job.id}
              title={match.job.title}
              company={match.job.company}
              location={match.job.location || 'Not specified'}
              score={match.score}
              onWriteCoverLetter={() => handleWriteCoverLetter(match.job)}
              description={match.job.desc}
              type="Internship"
              postedDate="2 days ago"
              missingSkills={match.missing_skills}
            />
          ))}
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
                {!profile.skills || profile.skills.length === 0
                  ? "Analyze your profile first"
                  : "No matches yet"
                }
              </h3>
              <p className="text-gray-600">
                {!profile.skills || profile.skills.length === 0
                  ? "Upload your resume or provide your LinkedIn URL on the dashboard to get personalized matches."
                  : "Click &quot;Load Sample Jobs&quot; to see AI-powered matches based on your skills."
                }
              </p>
            </div>

            {/* Actions */}
            <div className="space-y-3">
              {(!profile.skills || profile.skills.length === 0) ? (
                <Button size="lg" className="w-full" onClick={() => window.location.href = '/dashboard'}>
                  📄 Go to Dashboard
                </Button>
              ) : (
                <Button
                  size="lg"
                  className="w-full"
                  onClick={handleLoadSampleJobs}
                  disabled={isLoading}
                >
                  🔍 Load Sample Jobs
                </Button>
              )}
            </div>

            {/* Help Text */}
            <div className="text-sm text-gray-500 pt-4 border-t border-gray-100">
              <p>
                <strong>Tip:</strong> The more complete your profile, the better your matches will be.
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
