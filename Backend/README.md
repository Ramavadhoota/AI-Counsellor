# AI Counsellor Backend

FastAPI backend for the AI Counsellor application with Google Gemini AI integration.

## Features

- 🔐 JWT-based authentication
- 👤 User profile management with onboarding
- 🤖 AI-powered career counseling (Google Gemini)
- 🌍 University search and recommendations
- 💬 Conversation management
- ✅ Todo/task management
- 📊 PostgreSQL database with SQLAlchemy ORM

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt
- **AI**: Google Gemini API
- **Validation**: Pydantic

## Project Structure

```
app/
├── __init__.py
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration and environment variables
├── database.py               # Database connection and session
├── models.py                 # SQLAlchemy database models
├── schemas.py                # Pydantic schemas for validation
├── crud.py                   # Database CRUD operations
├── auth.py                   # Authentication utilities
├── ai_counsellor.py          # Google Gemini AI integration
├── university_service.py     # External university API service
└── routers/                  # API route handlers
    ├── __init__.py
    ├── auth.py               # Authentication endpoints
    ├── onboarding.py         # User onboarding
    ├── profile.py            # Profile management
    ├── counsellor.py         # AI chat endpoints
    ├── universities.py       # University search
    └── todos.py              # Todo management
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Google Gemini API key

### 2. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_counsellor_db

# Security (generate a secure secret key)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key

# CORS (add your frontend URL)
CORS_ORIGINS=http://localhost:3000

# University API
UNIVERSITY_API_URL=http://universities.hipolabs.com
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb ai_counsellor_db

# The application will automatically create tables on first run
# Or you can use Alembic for migrations:
# alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh access token

### Onboarding
- `POST /api/onboarding/complete` - Complete onboarding
- `GET /api/onboarding/status` - Check onboarding status
- `POST /api/onboarding/skip` - Skip onboarding

### Profile
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/` - Update profile
- `DELETE /api/profile/` - Delete profile

### AI Counsellor
- `POST /api/counsellor/chat` - Chat with AI
- `GET /api/counsellor/conversations` - Get conversations
- `POST /api/counsellor/conversations` - Create conversation
- `GET /api/counsellor/conversations/{id}/messages` - Get messages
- `POST /api/counsellor/conversations/{id}/messages` - Add message

### Universities
- `GET /api/universities/search` - Search universities
- `GET /api/universities/countries` - Get countries list
- `GET /api/universities/recommendations` - Get personalized recommendations
- `GET /api/universities/{country}` - Get universities by country

### Todos
- `GET /api/todos/` - Get all todos
- `POST /api/todos/` - Create todo
- `GET /api/todos/{id}` - Get todo by ID
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `POST /api/todos/{id}/toggle` - Toggle completion

## Database Models

### User
- id (UUID)
- email (String, unique)
- password_hash (String)
- full_name (String)
- onboarding_completed (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

### UserProfile
- id (UUID)
- user_id (UUID, FK)
- academic_background (JSON)
- interests (Array)
- career_goals (JSON)
- preferences (JSON)
- test_scores (JSON)
- created_at (DateTime)
- updated_at (DateTime)

### Conversation
- id (UUID)
- user_id (UUID, FK)
- title (String)
- created_at (DateTime)
- updated_at (DateTime)

### Message
- id (UUID)
- conversation_id (UUID, FK)
- role (String: 'user' or 'assistant')
- content (Text)
- created_at (DateTime)

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## Deployment

### Using Docker

```bash
docker build -t ai-counsellor-backend .
docker run -p 8000:8000 --env-file .env ai-counsellor-backend
```

### Environment Variables for Production

Make sure to set these in production:
- Use a strong `SECRET_KEY`
- Set proper `CORS_ORIGINS`
- Use production database credentials
- Enable HTTPS
- Set appropriate `ACCESS_TOKEN_EXPIRE_MINUTES`

## API Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Get a token by calling `/api/auth/login` or `/api/auth/register`.

## Google Gemini AI Integration

The AI counselor uses Google's Gemini 1.5 Flash model for:
- Personalized career guidance
- University recommendations
- Course suggestions
- Career path analysis
- Document analysis (resume, SOP, etc.)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify DATABASE_URL is correct
- Check firewall settings

### CORS Errors
- Add your frontend URL to CORS_ORIGINS
- Ensure proper format: `http://localhost:3000` (no trailing slash)

### Import Errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License