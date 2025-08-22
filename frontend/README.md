# AI Email Campaign Writer - Frontend

A modern, responsive Next.js 14 frontend for the AI Email Campaign Writer application. Built with TypeScript, Tailwind CSS, and Framer Motion for a premium user experience.

## 🚀 Features

- **Next.js 14** with App Router for optimal performance
- **TypeScript** for type safety and better developer experience
- **Tailwind CSS** for utility-first styling
- **Framer Motion** for smooth animations and transitions
- **Dark/Light Mode** support with system preference detection
- **Responsive Design** that works on all devices
- **Real-time Updates** via WebSocket connections
- **JWT Authentication** with secure token management
- **React Query** for efficient data fetching and caching
- **Form Handling** with React Hook Form
- **State Management** with Zustand
- **Accessibility** compliant with WCAG 2.1 AA standards

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **State Management**: Zustand
- **Data Fetching**: React Query + Axios
- **Forms**: React Hook Form
- **Icons**: Heroicons
- **Real-time**: Socket.io Client
- **Testing**: Jest + React Testing Library

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-email-campaign-writer/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   ```
   
   Update the `.env.local` file with your configuration:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   NEXT_PUBLIC_WS_URL=ws://localhost:8000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── layout/           # Layout components
│   ├── sections/         # Page sections
│   └── providers/        # Context providers
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries
├── types/                # TypeScript type definitions
├── styles/               # Additional styles
└── public/               # Static assets
```

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (#3B82F6 to #2563EB)
- **Secondary**: Green gradient (#22C55E to #16A34A)
- **Gray**: Neutral grays for text and backgrounds
- **Dark Mode**: Full dark theme support

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Monospace**: JetBrains Mono for code

### Components
- **Buttons**: Primary, secondary, and ghost variants
- **Cards**: With hover effects and shadows
- **Forms**: Styled inputs with validation
- **Navigation**: Responsive header with mobile menu

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage

## 🌐 API Integration

The frontend integrates with the FastAPI backend through a comprehensive API client:

- **Authentication**: JWT-based auth with refresh tokens
- **Campaigns**: CRUD operations for email campaigns
- **Templates**: Template management and customization
- **AI Generation**: Content generation and analysis
- **Analytics**: Campaign performance tracking
- **File Upload**: Image and document uploads
- **Real-time**: WebSocket connections for live updates

## 🔐 Authentication

The app uses JWT authentication with the following features:

- **Login/Register**: User account creation and login
- **Token Management**: Automatic token refresh
- **Protected Routes**: Route protection based on auth status
- **Profile Management**: User profile updates
- **Password Reset**: Forgot password functionality

## 📱 Responsive Design

The application is fully responsive with:

- **Mobile-first** approach
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Touch-friendly** interfaces
- **Optimized** for all screen sizes

## ♿ Accessibility

Built with accessibility in mind:

- **WCAG 2.1 AA** compliance
- **Keyboard navigation** support
- **Screen reader** friendly
- **High contrast** mode support
- **Focus management** for better UX

## 🧪 Testing

The project includes comprehensive testing:

- **Unit Tests**: Component and utility testing
- **Integration Tests**: API integration testing
- **E2E Tests**: End-to-end user flow testing
- **Coverage**: >90% test coverage target

## 🚀 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Other Platforms
- **Netlify**: Compatible with Next.js
- **AWS Amplify**: Full-stack deployment
- **Docker**: Containerized deployment

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL | `ws://localhost:8000` |
| `NEXTAUTH_URL` | NextAuth.js URL | `http://localhost:3000` |
| `NEXTAUTH_SECRET` | NextAuth.js secret | Required |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- 📧 Email: support@aiemailwriter.com
- 💬 Discord: [Join our community](https://discord.gg/aiemailwriter)
- 📖 Documentation: [docs.aiemailwriter.com](https://docs.aiemailwriter.com)
- 🐛 Issues: [GitHub Issues](https://github.com/aiemailwriter/frontend/issues)

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) for the amazing framework
- [Tailwind CSS](https://tailwindcss.com/) for the utility-first CSS
- [Framer Motion](https://www.framer.com/motion/) for animations
- [Heroicons](https://heroicons.com/) for beautiful icons
- [Vercel](https://vercel.com/) for hosting and deployment
