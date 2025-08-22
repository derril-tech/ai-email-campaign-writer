'use client';

import React, { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { motion } from 'framer-motion';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Badge } from '@/components/ui/Badge';
import { CampaignForm as CampaignFormType } from '@/types';
import { CAMPAIGN_TYPES } from '@/lib/constants';
import {
  SparklesIcon, EnvelopeIcon, UsersIcon, CalendarIcon,
  DocumentTextIcon, EyeIcon, EyeSlashIcon
} from '@heroicons/react/24/outline';

interface CampaignFormProps {
  initialData?: Partial<CampaignFormType>;
  onSubmit: (data: CampaignFormType) => void;
  onCancel?: () => void;
  isLoading?: boolean;
  onAIGenerate?: (type: 'subject' | 'content' | 'both') => Promise<void>;
  isAIGenerating?: boolean;
}

export function CampaignForm({
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
  onAIGenerate,
  isAIGenerating = false,
}: CampaignFormProps) {
  const [showPreview, setShowPreview] = useState(false);
  const [previewMode, setPreviewMode] = useState<'desktop' | 'mobile'>('desktop');

  const {
    control,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid },
  } = useForm<CampaignFormType>({
    defaultValues: {
      name: initialData?.name || '',
      subject: initialData?.subject || '',
      content: initialData?.content || '',
      type: initialData?.type || 'newsletter',
      scheduledAt: initialData?.scheduledAt || '',
      senderName: initialData?.senderName || '',
      senderEmail: initialData?.senderEmail || '',
      tags: initialData?.tags || [],
      ...initialData,
    },
    mode: 'onChange',
  });

  const watchedContent = watch('content');
  const watchedSubject = watch('subject');

  const campaignTypeOptions = Object.entries(CAMPAIGN_TYPES).map(([value, label]) => ({
    value,
    label,
  }));

  const handleAIGenerate = async (type: 'subject' | 'content' | 'both') => {
    if (onAIGenerate) {
      await onAIGenerate(type);
    }
  };

  const handleFormSubmit = (data: CampaignFormType) => {
    onSubmit(data);
  };

  const wordCount = watchedContent?.split(/\s+/).filter(Boolean).length || 0;
  const characterCount = watchedContent?.length || 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Create New Campaign
            </h2>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowPreview(!showPreview)}
                leftIcon={showPreview ? <EyeSlashIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
              >
                {showPreview ? 'Hide Preview' : 'Preview'}
              </Button>
              {showPreview && (
                <div className="flex items-center space-x-1">
                  <Button
                    variant={previewMode === 'desktop' ? 'primary' : 'outline'}
                    size="sm"
                    onClick={() => setPreviewMode('desktop')}
                  >
                    Desktop
                  </Button>
                  <Button
                    variant={previewMode === 'mobile' ? 'primary' : 'outline'}
                    size="sm"
                    onClick={() => setPreviewMode('mobile')}
                  >
                    Mobile
                  </Button>
                </div>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Controller
                name="name"
                control={control}
                rules={{ required: 'Campaign name is required' }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Campaign Name"
                    placeholder="Enter campaign name"
                    error={errors.name?.message}
                    leftIcon={<EnvelopeIcon className="h-4 w-4" />}
                    fullWidth
                  />
                )}
              />

              <Controller
                name="type"
                control={control}
                rules={{ required: 'Campaign type is required' }}
                render={({ field }) => (
                  <Select
                    options={campaignTypeOptions}
                    value={field.value}
                    onChange={field.onChange}
                    label="Campaign Type"
                    error={errors.type?.message}
                    fullWidth
                  />
                )}
              />
            </div>

            {/* Subject Line */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Subject Line
                </label>
                {onAIGenerate && (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => handleAIGenerate('subject')}
                    loading={isAIGenerating}
                    leftIcon={<SparklesIcon className="h-4 w-4" />}
                  >
                    AI Generate
                  </Button>
                )}
              </div>
              <Controller
                name="subject"
                control={control}
                rules={{ required: 'Subject line is required' }}
                render={({ field }) => (
                  <Input
                    {...field}
                    placeholder="Enter email subject line"
                    error={errors.subject?.message}
                    fullWidth
                  />
                )}
              />
            </div>

            {/* Content */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Email Content
                </label>
                <div className="flex items-center space-x-2">
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {wordCount} words • {characterCount} characters
                  </span>
                  {onAIGenerate && (
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => handleAIGenerate('content')}
                      loading={isAIGenerating}
                      leftIcon={<SparklesIcon className="h-4 w-4" />}
                    >
                      AI Generate
                    </Button>
                  )}
                </div>
              </div>
              <Controller
                name="content"
                control={control}
                rules={{ required: 'Email content is required' }}
                render={({ field }) => (
                  <Textarea
                    {...field}
                    placeholder="Write your email content here..."
                    error={errors.content?.message}
                    showCharacterCount
                    maxLength={5000}
                    rows={12}
                    fullWidth
                  />
                )}
              />
            </div>

            {/* Sender Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Controller
                name="senderName"
                control={control}
                rules={{ required: 'Sender name is required' }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Sender Name"
                    placeholder="Enter sender name"
                    error={errors.senderName?.message}
                    leftIcon={<UsersIcon className="h-4 w-4" />}
                    fullWidth
                  />
                )}
              />

              <Controller
                name="senderEmail"
                control={control}
                rules={{ 
                  required: 'Sender email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                  }
                }}
                render={({ field }) => (
                  <Input
                    {...field}
                    label="Sender Email"
                    placeholder="Enter sender email"
                    error={errors.senderEmail?.message}
                    leftIcon={<EnvelopeIcon className="h-4 w-4" />}
                    fullWidth
                  />
                )}
              />
            </div>

            {/* Scheduling */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Schedule Campaign (Optional)
              </label>
              <Controller
                name="scheduledAt"
                control={control}
                render={({ field }) => (
                  <Input
                    {...field}
                    type="datetime-local"
                    leftIcon={<CalendarIcon className="h-4 w-4" />}
                    fullWidth
                  />
                )}
              />
            </div>

            {/* Tags */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Tags (Optional)
              </label>
              <div className="flex flex-wrap gap-2">
                {watch('tags')?.map((tag, index) => (
                  <Badge key={index} variant="primary">
                    {tag}
                    <button
                      type="button"
                      onClick={() => {
                        const newTags = watch('tags')?.filter((_, i) => i !== index) || [];
                        setValue('tags', newTags);
                      }}
                      className="ml-1 hover:text-red-500"
                    >
                      ×
                    </button>
                  </Badge>
                ))}
              </div>
              <Input
                placeholder="Add a tag and press Enter"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    const input = e.target as HTMLInputElement;
                    const tag = input.value.trim();
                    if (tag && !watch('tags')?.includes(tag)) {
                      const newTags = [...(watch('tags') || []), tag];
                      setValue('tags', newTags);
                      input.value = '';
                    }
                  }
                }}
                fullWidth
              />
            </div>

            {/* Form Actions */}
            <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
              {onCancel && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={onCancel}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
              )}
              <Button
                type="submit"
                loading={isLoading}
                disabled={!isValid || isLoading}
              >
                {initialData ? 'Update Campaign' : 'Create Campaign'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Preview */}
      {showPreview && (
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Email Preview
            </h3>
          </CardHeader>
          <CardContent>
            <div className={`border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden ${
              previewMode === 'mobile' ? 'max-w-sm mx-auto' : 'max-w-2xl'
            }`}>
              <div className="bg-gray-50 dark:bg-gray-800 px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <DocumentTextIcon className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Preview
                  </span>
                </div>
              </div>
              <div className="p-6 bg-white dark:bg-gray-900">
                <div className="mb-4">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {watchedSubject || 'Subject Line Preview'}
                  </h2>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    From: {watch('senderName') || 'Sender Name'} &lt;{watch('senderEmail') || 'sender@example.com'}&gt;
                  </p>
                </div>
                <div className="prose prose-sm max-w-none dark:prose-invert">
                  <div dangerouslySetInnerHTML={{ 
                    __html: watchedContent || '<p>Email content preview will appear here...</p>' 
                  }} />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
