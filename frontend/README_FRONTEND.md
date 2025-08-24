# Frontend - AI Email Campaign Writer

Next.js 14 frontend application for the AI Email Campaign Writer platform.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom components with design tokens
- **State Management**: React Context + Hooks
- **Testing**: Jest + React Testing Library
- **Linting**: ESLint + Prettier

## Prerequisites

- Node.js 18+ (see `.nvmrc`)
- pnpm 8+

## Quick Start

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

## Development

### Available Scripts

```bash
# Development
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server

# Testing
pnpm test         # Run tests
pnpm test:watch   # Run tests in watch mode
pnpm test:coverage # Run tests with coverage

# Code Quality
pnpm lint         # Run ESLint
pnpm lint:fix     # Fix ESLint issues
pnpm typecheck    # Run TypeScript type checking
pnpm format       # Format code with Prettier

# Utilities
pnpm clean        # Clean build artifacts
```

### Environment Variables

Copy `.env.example` to `.env.local` and configure:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key

# External Services
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication routes
│   ├── dashboard/         # Dashboard routes
│   ├── campaigns/         # Campaign management
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── ui/               # Base UI components
│   ├── forms/            # Form components
│   ├── layout/           # Layout components
│   └── sections/         # Page sections
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries
├── types/                # TypeScript type definitions
└── _INSTRUCTIONS.md      # Development instructions
```

## Component Guidelines

### Using Design Tokens

```typescript
import { colors, spacing } from '@ai-email-campaign/ui';

const MyComponent = () => (
  <div style={{ 
    backgroundColor: colors.primary[600],
    padding: spacing.md 
  }}>
    Content
  </div>
);
```

### Class Name Utilities

```typescript
import { cn } from '@ai-email-campaign/ui';

const MyComponent = ({ className, ...props }) => (
  <div className={cn(
    'base-classes',
    'conditional-classes',
    className
  )} {...props}>
    Content
  </div>
);
```

## Testing

### Running Tests

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage

# Run specific test file
pnpm test Button.test.tsx
```

### Test Structure

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

## Code Quality

### ESLint Configuration

The project uses a strict ESLint configuration with:
- TypeScript support
- React hooks rules
- Accessibility rules
- Import sorting

### Prettier Configuration

Code formatting is handled by Prettier with:
- 2-space indentation
- Single quotes
- Trailing commas
- 80 character line length

### TypeScript

Strict TypeScript configuration with:
- No implicit any
- Strict null checks
- No unused variables
- Exact function parameter types

## Performance

### Bundle Analysis

```bash
# Analyze bundle size
pnpm build
pnpm analyze
```

### Performance Budgets

- Initial bundle: < 200KB
- Total bundle: < 500KB
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s

## Deployment

### Vercel (Recommended)

1. Connect your repository to Vercel
2. Configure environment variables
3. Deploy automatically on push to main

### Other Platforms

```bash
# Build the application
pnpm build

# The output is in the .next directory
# Deploy the .next directory to your hosting platform
```

## Troubleshooting

### Common Issues

1. **Port 3000 already in use**
   ```bash
   # Kill the process using port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **TypeScript errors**
   ```bash
   # Clear TypeScript cache
   rm -rf .next
   pnpm typecheck
   ```

3. **Build failures**
   ```bash
   # Clean and rebuild
   pnpm clean
   pnpm install
   pnpm build
   ```

## Contributing

1. Follow the coding standards in `_INSTRUCTIONS.md`
2. Write tests for new components
3. Update documentation as needed
4. Ensure all tests pass before submitting PR
