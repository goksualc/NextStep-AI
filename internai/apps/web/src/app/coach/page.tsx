'use client';

import React from 'react';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';

export default function Coach() {
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
        <Button>
          🎯 Get Coaching
        </Button>
      </div>

      {/* Empty State */}
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
    </div>
  );
}
