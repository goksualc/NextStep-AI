'use client';

import React, { useState } from 'react';
import { Card, Button, Input } from '@/components';
import { useUserStore } from '@/lib/store';
import { coachPrep, APIError } from '@/lib/api';
import { CoachResponse } from '@/lib/types';

export default function Coach() {
  const { profile } = useUserStore();
  const [role, setRole] = useState('');
  const [company, setCompany] = useState('');
  const [coaching, setCoaching] = useState<CoachResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedQuestion, setExpandedQuestion] = useState<number | null>(null);

  const handleGetCoaching = async () => {
    if (!role.trim()) {
      setError('Please enter a role');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const result = await coachPrep({
        role: role.trim(),
        company: company.trim() || undefined,
        profile: profile
      });

      setCoaching(result);
    } catch (err) {
      if (err instanceof APIError) {
        setError(`Coaching failed: ${err.message}`);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Interview Coach</h1>
          <p className="text-gray-600 mt-1">
            Get personalized coaching and interview preparation
          </p>
        </div>
      </div>

      {/* Input Form */}
      <Card>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-gray-900">
            Get Interview Coaching
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Target Role"
              placeholder="e.g., Software Engineering Intern"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              required
            />
            <Input
              label="Company (Optional)"
              placeholder="e.g., TechCorp"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </div>

          <Button
            onClick={handleGetCoaching}
            disabled={isLoading || !role.trim()}
            size="lg"
            className="w-full md:w-auto"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                Generating...
              </>
            ) : (
              '🎯 Get Coaching'
            )}
          </Button>
        </div>
      </Card>

      {/* Error Display */}
      {error && (
        <Card className="bg-red-50 border-red-200">
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
        </Card>
      )}

      {/* Coaching Results */}
      {coaching && (
        <div className="space-y-6">
          {/* Questions */}
          <Card>
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-gray-900">
                Interview Questions & Answers
              </h3>
              <div className="space-y-4">
                {coaching.questions.map((question, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <h4 className="font-medium text-gray-900 mb-2">
                        {question.q}
                      </h4>
                      <button
                        onClick={() => setExpandedQuestion(expandedQuestion === index ? null : index)}
                        className="text-primary-600 hover:text-primary-800 text-sm font-medium"
                      >
                        {expandedQuestion === index ? 'Hide Answer' : 'Show Answer'}
                      </button>
                    </div>
                    {expandedQuestion === index && (
                      <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                        <p className="text-sm text-blue-800">
                          <strong>Ideal Answer:</strong> {question.ideal_answer}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </Card>

          {/* Tips */}
          <Card>
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-gray-900">
                Interview Tips
              </h3>
              <div className="space-y-3">
                {coaching.tips.map((tip, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                    <span className="text-green-600 mt-1">💡</span>
                    <p className="text-sm text-green-800">{tip}</p>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Empty State */}
      {!coaching && !isLoading && (
        <Card padding="lg" className="text-center">
        <div className="max-w-2xl mx-auto space-y-6">
          {/* Icon */}
          <div className="w-32 h-32 bg-gradient-to-br from-primary-100 to-purple-100 rounded-3xl flex items-center justify-center mx-auto">
            <span className="text-6xl">💼</span>
          </div>

          {/* Content */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">
              Your AI Interview Coach is Ready
            </h2>
            <p className="text-lg text-gray-600 max-w-lg mx-auto">
              Get personalized interview preparation, practice questions, and career guidance
              tailored to your profile and target roles.
            </p>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
            <div className="space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">🎯</span>
              </div>
              <h3 className="font-semibold text-gray-900">Practice Questions</h3>
              <p className="text-sm text-gray-600">
                Get role-specific interview questions and practice with AI feedback
              </p>
            </div>

            <div className="space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">📝</span>
              </div>
              <h3 className="font-semibold text-gray-900">Resume Review</h3>
              <p className="text-sm text-gray-600">
                Get detailed feedback on your resume and suggestions for improvement
              </p>
            </div>

            <div className="space-y-3">
              <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-xl">💡</span>
              </div>
              <h3 className="font-semibold text-gray-900">Career Advice</h3>
              <p className="text-sm text-gray-600">
                Receive personalized career guidance and skill development recommendations
              </p>
            </div>
          </div>

          {/* CTA */}
          <div className="space-y-4 pt-6">
            <div className="space-y-3">
              <Button size="lg" className="w-full md:w-auto">
                🚀 Start Coaching Session
              </Button>
              <Button variant="outline" size="lg" className="w-full md:w-auto">
                📋 Upload Resume for Review
              </Button>
            </div>

            <p className="text-sm text-gray-500">
              Free for your first session • Takes 5-10 minutes
            </p>
          </div>
        </div>
      </Card>

      {/* How It Works */}
      <Card>
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900 text-center">
            How Interview Coaching Works
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-gray-900">Upload Profile</h4>
                <p className="text-sm text-gray-600">
                  Upload your resume and tell us about your career goals
                </p>
              </div>
            </div>

            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-2xl font-bold text-blue-600">2</span>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-gray-900">AI Analysis</h4>
                <p className="text-sm text-gray-600">
                  Our AI analyzes your profile and identifies areas for improvement
                </p>
              </div>
            </div>

            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-2xl font-bold text-green-600">3</span>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-gray-900">Practice Session</h4>
                <p className="text-sm text-gray-600">
                  Practice interview questions with real-time feedback and tips
                </p>
              </div>
            </div>

            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto">
                <span className="text-2xl font-bold text-purple-600">4</span>
              </div>
              <div className="space-y-2">
                <h4 className="font-semibold text-gray-900">Get Recommendations</h4>
                <p className="text-sm text-gray-600">
                  Receive personalized advice and action items for improvement
                </p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Quick Tips */}
      <Card>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-gray-900">
            Quick Interview Tips
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start space-x-3 p-4 bg-blue-50 rounded-xl">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-blue-600 text-sm">💡</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Research the Company</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Learn about their mission, values, and recent news before your interview.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3 p-4 bg-green-50 rounded-xl">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-sm">🎯</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Practice STAR Method</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Structure your answers with Situation, Task, Action, and Result.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3 p-4 bg-yellow-50 rounded-xl">
              <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-yellow-600 text-sm">❓</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Prepare Questions</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Have thoughtful questions ready to ask about the role and company.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3 p-4 bg-purple-50 rounded-xl">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-purple-600 text-sm">⏰</span>
              </div>
              <div>
                <h4 className="font-medium text-gray-900">Be Punctual</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Arrive 5-10 minutes early for in-person interviews or test your tech beforehand.
                </p>
              </div>
            </div>
          </div>
        </div>
      </Card>
      )}
    </div>
  );
}
