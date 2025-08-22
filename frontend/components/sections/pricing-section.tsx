'use client'

import { motion } from 'framer-motion'
import { Check, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'

const plans = [
  {
    name: 'Free',
    price: '$0',
    period: 'forever',
    description: 'Perfect for getting started with email marketing',
    features: [
      '1,000 emails per month',
      'Basic AI content generation',
      '5 email templates',
      'Basic analytics',
      'Email support'
    ],
    popular: false,
    cta: 'Get Started Free',
    href: '/auth/register'
  },
  {
    name: 'Pro',
    price: '$29',
    period: 'per month',
    description: 'For growing businesses and marketing teams',
    features: [
      '50,000 emails per month',
      'Advanced AI content generation',
      'Unlimited templates',
      'Advanced analytics & A/B testing',
      'Priority support',
      'Team collaboration',
      'Custom branding',
      'API access'
    ],
    popular: true,
    cta: 'Start Pro Trial',
    href: '/auth/register?plan=pro'
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: 'per month',
    description: 'For large organizations with advanced needs',
    features: [
      'Unlimited emails',
      'Custom AI models',
      'White-label solution',
      'Advanced security & compliance',
      'Dedicated account manager',
      'Custom integrations',
      'SLA guarantees',
      'On-premise deployment'
    ],
    popular: false,
    cta: 'Contact Sales',
    href: '/contact'
  }
]

export function PricingSection() {
  return (
    <section id="pricing" className="py-20 lg:py-32 bg-slate-50 dark:bg-slate-800">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl lg:text-5xl mb-6"
          >
            Simple, transparent pricing
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              that grows with you
            </span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-lg text-slate-600 dark:text-slate-400"
          >
            Choose the plan that fits your needs. All plans include our core features.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className={`relative rounded-2xl border bg-white p-8 shadow-sm transition-all duration-300 hover:shadow-lg dark:bg-slate-900 dark:border-slate-700 ${
                plan.popular 
                  ? 'border-blue-500 ring-2 ring-blue-500/20 scale-105' 
                  : 'border-slate-200'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <div className="flex items-center rounded-full bg-blue-600 px-4 py-1 text-sm font-medium text-white">
                    <Star className="mr-1 h-4 w-4" />
                    Most Popular
                  </div>
                </div>
              )}

              <div className="text-center">
                <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                  {plan.name}
                </h3>
                <div className="mb-4">
                  <span className="text-4xl font-bold text-slate-900 dark:text-white">
                    {plan.price}
                  </span>
                  {plan.period !== 'forever' && (
                    <span className="text-slate-600 dark:text-slate-400">
                      /{plan.period}
                    </span>
                  )}
                </div>
                <p className="text-slate-600 dark:text-slate-400 mb-8">
                  {plan.description}
                </p>
              </div>

              <ul className="mb-8 space-y-4">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start">
                    <Check className="mr-3 h-5 w-5 flex-shrink-0 text-green-500 mt-0.5" />
                    <span className="text-slate-700 dark:text-slate-300">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              <Button 
                className={`w-full ${
                  plan.popular 
                    ? 'bg-blue-600 hover:bg-blue-700' 
                    : ''
                }`}
                variant={plan.popular ? 'default' : 'outline'}
                size="lg"
                asChild
              >
                <a href={plan.href}>
                  {plan.cta}
                </a>
              </Button>
            </motion.div>
          ))}
        </div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <p className="text-slate-600 dark:text-slate-400 mb-4">
            Questions about pricing? 
          </p>
          <Button variant="link" className="text-blue-600 hover:text-blue-700">
            View our FAQ
          </Button>
        </motion.div>
      </div>
    </section>
  )
}
