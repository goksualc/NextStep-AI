'use client';

import React, { useState, useEffect } from 'react';
import { Card, Button } from '@/components';

interface Agent {
  key: string;
  name: string;
  id: string;
}

interface AgentsResponse {
  agents: Agent[];
  status: string;
  count: number;
  error?: string;
  message?: string;
}

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [status, setStatus] = useState<string>('loading');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchAgents = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/v1/agents');

      if (!response.ok) {
        throw new Error(`Failed to fetch agents: ${response.statusText}`);
      }

      const data: AgentsResponse = await response.json();

      if (data.error) {
        setError(data.error);
        setStatus('error');
      } else {
        setAgents(data.agents);
        setStatus(data.status);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setStatus('error');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'cached':
        return 'text-green-600 bg-green-100';
      case 'no_cache':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'cached':
        return 'Registered';
      case 'no_cache':
        return 'Not Registered';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Coral Agents</h1>
          <p className="text-gray-600 mt-1">
            AI agents registered with the Coral distributed computing platform
          </p>
        </div>
        <Button
          onClick={fetchAgents}
          disabled={isLoading}
          variant="outline"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-transparent mr-2"></div>
              Loading...
            </>
          ) : (
            '🔄 Refresh'
          )}
        </Button>
      </div>

      {/* Status Banner */}
      <Card className="bg-blue-50 border-blue-200">
        <div className="flex items-center space-x-3">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-blue-600 text-sm font-semibold">🤖</span>
            </div>
          </div>
          <div className="flex-1">
            <h3 className="text-sm font-medium text-blue-900">
              Coral Integration Status
            </h3>
            <p className="text-sm text-blue-700">
              {status === 'cached' && `${agents.length} agents registered and ready for distributed execution`}
              {status === 'no_cache' && 'No agents registered yet. Agents will be registered on API startup.'}
              {status === 'error' && 'Unable to connect to Coral or fetch agent status.'}
              {status === 'loading' && 'Checking agent registration status...'}
            </p>
          </div>
          <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
            {getStatusLabel(status)}
          </div>
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
              <h3 className="text-sm font-medium text-red-800">Error Loading Agents</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </Card>
      )}

      {/* Agents List */}
      {agents.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Card key={agent.key} className="hover:shadow-soft-lg transition-shadow duration-200">
              <div className="space-y-4">
                {/* Agent Header */}
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {agent.name}
                    </h3>
                    <p className="text-sm text-gray-600 font-mono">
                      {agent.key}
                    </p>
                  </div>
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                      <span className="text-green-600 text-sm">✓</span>
                    </div>
                  </div>
                </div>

                {/* Agent Details */}
                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                      Agent ID
                    </p>
                    <p className="text-sm font-mono text-gray-900 break-all">
                      {agent.id || 'Not assigned'}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">
                      Status
                    </p>
                    <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      <div className="w-2 h-2 bg-green-400 rounded-full mr-1.5"></div>
                      Active
                    </div>
                  </div>
                </div>

                {/* Agent Description */}
                <div className="pt-2 border-t border-gray-100">
                  <p className="text-xs text-gray-600">
                    {agent.key === 'cv_analyzer' && 'Extracts skills and highlights from resumes and LinkedIn profiles'}
                    {agent.key === 'job_scout' && 'Discovers and curates relevant job opportunities'}
                    {agent.key === 'matcher' && 'Matches user profiles with job opportunities using AI'}
                    {agent.key === 'app_writer' && 'Generates personalized cover letters and application materials'}
                    {agent.key === 'coach' && 'Provides interview preparation and career coaching'}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        /* Empty State */
        <Card className="text-center py-12">
          <div className="max-w-md mx-auto space-y-4">
            <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto">
              <span className="text-2xl">🤖</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                No Agents Registered
              </h3>
              <p className="text-gray-600 mt-1">
                {status === 'no_cache'
                  ? 'Agents will be automatically registered when the API server starts with Coral configuration.'
                  : 'Unable to load agent information. Please check your Coral connection.'
                }
              </p>
            </div>
            <Button onClick={fetchAgents} variant="outline">
              Try Again
            </Button>
          </div>
        </Card>
      )}

      {/* Coral Information */}
      <Card>
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            About Coral Integration
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">What is Coral?</h4>
              <p className="text-sm text-gray-600">
                Coral is a distributed computing platform that enables AI agents to run across multiple servers and scale automatically based on demand.
              </p>
            </div>
            <div className="space-y-3">
              <h4 className="font-medium text-gray-900">Benefits</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Scalable AI agent execution</li>
                <li>• Distributed workload processing</li>
                <li>• High availability and reliability</li>
                <li>• Easy agent management and monitoring</li>
              </ul>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
