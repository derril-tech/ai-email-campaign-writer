# @ai-email-campaign/ui

Shared UI components and design tokens for the AI Email Campaign Writer platform.

## Installation

```bash
pnpm add @ai-email-campaign/ui
```

## Usage

### Design Tokens

```typescript
import { colors, spacing, typography } from '@ai-email-campaign/ui';

// Use semantic color tokens instead of hard-coded values
const buttonStyle = {
  backgroundColor: colors.primary[600],
  padding: spacing.md,
  fontSize: typography.fontSize.base,
};
```

### Utility Functions

```typescript
import { cn } from '@ai-email-campaign/ui';

// Combine class names with Tailwind CSS merging
const className = cn(
  'bg-blue-500',
  'hover:bg-blue-600',
  'text-white',
  'px-4 py-2',
  'rounded-lg'
);
```

## Design System

### Colors

The design system uses a semantic color palette:

- **Primary**: Blue shades for main actions and branding
- **Secondary**: Gray shades for secondary elements
- **Success**: Green shades for positive states
- **Warning**: Yellow/Orange shades for caution states
- **Error**: Red shades for error states
- **Neutral**: Gray shades for text and borders

### Spacing

Consistent spacing scale:
- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px
- `3xl`: 64px

### Typography

Font families:
- **Sans**: Inter (primary)
- **Mono**: JetBrains Mono (for code)

Font sizes follow a consistent scale from `xs` (12px) to `6xl` (60px).

## Development

```bash
# Build the package
pnpm build

# Watch for changes
pnpm dev

# Clean build artifacts
pnpm clean
```

## Best Practices

1. **Use design tokens**: Always use the provided design tokens instead of hard-coded values
2. **Semantic colors**: Use semantic color tokens for better theming support
3. **Consistent spacing**: Use the spacing scale for consistent layouts
4. **Class merging**: Use the `cn` utility for combining Tailwind classes
5. **Accessibility**: Ensure proper contrast ratios and focus states
