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
