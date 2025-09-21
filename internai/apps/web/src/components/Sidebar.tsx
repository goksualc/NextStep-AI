'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Card } from './Card';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: '📊' },
  { name: 'Matches', href: '/matches', icon: '🎯' },
  { name: 'Applications', href: '/applications', icon: '📝' },
  { name: 'Coach', href: '/coach', icon: '💼' },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 py-4 shadow-soft-lg border-r border-gray-100">
        {/* Logo */}
        <div className="flex h-16 shrink-0 items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Intern<span className="text-primary-600">AI</span>
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-2">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className={`sidebar-link ${isActive ? 'active' : ''}`}
                  >
                    <span className="text-xl mr-3">{item.icon}</span>
                    <span className="font-medium">{item.name}</span>
                  </Link>
                </li>
              );
            })}
          </ul>

          {/* Profile Section */}
          <div className="mt-auto">
            <Card padding="sm" shadow="none" className="border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
                  <span className="text-primary-600 font-semibold">JD</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    John Doe
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    Computer Science Student
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </nav>
      </div>
    </div>
  );
};
