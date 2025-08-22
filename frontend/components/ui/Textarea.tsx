'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { AlertCircle, CheckCircle } from 'lucide-react';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  success?: string;
  helperText?: string;
  fullWidth?: boolean;
  showCharacterCount?: boolean;
  maxLength?: number;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    {
      className,
      label,
      error,
      success,
      helperText,
      fullWidth = false,
      showCharacterCount = false,
      maxLength,
      id,
      ...props
    },
    ref
  ) => {
    const textareaId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`;
    const baseClasses = 'block w-full px-3 py-2 border rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-0 disabled:opacity-50 disabled:cursor-not-allowed resize-vertical';
    
    const stateClasses = {
      default: 'border-gray-300 dark:border-gray-600 focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:text-white',
      error: 'border-red-300 dark:border-red-600 focus:border-red-500 focus:ring-red-500 dark:bg-gray-800 dark:text-white',
      success: 'border-green-300 dark:border-green-600 focus:border-green-500 focus:ring-green-500 dark:bg-gray-800 dark:text-white',
    };

    const getStateClass = () => {
      if (error) return stateClasses.error;
      if (success) return stateClasses.success;
      return stateClasses.default;
    };

    const widthClass = fullWidth ? 'w-full' : '';

    return (
      <div className={cn('space-y-1', widthClass)}>
        {label && (
          <label
            htmlFor={textareaId}
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            {label}
          </label>
        )}
        
        <div className="relative">
          <textarea
            id={textareaId}
            className={cn(baseClasses, getStateClass(), className)}
            ref={ref}
            maxLength={maxLength}
            {...props}
          />
          
          {(error || success) && (
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              {error && <AlertCircle className="h-4 w-4 text-red-500" />}
              {success && <CheckCircle className="h-4 w-4 text-green-500" />}
            </div>
          )}
        </div>
        
        {(error || success || helperText || (showCharacterCount && maxLength)) && (
          <div className="flex justify-between items-start">
            <div className="text-sm">
              {error && <p className="text-red-600 dark:text-red-400">{error}</p>}
              {success && <p className="text-green-600 dark:text-green-400">{success}</p>}
              {helperText && !error && !success && (
                <p className="text-gray-500 dark:text-gray-400">{helperText}</p>
              )}
            </div>
            
            {showCharacterCount && maxLength && (
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {props.value?.toString().length || 0}/{maxLength}
              </span>
            )}
          </div>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';

export { Textarea };
