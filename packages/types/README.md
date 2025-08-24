# @ai-email-campaign/types

Shared TypeScript types and interfaces for the AI Email Campaign Writer platform.

## Installation

```bash
pnpm add @ai-email-campaign/types
```

## Usage

```typescript
import { Campaign, User, CampaignStatus } from '@ai-email-campaign/types';

const campaign: Campaign = {
  id: 'campaign-123',
  userId: 'user-456',
  name: 'Welcome Campaign',
  subject: 'Welcome to our platform!',
  content: 'Hello {{firstName}}, welcome to our platform...',
  status: CampaignStatus.DRAFT,
  recipientCount: 1000,
  sentCount: 0,
  openedCount: 0,
  clickedCount: 0,
  createdAt: new Date(),
  updatedAt: new Date()
};
```

## Available Types

- **User**: User account information
- **Campaign**: Email campaign data
- **Recipient**: Campaign recipient information
- **Template**: Email template data
- **Analytics**: Campaign performance metrics
- **API Responses**: Standard API response formats
- **AI Service**: AI generation request/response types
- **Email Service**: Email sending types

## Development

```bash
# Build the package
pnpm build

# Watch for changes
pnpm dev

# Clean build artifacts
pnpm clean
```
