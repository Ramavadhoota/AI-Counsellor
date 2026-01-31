# 🚀 AI Study Abroad Counsellor - Frontend

A modern, AI-powered study abroad counselling platform built with Next.js 14, TypeScript, and Tailwind CSS.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Development](#development)
- [Deployment](#deployment)
- [Documentation](#documentation)

---

## ✨ Features

### Core Features
- 🔐 **Authentication**: Secure JWT-based login/signup
- 📝 **Onboarding Wizard**: Multi-step user profile creation
- 🎯 **Smart Dashboard**: Personalized study abroad journey tracking
- 🤖 **AI Counsellor**: Interactive chat for guidance
- 🎓 **University Explorer**: Browse and shortlist universities
- 📊 **Profile Strength**: Track application readiness
- 🗺️ **Journey Stages**: Visual progress through stages
- 👤 **Profile Management**: Complete user profile control

### UI/UX
- 🌑 **Dark Theme**: Modern teal (#20B2AA) accent
- 📱 **Responsive Design**: Mobile-first approach
- ⚡ **Fast Performance**: Optimized Next.js build
- ♿ **Accessible**: ARIA labels and keyboard navigation
- 🎨 **Consistent Design**: Custom component library

---

## 🛠️ Tech Stack

### Framework & Language
- [Next.js 14](https://nextjs.org/) - React framework with App Router
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [React 18](https://react.dev/) - UI library

### Styling
- [Tailwind CSS 3](https://tailwindcss.com/) - Utility-first CSS
- Custom dark theme configuration
- Responsive breakpoints

### State & Data
- [Zustand](https://zustand-demo.pmnd.rs/) - State management (optional)
- [Axios](https://axios-http.com/) - HTTP client
- Local Storage - Token persistence

### UI Components
- Custom component library (Button, Card, Input, etc.)
- [Lucide React](https://lucide.dev/) - Icon library

### Development Tools
- ESLint - Code linting
- Prettier - Code formatting (recommended)
- TypeScript - Type checking

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-counsellor.git
   cd ai-counsellor/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local` with your configuration:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_SITE_URL=http://localhost:3000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   ├── login/              # Login page
│   │   ├── signup/             # Signup page
│   │   ├── onboarding/         # Onboarding wizard
│   │   ├── dashboard/          # Main dashboard
│   │   ├── counsellor/         # AI chat
│   │   ├── universities/       # University listing
│   │   └── profile/            # User profile
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # Reusable UI components
│   │   ├── auth/               # Auth components
│   │   ├── onboarding/         # Onboarding forms
│   │   ├── dashboard/          # Dashboard components
│   │   ├── counsellor/         # Chat components
│   │   └── universities/       # University components
│   │
│   ├── lib/                    # Utilities and helpers
│   │   ├── api.ts              # API client (Axios)
│   │   ├── auth.ts             # Auth utilities
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Helper functions
│   │
│   └── middleware.ts           # Route protection
│
├── public/                     # Static files
│   ├── logo.svg
│   └── images/
│
├── docs/                       # Documentation
│   ├── API.md                  # API documentation
│   ├── SETUP.md                # Setup guide
│   ├── ARCHITECTURE.md         # Architecture docs
│   └── DEPLOYMENT.md           # Deployment guide
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── .env.local.example
```

---

## 🔧 Environment Setup

### Required Variables

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Site Configuration
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Optional: NextAuth.js (if using)
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

### Generate Secrets

```bash
# Generate NEXTAUTH_SECRET
openssl rand -base64 32
```

---

## 💻 Development

### Available Scripts

```bash
# Development server (with hot reload)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint

# Format code (if Prettier configured)
npm run format
```

### Development Workflow

1. **Start backend API** (see backend README)
2. **Start frontend dev server**: `npm run dev`
3. **Make changes** - hot reload will update automatically
4. **Test features** in browser
5. **Check types**: `npm run type-check`
6. **Lint code**: `npm run lint`

### Code Style

- Use TypeScript for all components
- Follow component naming conventions (PascalCase)
- Use Tailwind classes for styling
- Keep components small and focused
- Add TypeScript interfaces for props

---

## 🚀 Deployment

### Vercel (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Configure environment variables** in Vercel dashboard

### Other Platforms

- **Netlify**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Docker**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **AWS/Railway**: See [DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [API Documentation](docs/API.md) - Frontend API integration
- [Architecture](docs/ARCHITECTURE.md) - System architecture
- [Deployment](docs/DEPLOYMENT.md) - Deployment guide

---

## 🔐 Authentication Flow

1. User signs up → Backend creates account
2. User logs in → Backend returns JWT token
3. Token stored in localStorage
4. Middleware checks token on protected routes
5. API client injects token in requests
6. On 401 error → Redirect to login

---

## 🎨 Theming

### Color Palette

```typescript
// Tailwind config
colors: {
  background: '#0F172A',    // Dark blue-gray
  surface: '#1E293B',       // Lighter surface
  primary: '#20B2AA',       // Teal accent
  secondary: '#64748B',     // Muted gray
  success: '#10B981',       // Green
  warning: '#F59E0B',       // Amber
  danger: '#EF4444',        // Red
}
```

### Typography

- **Font**: System fonts (Inter-style)
- **Headings**: Semibold (600)
- **Body**: Regular (400)
- **Scale**: 14px base, responsive scaling

---

## 🧪 Testing (Future)

```bash
# Unit tests (Jest + React Testing Library)
npm run test

# E2E tests (Playwright/Cypress)
npm run test:e2e
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Team

- **Your Name** - Full Stack Developer

---

## 🙏 Acknowledgments

- Next.js team for the amazing framework
- Tailwind CSS for utility-first styling
- Vercel for hosting platform
- FastAPI team for backend framework

---

## 📞 Support

- **Documentation**: Check the [docs](docs/) folder
- **Issues**: Open an issue on GitHub
- **Email**: support@yourdomain.com

---

**Built with ❤️ for students pursuing their dreams abroad**
