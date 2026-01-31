# 📚 Frontend - Documentation Files (Part 2)

## docs/ARCHITECTURE.md

```markdown
# System Architecture

## Overview

The AI Study Abroad Counsellor frontend is built with **Next.js 14**, using the **App Router** architecture with **TypeScript** and **Tailwind CSS**.

---

## Technology Stack

### Core Framework
- **Next.js 14.2.0**: React framework with App Router
- **React 18**: UI library
- **TypeScript 5**: Type-safe development

### Styling
- **Tailwind CSS 3**: Utility-first CSS framework
- **Custom Dark Theme**: Teal (#20B2AA) primary color
- **Responsive Design**: Mobile-first approach

### State Management
- **Zustand**: Lightweight state management
- **React Context**: For theme and auth state
- **Local Storage**: Token persistence

### HTTP Client
- **Axios**: Promise-based HTTP client
- **Interceptors**: Auto token injection
- **Error handling**: Centralized error management

### UI Components
- **Custom Components**: Button, Card, Input, etc.
- **Lucide React**: Icon library
- **Modular Design**: Reusable component architecture

---

## Architecture Patterns

### 1. App Router Structure

```
src/app/
├── layout.tsx          # Root layout (wraps all pages)
├── page.tsx            # Landing page (/)
├── login/
│   └── page.tsx        # Login page (/login)
├── signup/
│   └── page.tsx        # Signup page (/signup)
├── onboarding/
│   └── page.tsx        # Onboarding wizard (/onboarding)
├── dashboard/
│   └── page.tsx        # Main dashboard (/dashboard)
├── counsellor/
│   └── page.tsx        # AI chat (/counsellor)
├── universities/
│   ├── page.tsx        # Universities list
│   └── [id]/
│       └── page.tsx    # University details (dynamic)
└── profile/
    └── page.tsx        # User profile
```

**Benefits:**
- File-system routing
- Nested layouts
- Server and Client Components
- Built-in loading/error states

---

### 2. Component Architecture

```
src/components/
├── ui/                 # Atomic UI components
│   ├── Button.tsx      # Reusable button
│   ├── Card.tsx        # Card container
│   ├── Input.tsx       # Form input
│   ├── Badge.tsx       # Status badge
│   ├── Progress.tsx    # Progress bar
│   ├── Select.tsx      # Dropdown select
│   ├── Textarea.tsx    # Text area
│   └── Modal.tsx       # Modal dialog
│
├── auth/               # Auth-specific components
│   ├── LoginForm.tsx
│   ├── SignupForm.tsx
│   └── ProtectedRoute.tsx
│
├── onboarding/         # Onboarding wizard
│   ├── OnboardingWizard.tsx
│   ├── AcademicForm.tsx
│   ├── GoalsForm.tsx
│   ├── BudgetForm.tsx
│   └── ExamsForm.tsx
│
├── dashboard/          # Dashboard components
│   ├── StageIndicator.tsx
│   ├── ProfileStrength.tsx
│   ├── StatCard.tsx
│   └── TodoList.tsx
│
├── counsellor/         # AI chat components
│   ├── ChatInterface.tsx
│   └── MessageBubble.tsx
│
└── universities/       # University components
    ├── UniversityCard.tsx
    ├── UniversityGrid.tsx
    ├── FilterSidebar.tsx
    └── LockModal.tsx
```

**Design Principles:**
- **Atomic Design**: UI → Components → Pages
- **Single Responsibility**: Each component has one job
- **Props Interface**: Typed props with TypeScript
- **Composition**: Build complex UIs from simple components

---

### 3. State Management Strategy

#### Local Component State
```typescript
// React useState for component-specific state
const [loading, setLoading] = useState(false);
```

#### Global State (Zustand)
```typescript
// src/lib/store.ts
interface AppState {
  user: User | null;
  setUser: (user: User) => void;
  universities: University[];
  setUniversities: (universities: University[]) => void;
}

export const useStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  universities: [],
  setUniversities: (universities) => set({ universities }),
}));
```

#### Persistence
```typescript
// Token in localStorage
localStorage.setItem('token', token);
```

---

### 4. API Integration Layer

```typescript
// src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (auto-inject token)
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor (handle errors)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      removeToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**Benefits:**
- Centralized configuration
- Auto token injection
- Global error handling
- Type-safe responses

---

### 5. Authentication Flow

```
┌─────────────┐
│   Signup    │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       v              v
┌─────────────┐  ┌─────────────┐
│    Login    │  │ Onboarding  │
└──────┬──────┘  └──────┬──────┘
       │                │
       └────────┬───────┘
                │
                v
         ┌─────────────┐
         │  Dashboard  │
         └──────┬──────┘
                │
       ┌────────┼────────┐
       │        │        │
       v        v        v
 ┌──────┐  ┌──────┐  ┌──────┐
 │ Chat │  │ Unis │  │Profile│
 └──────┘  └──────┘  └──────┘
```

