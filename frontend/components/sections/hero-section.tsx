'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles, Mail, BarChart3, Users, Zap } from 'lucide-react'

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 py-20 lg:py-32">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))] dark:bg-grid-slate-700/25 dark:[mask-image:linear-gradient(0deg,rgba(255,255,255,0.1),rgba(255,255,255,0.5))]" />
      
      <div className="container relative mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <div className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 dark:border-blue-800 dark:bg-blue-900/20 dark:text-blue-300">
              <Sparkles className="mr-2 h-4 w-4" />
              AI-Powered Email Campaigns
              <span className="ml-2 rounded-full bg-blue-100 px-2 py-0.5 text-xs dark:bg-blue-800/30">
                New
              </span>
            </div>
          </motion.div>

          {/* Main heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="mb-6 text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl lg:text-6xl"
          >
            Create Engaging Email Campaigns
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              with AI Magic
            </span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mb-8 text-lg text-slate-600 dark:text-slate-400 sm:text-xl"
          >
            Transform your email marketing with AI-powered content generation, 
            intelligent audience targeting, and advanced analytics. 
            Create campaigns that convert in minutes, not hours.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mb-12 flex flex-col items-center justify-center gap-4 sm:flex-row"
          >
            <Link href="/auth/register">
              <Button size="lg" className="group">
                Start Creating Free
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="#demo">
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="grid grid-cols-2 gap-8 border-t border-slate-200 pt-8 dark:border-slate-700 sm:grid-cols-4"
          >
            <div className="text-center">
              <div className="mb-2 flex justify-center">
                <Mail className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">10M+</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">Emails Sent</div>
            </div>
            <div className="text-center">
              <div className="mb-2 flex justify-center">
                <BarChart3 className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">45%</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">Avg Open Rate</div>
            </div>
            <div className="text-center">
              <div className="mb-2 flex justify-center">
                <Users className="h-8 w-8 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">50K+</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">Active Users</div>
            </div>
            <div className="text-center">
              <div className="mb-2 flex justify-center">
                <Zap className="h-8 w-8 text-orange-600 dark:text-orange-400" />
              </div>
              <div className="text-2xl font-bold text-slate-900 dark:text-white">90%</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">Faster Creation</div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Floating elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl" />
        <div className="absolute -bottom-40 -left-40 h-80 w-80 rounded-full bg-gradient-to-tr from-green-400/20 to-blue-400/20 blur-3xl" />
      </div>
    </section>
  )
}
