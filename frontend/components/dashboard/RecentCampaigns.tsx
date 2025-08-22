'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { formatDate, getRelativeTime } from '@/lib/utils';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { Campaign } from '@/types';
import {
  EyeIcon, PencilIcon, TrashIcon, PlayIcon, PauseIcon
} from '@heroicons/react/24/outline';

interface RecentCampaignsProps {
  campaigns: Campaign[];
  onView?: (campaign: Campaign) => void;
  onEdit?: (campaign: Campaign) => void;
  onDelete?: (campaign: Campaign) => void;
  onPause?: (campaign: Campaign) => void;
  onResume?: (campaign: Campaign) => void;
}

const getStatusBadge = (status: Campaign['status']) => {
  const statusConfig = {
    draft: { variant: 'default' as const, label: 'Draft' },
    scheduled: { variant: 'warning' as const, label: 'Scheduled' },
    sending: { variant: 'primary' as const, label: 'Sending' },
    sent: { variant: 'success' as const, label: 'Sent' },
    paused: { variant: 'error' as const, label: 'Paused' },
  };

  const config = statusConfig[status];
  return <Badge variant={config.variant}>{config.label}</Badge>;
};

const getStatusIcon = (status: Campaign['status']) => {
  switch (status) {
    case 'sending':
      return <PlayIcon className="h-4 w-4" />;
    case 'paused':
      return <PauseIcon className="h-4 w-4" />;
    default:
      return null;
  }
};

export function RecentCampaigns({
  campaigns,
  onView,
  onEdit,
  onDelete,
  onPause,
  onResume,
}: RecentCampaignsProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Campaigns
          </h3>
          <Button variant="outline" size="sm">
            View All
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {campaigns.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">
                No campaigns yet. Create your first campaign to get started.
              </p>
            </div>
          ) : (
            campaigns.map((campaign, index) => (
              <motion.div
                key={campaign.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      {getStatusIcon(campaign.status)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {campaign.name}
                      </h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
                        {campaign.subject}
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                    <span>{campaign.recipients.length} recipients</span>
                    <span>•</span>
                    <span>{getRelativeTime(campaign.createdAt)}</span>
                    {campaign.scheduledAt && (
                      <>
                        <span>•</span>
                        <span>Scheduled: {formatDate(campaign.scheduledAt, 'MMM dd, yyyy HH:mm')}</span>
                      </>
                    )}
                  </div>
                </div>

                <div className="flex items-center space-x-2 ml-4">
                  {getStatusBadge(campaign.status)}
                  
                  <div className="flex items-center space-x-1">
                    {onView && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onView(campaign)}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </Button>
                    )}
                    
                    {onEdit && campaign.status === 'draft' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onEdit(campaign)}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </Button>
                    )}
                    
                    {onPause && campaign.status === 'sending' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onPause(campaign)}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <PauseIcon className="h-4 w-4" />
                      </Button>
                    )}
                    
                    {onResume && campaign.status === 'paused' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onResume(campaign)}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <PlayIcon className="h-4 w-4" />
                      </Button>
                    )}
                    
                    {onDelete && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDelete(campaign)}
                        className="text-red-400 hover:text-red-600 dark:hover:text-red-300"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}