**Implementation:**
1. User signs up → receives JWT token
2. Token stored in localStorage
3. Middleware checks token on protected routes
4. API client injects token in requests
5. Backend validates token
6. On 401, redirect to login

---

### 6. Routing & Middleware

```typescript
// src/middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const isProtectedRoute = protectedRoutes.some((route) =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Redirect to login if accessing protected route without token
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Redirect to dashboard if accessing auth pages with token
  if ((pathname === '/login' || pathname === '/signup') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}
```

**Protected Routes:**
- `/dashboard`
- `/profile`
- `/onboarding`
- `/counsellor`
- `/universities`

---

### 7. Data Flow

```
┌──────────────┐
│  User Action │ (Click button)
└──────┬───────┘
       │
       v
┌──────────────┐
│  Component   │ (Event handler)
└──────┬───────┘
       │
       v
┌──────────────┐
│  API Client  │ (axios request)
└──────┬───────┘
       │
       v
┌──────────────┐
│   Backend    │ (FastAPI)
└──────┬───────┘
       │
       v
┌──────────────┐
│   Response   │ (JSON data)
└──────┬───────┘
       │
       v
┌──────────────┐
│     State    │ (useState/Zustand)
└──────┬───────┘
       │
       v
┌──────────────┐
│   Re-render  │ (React updates UI)
└──────────────┘
```

---

### 8. Error Handling Strategy

#### Component Level
```typescript
try {
  const data = await fetchData();
  setData(data);
} catch (error) {
  setError('Failed to load data');
}
```

#### Global Error Boundary
```typescript
// src/app/error.tsx
export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

#### API Error Interceptor
```typescript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);
```

---

### 9. Performance Optimizations

#### Code Splitting
```typescript
// Dynamic imports for heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />,
});
```

#### Image Optimization
```typescript
import Image from 'next/image';

<Image
  src="/logo.svg"
  alt="Logo"
  width={200}
  height={200}
  priority
/>
```

#### Memoization
```typescript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

---

### 10. Styling Architecture

#### Tailwind Utility Classes
```typescript
<div className="bg-background text-white p-4 rounded-lg">
  <h1 className="text-2xl font-bold mb-4">Title</h1>
</div>
```

#### Custom Theme Configuration
```typescript
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      background: '#0F172A',
      surface: '#1E293B',
      primary: '#20B2AA',
      // ...
    },
  },
}
```

#### Global Styles
```css
/* src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-white;
  }
}
```

---

## Security Considerations

### 1. Authentication
- JWT tokens stored in localStorage
- Token validated on every protected route
- Auto-redirect on 401 responses

### 2. XSS Prevention
- React auto-escapes content
- Avoid `dangerouslySetInnerHTML`
- Sanitize user inputs

### 3. CSRF Protection
- SameSite cookies
- Token-based auth
- Backend CORS configuration

### 4. Environment Variables
- Sensitive data in `.env.local`
- Never commit `.env.local`
- Use `NEXT_PUBLIC_` prefix for client-side vars

---

## Deployment Architecture

```
┌─────────────────┐
│   Vercel CDN    │ (Static assets)
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Next.js Server │ (SSR/API routes)
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Backend API    │ (FastAPI on Railway/Render)
└────────┬────────┘
         │
         v
┌─────────────────┐
│   PostgreSQL    │ (Database)
└─────────────────┘
```

---

## Development vs Production

### Development
- Hot reload enabled
- Source maps available
- Debug mode on
- Local API (localhost:8000)

