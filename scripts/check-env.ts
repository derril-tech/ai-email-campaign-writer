#!/usr/bin/env node

/**
 * Environment Variable Validation Script
 * 
 * This script checks that all required environment variables are set
 * and have valid values. It fails fast if any required variables are missing.
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

interface EnvConfig {
  required: string[];
  optional: string[];
  validation?: Record<string, (value: string) => boolean>;
}

const envConfigs: Record<string, EnvConfig> = {
  frontend: {
    required: [
      'NEXT_PUBLIC_API_URL',
      'NEXTAUTH_URL',
      'NEXTAUTH_SECRET'
    ],
    optional: [
      'NEXT_PUBLIC_WS_URL',
      'NEXT_PUBLIC_SENTRY_DSN'
    ],
    validation: {
      'NEXT_PUBLIC_API_URL': (value) => value.startsWith('http'),
      'NEXTAUTH_URL': (value) => value.startsWith('http'),
      'NEXTAUTH_SECRET': (value) => value.length >= 32
    }
  },
  backend: {
    required: [
      'DATABASE_URL',
      'REDIS_URL',
      'SECRET_KEY',
      'ALGORITHM',
      'ACCESS_TOKEN_EXPIRE_MINUTES'
    ],
    optional: [
      'OPENAI_API_KEY',
      'SENDGRID_API_KEY',
      'SMTP_HOST',
      'SMTP_PORT',
      'SMTP_USERNAME',
      'SMTP_PASSWORD',
      'ENVIRONMENT',
      'DEBUG',
      'ALLOWED_HOSTS',
      'ALLOWED_ORIGINS'
    ],
    validation: {
      'DATABASE_URL': (value) => value.startsWith('postgresql://'),
      'REDIS_URL': (value) => value.startsWith('redis://'),
      'SECRET_KEY': (value) => value.length >= 32,
      'ACCESS_TOKEN_EXPIRE_MINUTES': (value) => !isNaN(Number(value)) && Number(value) > 0
    }
  }
};

function loadEnvFile(filePath: string): Record<string, string> {
  if (!existsSync(filePath)) {
    return {};
  }

  const content = readFileSync(filePath, 'utf-8');
  const env: Record<string, string> = {};

  content.split('\n').forEach(line => {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith('#')) {
      const [key, ...valueParts] = trimmed.split('=');
      if (key && valueParts.length > 0) {
        env[key] = valueParts.join('=').replace(/^["']|["']$/g, '');
      }
    }
  });

  return env;
}

function validateEnv(env: Record<string, string>, config: EnvConfig): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Check required variables
  for (const required of config.required) {
    if (!env[required]) {
      errors.push(`Missing required environment variable: ${required}`);
    }
  }

  // Validate variables that have validation rules
  if (config.validation) {
    for (const [key, validator] of Object.entries(config.validation)) {
      const value = env[key];
      if (value && !validator(value)) {
        errors.push(`Invalid value for environment variable: ${key}`);
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

function main() {
  const args = process.argv.slice(2);
  const target = args[0] || 'all';
  
  console.log(`🔍 Checking environment variables for: ${target}`);
  console.log('');

  let allValid = true;
  const allErrors: string[] = [];

  if (target === 'all' || target === 'frontend') {
    const frontendEnv = loadEnvFile(join(process.cwd(), 'frontend', '.env.local'));
    const frontendResult = validateEnv(frontendEnv, envConfigs.frontend);
    
    console.log('📱 Frontend Environment:');
    if (frontendResult.valid) {
      console.log('  ✅ All required variables are set');
    } else {
      console.log('  ❌ Missing or invalid variables:');
      frontendResult.errors.forEach(error => console.log(`    - ${error}`));
      allValid = false;
      allErrors.push(...frontendResult.errors.map(e => `Frontend: ${e}`));
    }
    console.log('');
  }

  if (target === 'all' || target === 'backend') {
    const backendEnv = loadEnvFile(join(process.cwd(), 'backend', '.env'));
    const backendResult = validateEnv(backendEnv, envConfigs.backend);
    
    console.log('🔧 Backend Environment:');
    if (backendResult.valid) {
      console.log('  ✅ All required variables are set');
    } else {
      console.log('  ❌ Missing or invalid variables:');
      backendResult.errors.forEach(error => console.log(`    - ${error}`));
      allValid = false;
      allErrors.push(...backendResult.errors.map(e => `Backend: ${e}`));
    }
    console.log('');
  }

  if (target === 'all' || target === 'root') {
    const rootEnv = loadEnvFile(join(process.cwd(), '.env'));
    console.log('🏠 Root Environment:');
    if (Object.keys(rootEnv).length === 0) {
      console.log('  ℹ️  No root .env file found (this is optional)');
    } else {
      console.log('  ✅ Root .env file exists');
    }
    console.log('');
  }

  // Summary
  console.log('📋 Summary:');
  if (allValid) {
    console.log('  ✅ All environment variables are properly configured');
    process.exit(0);
  } else {
    console.log('  ❌ Environment validation failed');
    console.log('');
    console.log('💡 To fix these issues:');
    console.log('  1. Copy the example environment files:');
    console.log('     cp frontend/env.example frontend/.env.local');
    console.log('     cp backend/env.example backend/.env');
    console.log('  2. Edit the files and set the required values');
    console.log('  3. Run this script again to validate');
    console.log('');
    console.log('🔗 Example files:');
    console.log('  - frontend/env.example');
    console.log('  - backend/env.example');
    
    process.exit(1);
  }
}

// Run the script
main();
