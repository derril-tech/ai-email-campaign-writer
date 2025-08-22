# 🎨 Frontend Development Instructions

## 📁 **Frontend Structure Overview**

This directory contains the Next.js 14 frontend application for PulseQuill - AI Email Campaign Writer.

### **Key Directories**
- `app/` - Next.js App Router pages and layouts
- `components/` - Reusable React components
- `hooks/` - Custom React hooks
- `lib/` - Utility functions and API clients
- `types/` - TypeScript type definitions

## 🎯 **Development Guidelines**

### **Component Structure**
- Use functional components with TypeScript
- Implement proper prop interfaces (IComponentNameProps)
- Follow atomic design principles
- Ensure WCAG AA accessibility compliance

### **State Management**
- Use Zustand for global state
- React Query for server state
- Local state with useState/useReducer
- Context for theme/auth providers

### **Styling**
- Tailwind CSS for styling
- Design tokens from design system
- Responsive design (320/768/1024/1440 breakpoints)
- Dark/light theme support

### **Performance**
- Code splitting with dynamic imports
- Image optimization with Next.js Image
- Bundle size optimization
- Core Web Vitals compliance

## 🚀 **TODO: Implementation Tasks**

### **High Priority**
- [ ] Complete authentication flow (login/register/logout)
- [ ] Implement campaign creation wizard
- [ ] Build email editor with drag-and-drop
- [ ] Create real-time analytics dashboard
- [ ] Add A/B testing interface

### **Medium Priority**
- [ ] Implement audience segmentation tools
- [ ] Build template management system
- [ ] Add campaign scheduling interface
- [ ] Create user settings and preferences
- [ ] Implement notification system

### **Low Priority**
- [ ] Add advanced reporting features
- [ ] Implement team collaboration tools
- [ ] Build white-label customization
- [ ] Add multi-language support
- [ ] Create mobile-responsive components

## 🔧 **Technical Requirements**

### **Dependencies**
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Framer Motion for animations
- Zustand for state management
- React Query for data fetching

### **Code Quality**
- ESLint + Prettier configuration
- TypeScript strict mode
- Jest + Testing Library for testing
- Accessibility testing with axe-core

### **Performance Targets**
- Lighthouse score ≥ 90
- Initial bundle < 500KB
- Time to Interactive < 3s
- Core Web Vitals compliance

## 📝 **Coding Standards**

### **File Naming**
- Components: PascalCase (e.g., `CampaignCard.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Pages: kebab-case (e.g., `campaign-details.tsx`)

### **Component Structure**
```typescript
interface IComponentProps {
  // Props definition
}

const Component: React.FC<IComponentProps> = ({ prop1, prop2 }) => {
  // Component logic
  return (
    // JSX
  );
};

export { Component };
```

### **State Management Pattern**
```typescript
// Zustand store
interface IStore {
  campaigns: Campaign[];
  loading: boolean;
  setCampaigns: (campaigns: Campaign[]) => void;
}

const useStore = create<IStore>((set) => ({
  campaigns: [],
  loading: false,
  setCampaigns: (campaigns) => set({ campaigns }),
}));
```

## 🎨 **Design System**

### **Colors**
- Primary: #3B82F6 (Blue)
- Secondary: #8B5CF6 (Purple)
- Success: #10B981 (Green)
- Warning: #F59E0B (Orange)
- Error: #EF4444 (Red)

### **Typography**
- Font: Inter
- Base size: 14px
- Scale: 1.25 modular scale

### **Spacing**
- Grid: 4px increments
- Common: 4, 8, 16, 24, 32, 48, 64

## 🔒 **Security Considerations**

### **Authentication**
- JWT token management
- Secure token storage
- Auto-refresh implementation
- Logout cleanup

### **Data Protection**
- Input validation
- XSS prevention
- CSRF protection
- Secure API calls

## 📊 **Testing Strategy**

### **Unit Tests**
- Component rendering
- User interactions
- State changes
- Utility functions

### **Integration Tests**
- API integration
- Form submissions
- Navigation flows
- Error handling

### **E2E Tests**
- User journeys
- Critical paths
- Cross-browser testing
- Performance testing

## 🚀 **Deployment**

### **Build Process**
- TypeScript compilation
- Bundle optimization
- Static asset optimization
- Environment variable injection

### **Vercel Deployment**
- Automatic deployment on main branch
- Preview deployments for PRs
- Environment variable configuration
- Performance monitoring

---

**Last Updated**: December 2024
**Version**: 1.0.0
