'use client'

import { motion } from 'framer-motion'
import { Star, Quote } from 'lucide-react'

const testimonials = [
  {
    name: 'Sarah Johnson',
    role: 'Marketing Director',
    company: 'TechFlow Inc.',
    avatar: '/avatars/sarah.jpg',
    content: 'AI Email Campaign Writer has transformed our email marketing. We\'ve seen a 40% increase in open rates and 25% boost in conversions. The AI content generation saves us hours every week.',
    rating: 5
  },
  {
    name: 'Michael Chen',
    role: 'Founder & CEO',
    company: 'StartupXYZ',
    avatar: '/avatars/michael.jpg',
    content: 'As a small team, we needed a solution that could compete with enterprise tools. This platform delivers exactly that - powerful AI features with an intuitive interface.',
    rating: 5
  },
  {
    name: 'Emily Rodriguez',
    role: 'Digital Marketing Manager',
    company: 'E-commerce Plus',
    avatar: '/avatars/emily.jpg',
    content: 'The audience targeting and personalization features are game-changing. Our customers love the relevant content, and our ROI has never been better.',
    rating: 5
  },
  {
    name: 'David Thompson',
    role: 'VP of Marketing',
    company: 'GrowthCorp',
    avatar: '/avatars/david.jpg',
    content: 'We\'ve tried many email marketing platforms, but none compare to the AI capabilities here. The content suggestions are spot-on and the analytics are incredibly detailed.',
    rating: 5
  },
  {
    name: 'Lisa Wang',
    role: 'Marketing Specialist',
    company: 'InnovateLab',
    avatar: '/avatars/lisa.jpg',
    content: 'The template library is extensive and the drag-and-drop editor is so easy to use. Plus, the AI helps us create compelling content that actually converts.',
    rating: 5
  },
  {
    name: 'James Wilson',
    role: 'Head of Growth',
    company: 'ScaleUp Solutions',
    avatar: '/avatars/james.jpg',
    content: 'This platform has been instrumental in our growth. The automation features and AI optimization have helped us scale our email marketing efforts efficiently.',
    rating: 5
  }
]

export function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-20 lg:py-32 bg-white dark:bg-slate-900">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-4xl lg:text-5xl mb-6"
          >
            Loved by marketers worldwide
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-lg text-slate-600 dark:text-slate-400"
          >
            See what our customers are saying about their experience with AI Email Campaign Writer.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="relative rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-lg dark:bg-slate-800 dark:border-slate-700"
            >
              {/* Quote icon */}
              <div className="absolute -top-3 left-6">
                <div className="rounded-full bg-blue-600 p-2">
                  <Quote className="h-4 w-4 text-white" />
                </div>
              </div>

              {/* Rating */}
              <div className="mb-4 flex items-center">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>

              {/* Content */}
              <blockquote className="mb-6 text-slate-700 dark:text-slate-300">
                "{testimonial.content}"
              </blockquote>

              {/* Author */}
              <div className="flex items-center">
                <div className="mr-4 h-12 w-12 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
                  <span className="text-sm font-semibold text-white">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div>
                  <div className="font-semibold text-slate-900 dark:text-white">
                    {testimonial.name}
                  </div>
                  <div className="text-sm text-slate-600 dark:text-slate-400">
                    {testimonial.role} at {testimonial.company}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          viewport={{ once: true }}
          className="mt-16 grid grid-cols-2 gap-8 border-t border-slate-200 pt-8 dark:border-slate-700 sm:grid-cols-4"
        >
          <div className="text-center">
            <div className="text-3xl font-bold text-slate-900 dark:text-white">4.9/5</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Average Rating</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-slate-900 dark:text-white">10K+</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Happy Customers</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-slate-900 dark:text-white">98%</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Satisfaction Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-slate-900 dark:text-white">24/7</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">Support</div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