### Production
- Optimized bundles
- Minified code
- No source maps
- Production API (https://api.yourdomain.com)

---

## Scalability Considerations

### 1. Code Organization
- Modular components
- Separation of concerns
- Reusable utilities

### 2. State Management
- Zustand for global state
- React Query for server state (future)

### 3. API Caching
- Next.js built-in caching
- SWR/React Query (future enhancement)

### 4. Bundle Size
- Tree shaking
- Dynamic imports
- Lazy loading

---

## Future Enhancements

1. **React Query**: Better server state management
2. **WebSockets**: Real-time AI chat
3. **PWA**: Progressive Web App features
4. **E2E Testing**: Playwright/Cypress
5. **Analytics**: Google Analytics/PostHog
6. **Monitoring**: Sentry error tracking
7. **A/B Testing**: Feature flags
8. **Internationalization**: Multi-language support

---

## Conclusion

The architecture is designed for:
- ✅ **Developer Experience**: TypeScript, modern tooling
- ✅ **Performance**: Optimized bundles, lazy loading
- ✅ **Scalability**: Modular structure, clean separation
- ✅ **Maintainability**: Clear patterns, documented code
- ✅ **Security**: Auth flow, input validation, XSS prevention
```

---

## docs/DEPLOYMENT.md

```markdown
# Deployment Guide

## Overview

This guide covers deploying the AI Study Abroad Counsellor frontend to production.

---

## Deployment Options

### 1. Vercel (Recommended)

**Why Vercel?**
- ✅ Built for Next.js
- ✅ Zero configuration
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Preview deployments
- ✅ Free tier available

---

### Vercel Deployment Steps

#### 1. Install Vercel CLI

```bash
npm install -g vercel
```

#### 2. Login to Vercel

```bash
vercel login
```

#### 3. Deploy

```bash
# From frontend directory
cd frontend
vercel
```

Follow the prompts:
- **Project name**: ai-counsellor-frontend
- **Framework**: Next.js
- **Root directory**: `./`
- **Build command**: `npm run build`
- **Output directory**: `.next`

#### 4. Configure Environment Variables

In Vercel Dashboard:

```
NEXT_PUBLIC_API_URL=https://your-backend-api.com
NEXT_PUBLIC_SITE_URL=https://your-app.vercel.app
NEXTAUTH_SECRET=your-production-secret
NEXTAUTH_URL=https://your-app.vercel.app
```

#### 5. Deploy to Production

```bash
vercel --prod
```

---

### 2. Netlify

#### Setup

```bash
npm install -g netlify-cli
netlify login
netlify init
```

#### netlify.toml

```toml
[build]
  command = "npm run build"
  publish = ".next"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Deploy

```bash
netlify deploy --prod
```

---

### 3. Docker Deployment

#### Dockerfile

```dockerfile
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
      - NEXT_PUBLIC_SITE_URL=https://yourdomain.com
    restart: unless-stopped
```

#### Build and Run

```bash
# Build image
docker build -t ai-counsellor-frontend .

# Run container
docker run -p 3000:3000 ai-counsellor-frontend
```

---

### 4. AWS (S3 + CloudFront)

#### 1. Export Static Site

```bash
npm run build
npm run export
```

#### 2. Upload to S3

```bash
aws s3 sync out/ s3://your-bucket-name
```

#### 3. Configure CloudFront

- Create CloudFront distribution
- Set origin to S3 bucket
- Configure SSL certificate
- Set custom domain

---

### 5. Railway

#### 1. Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### 2. Initialize Project

```bash
railway init
```

#### 3. Deploy

```bash
railway up
```

#### 4. Set Environment Variables

```bash
railway variables set NEXT_PUBLIC_API_URL=https://your-api.railway.app
```

---

## Environment Configuration

### Production Environment Variables

```bash
# Required
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_SITE_URL=https://yourdomain.com

# Auth (if using NextAuth)
NEXTAUTH_SECRET=<generate-secure-secret>
NEXTAUTH_URL=https://yourdomain.com

# Optional
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### Generate Secrets

```bash
# NEXTAUTH_SECRET
openssl rand -base64 32
```

---

## Build Optimization

### 1. Enable SWC Minification

```javascript
// next.config.js
module.exports = {
  swcMinify: true,
}
```

### 2. Enable Compression

```javascript
module.exports = {
  compress: true,
}
```

### 3. Optimize Images

```javascript
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
  },
}
```

---

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Dependencies
        run: npm ci

      - name: Run Tests
        run: npm test

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.API_URL }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

---

## Health Checks

### 1. Add Health Endpoint

```typescript
// src/app/api/health/route.ts
export async function GET() {
  return Response.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
  });
}
```

### 2. Monitor Endpoint

```bash
curl https://yourdomain.com/api/health
```

---

## Performance Monitoring

### 1. Vercel Analytics

```bash
npm install @vercel/analytics
```

```typescript
// src/app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 2. Google Analytics

```typescript
// src/app/layout.tsx
<Script
  src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
  strategy="afterInteractive"
/>
```

---

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] API endpoints protected
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] XSS prevention active
- [ ] CSRF protection enabled

---

## Troubleshooting

### Build Failures

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

### Environment Variable Issues

```bash
# Verify variables are set
printenv | grep NEXT_PUBLIC
```

### Deployment Errors

Check logs:
```bash
# Vercel
vercel logs

# Netlify
netlify logs

# Docker
docker logs container-name
```

---

## Rollback Strategy

### Vercel

```bash
# List deployments
vercel ls

# Promote specific deployment
vercel promote <deployment-url>
```

### Docker

```bash
# Tag previous version
docker tag ai-counsellor-frontend:latest ai-counsellor-frontend:previous

# Rollback
docker run ai-counsellor-frontend:previous
```

---

## Post-Deployment Checklist

- [ ] Frontend loads successfully
- [ ] API connection works
- [ ] Authentication flow works
- [ ] All pages accessible
- [ ] Images load correctly
- [ ] Forms submit properly
- [ ] Mobile responsive
- [ ] HTTPS working
- [ ] Analytics tracking
- [ ] Error monitoring active

---

## Monitoring & Maintenance

### Daily
- Check error logs
- Monitor response times
- Verify uptime

### Weekly
- Review analytics
- Check performance metrics
- Update dependencies

### Monthly
- Security audits
- Performance optimization
- Feature updates

---

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Railway Docs**: https://docs.railway.app
- **Netlify Docs**: https://docs.netlify.com

---

Deployment complete! 🚀
```

This completes the documentation files! Let me continue with the README file.
