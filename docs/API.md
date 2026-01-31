# 📚 Frontend - Documentation Files

## docs/API.md

```markdown
# API Documentation

## Overview

This document describes the frontend API integration with the FastAPI backend.

## Base Configuration

```typescript
// Located in: src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

---

## Authentication Endpoints

### Login

**POST** `/api/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "onboarding_completed": false
  }
}
```

---

### Signup

**POST** `/api/auth/signup`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "onboarding_completed": false
  }
}
```

---

### Get Current User

**GET** `/api/auth/me`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "onboarding_completed": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Onboarding Endpoints

### Submit Onboarding

**POST** `/api/onboarding`

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "education_level": "bachelors",
  "degree": "B.Tech",
  "major": "Computer Science",
  "graduation_year": 2024,
  "gpa": 3.5,
  "intended_degree": "masters",
  "field_of_study": "Computer Science",
  "target_intake": "fall_2025",
  "preferred_countries": ["USA", "Canada"],
  "budget_min": 30000,
  "budget_max": 50000,
  "funding_plan": "self_funded",
  "ielts_status": "completed",
  "gre_status": "preparing",
  "sop_status": "drafting"
}
```

**Response:**
```json
{
  "message": "Onboarding completed successfully",
  "user": {
    "id": "uuid",
    "onboarding_completed": true
  }
}
```

---

## Profile Endpoints

### Get Profile

**GET** `/api/profile`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "education_level": "bachelors",
  "degree": "B.Tech",
  "major": "Computer Science",
  "graduation_year": 2024,
  "gpa": 3.5,
  "intended_degree": "masters",
  "field_of_study": "Computer Science",
  "target_intake": "fall_2025",
  "preferred_countries": ["USA", "Canada"],
  "budget_min": 30000,
  "budget_max": 50000,
  "funding_plan": "self_funded",
  "ielts_status": "completed",
  "gre_status": "preparing",
  "sop_status": "drafting",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

---

### Update Profile

**PUT** `/api/profile`

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "full_name": "John Doe Updated",
  "gpa": 3.7,
  "ielts_status": "completed"
}
```

**Response:**
```json
{
  "message": "Profile updated successfully",
  "user": { /* updated user object */ }
}
```

---

## Universities Endpoints

### Get Recommended Universities

**GET** `/api/universities/recommendations`

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `country` (optional): Filter by country
- `category` (optional): Filter by category (dream/target/safe)
- `limit` (optional): Number of results (default: 50)

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Stanford University",
    "country": "USA",
    "city": "Stanford, CA",
    "category": "dream",
    "tuition_min": 55000,
    "tuition_max": 60000,
    "acceptance_rate": 0.04,
    "fit_score": 85,
    "risk_level": "high",
    "why_fits": [
      "Strong CS program matches your background",
      "Budget aligns with your range"
    ],
    "risks": [
      "Highly competitive acceptance rate",
      "GRE score improvement recommended"
    ],
    "shortlisted": false,
    "locked": false
  }
]
```

---

### Get University Details

**GET** `/api/universities/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Stanford University",
  "country": "USA",
  "city": "Stanford, CA",
  "category": "dream",
  "tuition_min": 55000,
  "tuition_max": 60000,
  "acceptance_rate": 0.04,
  "fit_score": 85,
  "risk_level": "high",
  "why_fits": ["..."],
  "risks": ["..."],
  "shortlisted": false,
  "locked": false,
  "details": {
    "description": "...",
    "programs": ["..."],
    "requirements": {
      "gpa_min": 3.5,
      "ielts_min": 7.0,
      "gre_min": 320
    }
  }
}
```

---

### Shortlist University

**POST** `/api/universities/{id}/shortlist`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "University shortlisted successfully",
  "university_id": "uuid"
}
```

---

### Lock University

**POST** `/api/universities/{id}/lock`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "University locked successfully",
  "university_id": "uuid",
  "tasks_created": 15
}
```

---

### Unlock University

**POST** `/api/universities/{id}/unlock`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "University unlocked successfully",
  "university_id": "uuid"
}
```

---

## AI Counsellor Endpoints

### Send Chat Message

**POST** `/api/counsellor/chat`

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "message": "What documents do I need for US universities?"
}
```

**Response:**
```json
{
  "response": "For US universities, you typically need: 1. Academic transcripts...",
  "conversation_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### Get Chat History

**GET** `/api/counsellor/history`

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `limit` (optional): Number of messages (default: 50)

**Response:**
```json
{
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "What documents do I need?",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "For US universities, you need...",
      "timestamp": "2024-01-15T10:30:15Z"
    }
  ]
}
```

---

## To-Do Endpoints

### Get All Todos

**GET** `/api/todos`

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `completed` (optional): Filter by completion status
- `category` (optional): Filter by category

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Complete IELTS exam",
    "description": "Schedule and complete IELTS test",
    "category": "exam",
    "deadline": "2024-06-01T00:00:00Z",
    "completed": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### Create Todo

**POST** `/api/todos`

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "title": "Prepare SOP",
  "description": "Write statement of purpose for Stanford",
  "category": "document",
  "deadline": "2024-08-01T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Prepare SOP",
  "description": "Write statement of purpose for Stanford",
  "category": "document",
  "deadline": "2024-08-01T00:00:00Z",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### Update Todo

**PUT** `/api/todos/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "completed": true
}
```

**Response:**
```json
{
  "id": "uuid",
  "completed": true,
  "updated_at": "2024-01-15T12:00:00Z"
}
```

---

### Delete Todo

**DELETE** `/api/todos/{id}`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Token is obtained from login/signup endpoints and stored in localStorage by the frontend.

---

## Rate Limiting

- **General endpoints**: 100 requests per minute
- **AI Counsellor**: 10 requests per minute
- **Authentication**: 5 requests per minute

---

## Pagination

Endpoints that return lists support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response includes:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "pages": 8
}
```

