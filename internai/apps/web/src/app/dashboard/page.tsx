'use client';

import React, { useState } from 'react';
import { Card, Button, FileDrop, Input, Textarea, SkillChip } from '@/components';
import { useUserStore } from '@/lib/store';
import { analyzeProfile, getSampleJobs, matchJobs, APIError } from '@/lib/api';

export default function Dashboard() {
  const {
    profile,
    setSkills,
    setMissingSkills,
    setHighlights,
    setProfileText,
    setLoading,
    setError,
    isLoading,
    error
  } = useUserStore();
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');

  const handleFileUpload = (file: File) => {
    setSelectedFile(file);
  };

  const handleAnalyzeProfile = async () => {
    if (!resumeText.trim()) {
      setError('Please provide resume text to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeProfile({
        text: resumeText,
      });

      setSkills(result.skills);
      setHighlights(result.highlights);
      setProfileText(result.profile_text);

      // Get missing skills by running a sample match
      try {
        const sampleJobs = await getSampleJobs();
        const matches = await matchJobs({
          profile: { ...profile, skills: result.skills },
          jobs: sampleJobs.slice(0, 3) // Only match against first 3 jobs for speed
        });

        // Collect unique missing skills from all matches
        const allMissingSkills = matches.flatMap(match => match.missing_skills || []);
        const uniqueMissingSkills = [...new Set(allMissingSkills)].slice(0, 5); // Top 5 unique missing skills
        setMissingSkills(uniqueMissingSkills);
      } catch (matchErr) {
        console.log('Could not get missing skills:', matchErr);
        // Continue without missing skills
      }

      // Clear form
      setResumeText('');
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
                Paste your resume text to extract skills and get personalized job matches.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Resume Text
                </label>
                <Textarea
                  placeholder="Paste your resume content here... Include your experience, skills, education, and achievements."
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  rows={8}
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  We&apos;ll analyze this text to extract your skills and highlights using AI.
                </p>
              </div>

              <Button
                onClick={handleAnalyzeProfile}
                size="lg"
                className="w-full"
                disabled={isLoading || !resumeText.trim()}
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
                <SkillChip
                  key={index}
                  skill={skill}
                  type="skill"
                  size="md"
                />
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Highlights Display */}
      {profile.highlights && profile.highlights.length > 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-blue-600 text-sm font-semibold">⭐</span>
              </div>
              <h3 className="text-xl font-semibold text-blue-900">
                Key Highlights
              </h3>
            </div>
            <div className="space-y-2">
              {profile.highlights.map((highlight, index) => (
                <div key={index} className="flex items-start space-x-2">
                  <span className="text-blue-600 mt-1">•</span>
                  <p className="text-blue-800 text-sm">{highlight}</p>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}

      {/* Missing Skills Display */}
      {profile.missing_skills && profile.missing_skills.length > 0 && (
        <Card className="bg-orange-50 border-orange-200">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <span className="text-orange-600 text-sm font-semibold">📈</span>
              </div>
              <h3 className="text-xl font-semibold text-orange-900">
                Top Missing Skills
              </h3>
            </div>
            <p className="text-sm text-orange-700">
              These skills appear frequently in job postings but are missing from your profile. Consider learning them to improve your match scores!
            </p>
            <div className="flex flex-wrap gap-2">
              {profile.missing_skills.map((skill, index) => (
                <SkillChip
                  key={index}
                  skill={skill}
                  type="missing"
                  size="md"
                />
              ))}
            </div>
            <div className="text-xs text-orange-600">
              💡 <strong>Tip:</strong> Focus on 1-2 skills that align with your career goals and start learning them through online courses or projects.
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
