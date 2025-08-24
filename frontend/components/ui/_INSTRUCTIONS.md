# UI Components Directory

This directory contains reusable base UI components that follow the design system.

## Components

### Button
- **File**: `Button.tsx`
- **Purpose**: Primary button component with variants
- **TODO**: Add loading states, icon support, and accessibility improvements

### Input
- **File**: `Input.tsx`
- **Purpose**: Form input component with validation states
- **TODO**: Add password toggle, character counter, and autocomplete

### Modal
- **File**: `Modal.tsx`
- **Purpose**: Modal dialog component
- **TODO**: Add animation, backdrop click handling, and focus management

### Card
- **File**: `Card.tsx`
- **Purpose**: Content container with consistent styling
- **TODO**: Add hover effects and loading skeletons

### Select
- **File**: `Select.tsx`
- **Purpose**: Dropdown selection component
- **TODO**: Add multi-select, search, and keyboard navigation

### Textarea
- **File**: `Textarea.tsx`
- **Purpose**: Multi-line text input
- **TODO**: Add auto-resize, character limit, and markdown preview

### Badge
- **File**: `Badge.tsx`
- **Purpose**: Status and label indicators
- **TODO**: Add clickable variants and color schemes

### Dropdown
- **File**: `Dropdown.tsx`
- **Purpose**: Context menu component
- **TODO**: Add sub-menus, keyboard navigation, and positioning

## Guidelines

1. **Use design tokens**: Import from `@ai-email-campaign/ui` package
2. **Accessibility**: Include ARIA labels and keyboard navigation
3. **TypeScript**: Use strict typing with proper interfaces
4. **Testing**: Write unit tests for all components
5. **Documentation**: Include usage examples and props documentation

## TODO: Implementation Tasks

- [ ] Add loading states to Button component
- [ ] Implement password toggle for Input component
- [ ] Add animation library for Modal transitions
- [ ] Create loading skeleton for Card component
- [ ] Add search functionality to Select component
- [ ] Implement auto-resize for Textarea
- [ ] Add clickable variants to Badge component
- [ ] Create sub-menu support for Dropdown