---

## WebSocket (Future)

Real-time features will use WebSocket connections:

```
ws://localhost:8000/ws/chat?token={jwt_token}
```

---

## Testing

Use the API health check endpoint:

**GET** `/api/health`

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```
```

---

## docs/SETUP.md

```markdown
# Setup Guide

## Prerequisites

Before setting up the project, ensure you have:

- **Node.js** 18.17 or later
- **npm** or **yarn** package manager
- **Git** for version control
- **Backend API** running (see backend README)

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-counsellor-hackathon.git
cd ai-counsellor-hackathon/frontend
```

---

### 2. Install Dependencies

```bash
npm install
```

Or with yarn:

```bash
yarn install
```

---

### 3. Environment Setup

Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

Update `.env.local` with your values:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Site Configuration
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=AI Study Abroad Counsellor

# Optional: NextAuth (if using)
NEXTAUTH_SECRET=your-random-secret-here
NEXTAUTH_URL=http://localhost:3000
```

Generate NextAuth secret:

```bash
openssl rand -base64 32
```

---

### 4. Start Development Server

```bash
npm run dev
```

Or with yarn:

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Project Structure

```
frontend/
├── public/              # Static assets
│   ├── logo.svg
│   ├── favicon.ico
│   └── manifest.json
│
├── src/
│   ├── app/            # Next.js 14 App Router
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   ├── globals.css         # Global styles
│   │   ├── login/              # Auth pages
│   │   ├── signup/
│   │   ├── onboarding/
│   │   ├── dashboard/
│   │   ├── counsellor/
│   │   ├── universities/
│   │   ├── profile/
│   │   └── api/                # API routes
│   │
│   ├── components/     # React components
│   │   ├── ui/                 # Reusable UI components
│   │   ├── auth/               # Auth components
│   │   ├── onboarding/         # Onboarding wizard
│   │   ├── dashboard/          # Dashboard components
│   │   ├── counsellor/         # Chat interface
│   │   └── universities/       # University components
│   │
│   ├── lib/            # Utilities
│   │   ├── api.ts              # API client (axios)
│   │   ├── auth.ts             # Auth utilities
│   │   ├── store.ts            # Zustand store
│   │   └── utils.ts            # Helper functions
│   │
│   └── types/          # TypeScript types
│       ├── index.ts
│       ├── user.ts
│       ├── university.ts
│       └── todo.ts
│
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── .env.local
```

---

## Configuration Files

### package.json

Dependencies are managed here. Key packages:

- **next**: React framework
- **react**: UI library
- **typescript**: Type safety
- **tailwindcss**: Styling
- **axios**: HTTP client
- **zustand**: State management
- **lucide-react**: Icons

---

### next.config.js

Next.js configuration for:
- Image optimization
- API rewrites
- Environment variables

---

### tailwind.config.ts

Tailwind CSS configuration with:
- Custom color palette (dark theme)
- Custom spacing
- Typography settings

---

### tsconfig.json

TypeScript configuration with:
- Path aliases (`@/` → `src/`)
- Strict type checking
- Next.js specific settings

---

## Development Workflow

### 1. Create New Page

```bash
# Create new route
mkdir -p src/app/new-page
touch src/app/new-page/page.tsx
```

Example page:

```typescript
export default function NewPage() {
  return (
    <div className="min-h-screen bg-background">
      <h1 className="text-white">New Page</h1>
    </div>
  );
}
```

---

### 2. Create New Component

```bash
# Create component file
touch src/components/MyComponent.tsx
```

Example component:

```typescript
import { Button } from '@/components/ui/Button';

export const MyComponent = () => {
  return (
    <Button onClick={() => alert('Clicked!')}>
      Click Me
    </Button>
  );
};
```

---

### 3. Add API Integration

Use the API client:

```typescript
import { api } from '@/lib/api';

const fetchData = async () => {
  try {
    const response = await api.get('/api/endpoint');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

---

## Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm run start

# Linting
npm run lint

# Type checking
npm run type-check
```

---

## Environment Variables

### Required

- `NEXT_PUBLIC_API_URL`: Backend API URL

### Optional

- `NEXT_PUBLIC_SITE_URL`: Frontend URL (for SEO)
- `NEXTAUTH_SECRET`: NextAuth secret (if using)
- `NEXTAUTH_URL`: NextAuth URL (if using)

---

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

---

### Module Not Found

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

### Type Errors

```bash
# Rebuild TypeScript definitions
npm run type-check
```

---

### Styling Issues

```bash
# Rebuild Tailwind CSS
npm run dev
# Refresh browser with hard reload (Cmd+Shift+R)
```

---

## Testing

### Manual Testing Checklist

- [ ] Landing page loads
- [ ] Signup flow works
- [ ] Login flow works
- [ ] Onboarding completes
- [ ] Dashboard displays data
- [ ] AI chat responds
- [ ] Universities list loads
- [ ] University details show
- [ ] Profile updates save

---

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions.

---

## Getting Help

- **Documentation**: Check docs/ folder
- **API Reference**: See API.md
- **Backend Issues**: Check backend README
- **Frontend Issues**: Create GitHub issue

---

## Next Steps

1. ✅ Complete setup
2. ✅ Start development server
3. ✅ Test authentication flow
4. ✅ Explore all pages
5. ✅ Customize as needed
6. ✅ Build features
7. ✅ Deploy to production

Good luck! 🚀
```

I'll create the remaining documentation files in the next message due to length constraints.
