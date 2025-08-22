'use client';

import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  ChartBarIcon, 
  EnvelopeIcon,
  UsersIcon,
  CogIcon,
  ShieldCheckIcon,
  LightningBoltIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';

export function Features() {
  const features = [
    {
      icon: SparklesIcon,
      title: 'AI-Powered Content Generation',
      description: 'Generate compelling email content in seconds using advanced AI models. Get personalized, engaging copy that converts.',
      color: 'text-primary-600'
    },
    {
      icon: ChartBarIcon,
      title: 'Advanced Analytics & Insights',
      description: 'Track performance with detailed analytics, A/B testing, and real-time insights to optimize your campaigns.',
      color: 'text-secondary-600'
    },
    {
      icon: EnvelopeIcon,
      title: 'Professional Templates',
      description: 'Choose from hundreds of professionally designed templates or create custom ones that match your brand.',
      color: 'text-purple-600'
    },
    {
      icon: UsersIcon,
      title: 'Smart Audience Targeting',
      description: 'Segment your audience intelligently and deliver personalized content that resonates with each subscriber.',
      color: 'text-green-600'
    },
    {
      icon: LightningBoltIcon,
      title: 'Real-time Collaboration',
      description: 'Work together with your team in real-time. Share templates, review campaigns, and get instant feedback.',
      color: 'text-yellow-600'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Enterprise Security',
      description: 'Bank-level security with encryption, compliance, and privacy protection for your sensitive data.',
      color: 'text-red-600'
    }
  ];

  return (
    <section id="features" className="py-20 bg-gray-50 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4"
          >
            Everything You Need for
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-secondary-600">
              {" "}Successful Email Marketing
            </span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
            className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto"
          >
            From AI-powered content creation to advanced analytics, 
            we provide all the tools you need to create, send, and optimize your email campaigns.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group relative bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              
              <div className="relative">
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg bg-gray-100 dark:bg-gray-700 mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Additional Features */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-8">
            And So Much More...
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              'Multi-language Support',
              'Mobile Optimization',
              'API Integration',
              'White-label Solutions',
              'Advanced Segmentation',
              'Automated Workflows',
              'GDPR Compliance',
              '24/7 Support'
            ].map((feature, index) => (
              <motion.div
                key={feature}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                viewport={{ once: true }}
                className="flex items-center justify-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
              >
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  {feature}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
