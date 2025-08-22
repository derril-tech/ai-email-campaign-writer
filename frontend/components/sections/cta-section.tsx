'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles, Zap, Shield } from 'lucide-react'

export function CTASection() {
  return (
    <section className="py-20 lg:py-32 bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-black/10" />
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20" />
      
      <div className="container relative mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="mb-8"
          >
            <div className="inline-flex items-center rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm font-medium text-white backdrop-blur-sm">
              <Sparkles className="mr-2 h-4 w-4" />
              Limited Time Offer
              <span className="ml-2 rounded-full bg-white/20 px-2 py-0.5 text-xs">
                Save 50%
              </span>
            </div>
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            viewport={{ once: true }}
            className="mb-6 text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl"
          >
            Ready to transform your
            <span className="block">email marketing?</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            viewport={{ once: true }}
            className="mb-8 text-xl text-blue-100"
          >
            Join thousands of marketers who are already creating better campaigns with AI.
            Start your free trial today and see the difference.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            viewport={{ once: true }}
            className="mb-12 flex flex-col items-center justify-center gap-4 sm:flex-row"
          >
            <Link href="/auth/register">
              <Button size="lg" className="group bg-white text-blue-600 hover:bg-blue-50">
                Start Free Trial
                <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="/demo">
              <Button variant="outline" size="lg" className="border-white/20 text-white hover:bg-white/10">
                Watch Demo
              </Button>
            </Link>
          </motion.div>

          {/* Features */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            viewport={{ once: true }}
            className="grid grid-cols-1 gap-6 sm:grid-cols-3"
          >
            <div className="flex items-center justify-center space-x-3 text-white">
              <Zap className="h-5 w-5 text-yellow-300" />
              <span className="text-sm font-medium">No credit card required</span>
            </div>
            <div className="flex items-center justify-center space-x-3 text-white">
              <Shield className="h-5 w-5 text-green-300" />
              <span className="text-sm font-medium">14-day free trial</span>
            </div>
            <div className="flex items-center justify-center space-x-3 text-white">
              <Sparkles className="h-5 w-5 text-purple-300" />
              <span className="text-sm font-medium">Cancel anytime</span>
            </div>
          </motion.div>

          {/* Trust indicators */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            viewport={{ once: true }}
            className="mt-12 border-t border-white/20 pt-8"
          >
            <p className="text-sm text-blue-200 mb-4">Trusted by leading companies worldwide</p>
            <div className="flex items-center justify-center space-x-8 opacity-60">
              <div className="h-8 w-20 bg-white/20 rounded"></div>
              <div className="h-8 w-20 bg-white/20 rounded"></div>
              <div className="h-8 w-20 bg-white/20 rounded"></div>
              <div className="h-8 w-20 bg-white/20 rounded"></div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
