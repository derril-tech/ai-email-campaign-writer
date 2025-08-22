'use client'

import { motion } from 'framer-motion'
import { 
  Brain, 
  Target, 
  BarChart3, 
  Zap, 
  Shield, 
  Palette,
  Users,
  Mail,
  TrendingUp,
  Smartphone
} from 'lucide-react'

const features = [
  {
    icon: Brain,
    title: 'AI Content Generation',
    description: 'Generate compelling email content in seconds with advanced AI models. Get personalized subject lines, body copy, and calls-to-action.',
    color: 'text-blue-600 dark:text-blue-400'
  },
  {
    icon: Target,
    title: 'Smart Audience Targeting',
    description: 'Segment your audience intelligently and deliver personalized content that resonates with each subscriber group.',
    color: 'text-green-600 dark:text-green-400'
  },
  {
    icon: BarChart3,
    title: 'Advanced Analytics',
    description: 'Track performance with detailed analytics, A/B testing, and real-time insights to optimize your campaigns.',
    color: 'text-purple-600 dark:text-purple-400'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Create and send campaigns in minutes, not hours. Our streamlined workflow gets your emails out quickly.',
    color: 'text-orange-600 dark:text-orange-400'
  },
  {
    icon: Shield,
    title: 'Enterprise Security',
    description: 'Bank-level security with SOC 2 compliance, GDPR support, and advanced encryption to protect your data.',
    color: 'text-red-600 dark:text-red-400'
  },
  {
    icon: Palette,
    title: 'Beautiful Templates',
    description: 'Choose from hundreds of professionally designed templates or create your own with our drag-and-drop editor.',
    color: 'text-pink-600 dark:text-pink-400'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Work together with your team. Share templates, review campaigns, and manage permissions seamlessly.',
    color: 'text-indigo-600 dark:text-indigo-400'
  },
  {
    icon: Mail,
    title: 'Multi-Channel Delivery',
    description: 'Send via multiple providers including SendGrid, AWS SES, and SMTP for maximum deliverability.',
    color: 'text-cyan-600 dark:text-cyan-400'
  },
  {
    icon: TrendingUp,
    title: 'Performance Optimization',
    description: 'AI-powered optimization suggestions to improve open rates, click-through rates, and conversions.',
    color: 'text-emerald-600 dark:text-emerald-400'
  },
  {
    icon: Smartphone,
    title: 'Mobile-First Design',
    description: 'Responsive templates that look great on all devices. Mobile optimization built-in by default.',
    color: 'text-violet-600 dark:text-violet-400'
  }
]

export function FeaturesSection() {
  return (
    <section id="features" className="py-20 lg:py-32 bg-white dark:bg-slate-900">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl lg:text-5xl mb-6"
          >
            Everything you need to create
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              successful email campaigns
            </span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-lg text-slate-600 dark:text-slate-400"
          >
            From AI-powered content generation to advanced analytics, 
            we provide all the tools you need to create campaigns that convert.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group relative rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-lg dark:border-slate-700 dark:bg-slate-800"
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-700">
                <feature.icon className={`h-6 w-6 ${feature.color}`} />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-slate-900 dark:text-white">
                {feature.title}
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                {feature.description}
              </p>
              
              {/* Hover effect */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-600/5 to-purple-600/5 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <div className="rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 p-8 text-white">
            <h3 className="mb-4 text-2xl font-bold">
              Ready to transform your email marketing?
            </h3>
            <p className="mb-6 text-blue-100">
              Join thousands of marketers who are already creating better campaigns with AI.
            </p>
            <button className="rounded-lg bg-white px-6 py-3 font-semibold text-blue-600 transition-colors hover:bg-blue-50">
              Get Started Free
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
