'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  EnvelopeIcon, UsersIcon, ChartBarIcon, ClockIcon,
  ArrowUpIcon, ArrowDownIcon
} from '@heroicons/react/24/outline';
import { Card, CardContent } from '@/components/ui/Card';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease';
  icon: React.ComponentType<{ className?: string }>;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  change,
  changeType,
  icon: Icon,
  color,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="h-full">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                {title}
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                {value}
              </p>
              {change !== undefined && (
                <div className="flex items-center mt-2">
                  {changeType === 'increase' ? (
                    <ArrowUpIcon className="h-4 w-4 text-green-500" />
                  ) : (
                    <ArrowDownIcon className="h-4 w-4 text-red-500" />
                  )}
                  <span
                    className={`text-sm font-medium ml-1 ${
                      changeType === 'increase' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                    }`}
                  >
                    {Math.abs(change)}%
                  </span>
                  <span className="text-sm text-gray-500 dark:text-gray-400 ml-1">
                    from last month
                  </span>
                </div>
              )}
            </div>
            <div className={`p-3 rounded-lg ${color}`}>
              <Icon className="h-6 w-6 text-white" />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

interface DashboardStatsProps {
  stats: {
    totalCampaigns: number;
    totalRecipients: number;
    openRate: number;
    clickRate: number;
    campaignsChange?: number;
    recipientsChange?: number;
    openRateChange?: number;
    clickRateChange?: number;
  };
}

export function DashboardStats({ stats }: DashboardStatsProps) {
  const statCards = [
    {
      title: 'Total Campaigns',
      value: stats.totalCampaigns.toLocaleString(),
      change: stats.campaignsChange,
      changeType: stats.campaignsChange && stats.campaignsChange > 0 ? 'increase' : 'decrease',
      icon: EnvelopeIcon,
      color: 'bg-blue-500',
    },
    {
      title: 'Total Recipients',
      value: stats.totalRecipients.toLocaleString(),
      change: stats.recipientsChange,
      changeType: stats.recipientsChange && stats.recipientsChange > 0 ? 'increase' : 'decrease',
      icon: UsersIcon,
      color: 'bg-green-500',
    },
    {
      title: 'Open Rate',
      value: `${stats.openRate}%`,
      change: stats.openRateChange,
      changeType: stats.openRateChange && stats.openRateChange > 0 ? 'increase' : 'decrease',
      icon: ChartBarIcon,
      color: 'bg-purple-500',
    },
    {
      title: 'Click Rate',
      value: `${stats.clickRate}%`,
      change: stats.clickRateChange,
      changeType: stats.clickRateChange && stats.clickRateChange > 0 ? 'increase' : 'decrease',
      icon: ClockIcon,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => (
        <StatCard
          key={stat.title}
          {...stat}
        />
      ))}
    </div>
  );
}
