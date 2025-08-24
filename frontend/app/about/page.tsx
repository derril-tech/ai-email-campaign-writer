'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600" />
            <span className="text-xl font-bold">AI Email Campaign Writer</span>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/" className="text-sm font-medium hover:text-primary">
              Home
            </Link>
            <Link href="/about" className="text-sm font-medium text-primary">
              About
            </Link>
            <Link href="#features" className="text-sm font-medium hover:text-primary">
              Features
            </Link>
            <Link href="#pricing" className="text-sm font-medium hover:text-primary">
              Pricing
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button variant="ghost" size="sm">
                Sign In
              </Button>
            </Link>
            <Link href="/auth/register">
              <Button size="sm">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="container py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">About AI Email Campaign Writer</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            We're revolutionizing email marketing by combining the power of artificial intelligence 
            with intuitive design to help businesses create engaging, personalized campaigns that convert.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-16">
          <div>
            <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
            <p className="text-lg text-muted-foreground mb-6">
              To democratize email marketing by making it accessible, intelligent, and effective 
              for businesses of all sizes. We believe every company deserves the tools to create 
              compelling email campaigns that drive real results.
            </p>
            <p className="text-lg text-muted-foreground">
              Our AI-powered platform analyzes your audience, suggests optimal content, and 
              helps you deliver the right message at the right time to maximize engagement and conversions.
            </p>
          </div>
          <div className="bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-8">
            <h3 className="text-2xl font-bold mb-4">Why Choose Us?</h3>
            <ul className="space-y-4">
              <li className="flex items-start space-x-3">
                <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="font-semibold">AI-Powered Content Generation</h4>
                  <p className="text-sm text-muted-foreground">Create compelling email content in seconds</p>
                </div>
              </li>
              <li className="flex items-start space-x-3">
                <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="font-semibold">Advanced Analytics</h4>
                  <p className="text-sm text-muted-foreground">Track performance and optimize campaigns</p>
                </div>
              </li>
              <li className="flex items-start space-x-3">
                <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="font-semibold">Personalization Engine</h4>
                  <p className="text-sm text-muted-foreground">Deliver targeted messages to your audience</p>
                </div>
              </li>
              <li className="flex items-start space-x-3">
                <div className="h-6 w-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold mt-0.5">
                  ✓
                </div>
                <div>
                  <h4 className="font-semibold">Easy-to-Use Interface</h4>
                  <p className="text-sm text-muted-foreground">No technical expertise required</p>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Team Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">Our Team</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card>
              <CardHeader className="text-center">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold">
                  JD
                </div>
                <CardTitle>John Doe</CardTitle>
                <CardDescription>CEO & Founder</CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-sm text-muted-foreground">
                  Former marketing executive with 15+ years of experience in email marketing and AI.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="text-center">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-green-500 to-blue-500 mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold">
                  JS
                </div>
                <CardTitle>Jane Smith</CardTitle>
                <CardDescription>CTO</CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-sm text-muted-foreground">
                  AI/ML expert with a passion for making technology accessible to everyone.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="text-center">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold">
                  MJ
                </div>
                <CardTitle>Mike Johnson</CardTitle>
                <CardDescription>Head of Product</CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-sm text-muted-foreground">
                  Product leader focused on creating intuitive user experiences that drive results.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Stats Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-center mb-12">Our Impact</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">10K+</div>
              <p className="text-muted-foreground">Happy Customers</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">50M+</div>
              <p className="text-muted-foreground">Emails Sent</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">85%</div>
              <p className="text-muted-foreground">Average Open Rate</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">24/7</div>
              <p className="text-muted-foreground">Customer Support</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Join thousands of businesses already using AI Email Campaign Writer to boost their email marketing.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/register">
              <Button size="lg">Start Free Trial</Button>
            </Link>
            <Link href="/#pricing">
              <Button variant="outline" size="lg">View Pricing</Button>
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-background mt-16">
        <div className="container py-12">
          <div className="text-center">
            <p className="text-muted-foreground">
              &copy; 2024 AI Email Campaign Writer. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
