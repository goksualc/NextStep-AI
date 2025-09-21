'use client';

import React from 'react';
import { Card } from '@/components/Card';
import { Button } from '@/components/Button';

interface Application {
  id: string;
  company: string;
  role: string;
  status: 'Applied' | 'Under Review' | 'Interview Scheduled' | 'Rejected' | 'Accepted';
  updated: string;
  matchScore?: number;
}

const mockApplications: Application[] = [
  {
    id: '1',
    company: 'TechCorp',
    role: 'Software Engineering Intern',
    status: 'Applied',
    updated: '2 hours ago',
    matchScore: 95
  },
  {
    id: '2',
    company: 'DataCorp',
    role: 'Data Science Intern',
    status: 'Interview Scheduled',
    updated: '1 day ago',
    matchScore: 88
  },
  {
    id: '3',
    company: 'StartupXYZ',
    role: 'Full Stack Developer Intern',
    status: 'Under Review',
    updated: '3 days ago',
    matchScore: 82
  },
  {
    id: '4',
    company: 'BigTech Inc',
    role: 'Product Management Intern',
    status: 'Rejected',
    updated: '1 week ago',
    matchScore: 65
  }
];

const getStatusColor = (status: Application['status']) => {
  switch (status) {
    case 'Applied':
      return 'bg-blue-100 text-blue-800';
    case 'Under Review':
      return 'bg-yellow-100 text-yellow-800';
    case 'Interview Scheduled':
      return 'bg-green-100 text-green-800';
    case 'Rejected':
      return 'bg-red-100 text-red-800';
    case 'Accepted':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function Applications() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Applications</h1>
          <p className="text-gray-600 mt-1">
            Track your internship applications and their progress
          </p>
        </div>
        <Button>
          ➕ New Application
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card padding="sm">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">8</p>
            <p className="text-sm text-gray-500">Total Applications</p>
          </div>
        </Card>
        <Card padding="sm">
          <div className="text-center">
            <p className="text-2xl font-bold text-yellow-600">3</p>
            <p className="text-sm text-gray-500">Under Review</p>
          </div>
        </Card>
        <Card padding="sm">
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">1</p>
            <p className="text-sm text-gray-500">Interviews</p>
          </div>
        </Card>
        <Card padding="sm">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-600">0</p>
            <p className="text-sm text-gray-500">Offers</p>
          </div>
        </Card>
      </div>

      {/* Applications Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Role
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Match Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Updated
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {mockApplications.map((application) => (
                <tr key={application.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-10 h-10 bg-gray-200 rounded-xl flex items-center justify-center">
                        <span className="text-sm font-medium text-gray-700">
                          {application.company.charAt(0)}
                        </span>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {application.company}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{application.role}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(application.status)}`}>
                      {application.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {application.matchScore && (
                      <div className="flex items-center">
                        <span className="text-sm font-medium text-gray-900 mr-2">
                          {application.matchScore}%
                        </span>
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${application.matchScore}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {application.updated}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button className="text-primary-600 hover:text-primary-900">
                      View
                    </button>
                    <button className="text-gray-600 hover:text-gray-900">
                      Edit
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Empty state if no applications */}
        {mockApplications.length === 0 && (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">📝</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No applications yet
            </h3>
            <p className="text-gray-600 mb-4">
              Start applying to internships to track your progress here.
            </p>
            <Button>
              Find Opportunities
            </Button>
          </div>
        )}
      </Card>
    </div>
  );
}