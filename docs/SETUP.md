# 🔧 Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js 18+** and npm (or yarn/pnpm)
- **Git** for version control
- **Code editor** (VS Code recommended)
- **Backend API** running (see backend setup guide)

---

## 📥 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-counsellor.git
cd ai-counsellor/frontend
```

### 2. Install Dependencies

```bash
npm install
```

**Alternative package managers:**
```bash
# Using Yarn
yarn install

# Using pnpm
pnpm install
```

---

## 🔐 Environment Configuration

### 1. Create Environment File

```bash
cp .env.local.example .env.local
```

### 2. Configure Environment Variables

Edit `.env.local` with your configuration:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Frontend Site URL
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# NextAuth Configuration (Optional - if using NextAuth.js)
NEXTAUTH_SECRET=your-random-secret-here
NEXTAUTH_URL=http://localhost:3000

# Optional: Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### 3. Generate Secrets (if using NextAuth)

```bash
# Generate a secure random secret
openssl rand -base64 32
```

Copy the output and set it as `NEXTAUTH_SECRET` in `.env.local`.

---

## 🚀 Running the Development Server

### 1. Start Backend API First

Make sure your backend API is running on `http://localhost:8000`.

See the backend setup guide for instructions.

### 2. Start Frontend Dev Server

```bash
npm run dev
```

The application will start at **http://localhost:3000**.

### 3. Verify Installation

Open your browser and navigate to:
- **Landing Page**: http://localhost:3000
- **Login**: http://localhost:3000/login
- **Signup**: http://localhost:3000/signup

---

## 📁 Project Structure Overview

```
frontend/
├── src/
│   ├── app/                    # Next.js pages (App Router)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── login/page.tsx      # Login page
│   │   ├── signup/page.tsx     # Signup page
│   │   ├── dashboard/page.tsx  # Dashboard
│   │   └── ...
│   │
│   ├── components/             # React components
│   │   ├── ui/                 # UI components (Button, Card, etc.)
│   │   ├── auth/               # Auth forms
│   │   ├── dashboard/          # Dashboard widgets
│   │   └── ...
│   │
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client (Axios)
│   │   ├── auth.ts             # Auth helpers
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Utility functions
│   │
│   └── middleware.ts           # Route protection
│
├── public/                     # Static assets
│   ├── logo.svg
│   └── images/
│
├── docs/                       # Documentation
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.ts          # Tailwind config
├── next.config.js              # Next.js config
└── .env.local                  # Environment variables
```

---

## 🔧 Configuration Files

### 1. TypeScript Configuration (`tsconfig.json`)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### 2. Tailwind Configuration (`tailwind.config.ts`)

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F172A',
        surface: '#1E293B',
        primary: '#20B2AA',
        secondary: '#64748B',
        accent: '#38BDF8',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        muted: '#475569',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
```

### 3. Next.js Configuration (`next.config.js`)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard',
        permanent: false,
        has: [
          {
            type: 'cookie',
            key: 'token',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

---

## 🔌 API Client Setup

The API client is pre-configured in `src/lib/api.ts`:

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auto-inject token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🛡️ Middleware Setup

Route protection is handled in `src/middleware.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';

const protectedRoutes = ['/dashboard', '/profile', '/counsellor', '/universities', '/onboarding'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const pathname = request.nextUrl.pathname;

  // Check if route is protected
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  );

  // Redirect to login if accessing protected route without token
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Redirect to dashboard if accessing login/signup with token
  if ((pathname === '/login' || pathname === '/signup') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

---

## 🎨 Styling Setup

### Global Styles (`src/app/globals.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-white antialiased;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold;
  }

  input, textarea, select {
    @apply bg-surface border border-gray-700 rounded-lg px-4 py-2 
           text-white placeholder-gray-400 focus:outline-none 
           focus:ring-2 focus:ring-primary transition-all;
  }

  button {
    @apply transition-all duration-200;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary hover:bg-primary/90 text-white font-medium 
           px-4 py-2 rounded-lg transition-all;
  }

  .btn-secondary {
    @apply bg-surface hover:bg-surface/80 text-white font-medium 
           px-4 py-2 rounded-lg border border-gray-700 transition-all;
  }

  .card {
    @apply bg-surface rounded-lg p-6 border border-gray-800;
  }
}
```

---

## 📦 Available Scripts

```bash
# Development (with hot reload)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint

# Fix linting issues
npm run lint:fix
```

---

## 🧪 Testing Your Setup

### 1. Test Landing Page

Visit http://localhost:3000 - should see the landing page.

### 2. Test Authentication

1. Navigate to http://localhost:3000/signup
2. Create an account
3. You should be redirected to onboarding or dashboard
4. Token should be stored in localStorage

### 3. Test Protected Routes

1. Try accessing http://localhost:3000/dashboard without login
2. Should redirect to login page
3. After login, should access dashboard successfully

### 4. Test API Connection

Open browser console and check:
```javascript
// Should see API calls to http://localhost:8000
// Check Network tab in DevTools
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
# On macOS/Linux:
lsof -ti:3000 | xargs kill -9

# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### API Connection Issues

1. **Check backend is running**: Visit http://localhost:8000/docs
2. **Check CORS settings** in backend
3. **Verify API URL** in `.env.local`

### Module Not Found Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Type Errors

```bash
# Regenerate TypeScript types
npm run type-check
```

### Build Errors

```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

---

## 🔄 Development Workflow

1. **Start backend API** (port 8000)
2. **Start frontend dev server** (port 3000)
3. **Make changes** to components
4. **Hot reload** updates automatically
5. **Test in browser**
6. **Check console** for errors
7. **Run type checking**: `npm run type-check`
8. **Run linting**: `npm run lint`
9. **Commit changes**

---

## 📱 Testing Responsive Design

### Browser DevTools

1. Open DevTools (F12)
2. Click "Toggle device toolbar" (Ctrl+Shift+M)
3. Test different screen sizes:
   - Mobile: 375px width
   - Tablet: 768px width
   - Desktop: 1920px width

### Tailwind Breakpoints

```typescript
// sm: 640px
// md: 768px
// lg: 1024px
// xl: 1280px
// 2xl: 1536px
```

---

## 🔐 Security Checklist

- [ ] `.env.local` added to `.gitignore`
- [ ] Never commit secrets to Git
- [ ] Use environment variables for API URLs
- [ ] Token stored securely (httpOnly cookies in production)
- [ ] HTTPS enabled in production
- [ ] CORS configured correctly on backend

---

## 📚 Next Steps

1. **Explore the codebase**: Check `src/app` and `src/components`
2. **Read documentation**: See `docs/` folder
3. **Customize theme**: Edit `tailwind.config.ts`
4. **Add features**: Build on existing components
5. **Deploy**: See `docs/DEPLOYMENT.md`

---

## 🆘 Getting Help

- **Documentation**: Check `docs/` folder
- **API Docs**: http://localhost:8000/docs
- **Issues**: Create an issue on GitHub
- **Team**: Ask your team members

---

## ✅ Setup Complete!

You're ready to start developing! 🚀

Run `npm run dev` and visit http://localhost:3000 to see your app in action.
