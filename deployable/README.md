# Deployable - AI-Powered Recruitment Platform

A production-ready monorepo for a modern web application built with Next.js (frontend), FastAPI (backend), and PostgreSQL (database).

**Domain:** deployable.in

## Tech Stack

- **Frontend:** Next.js with TypeScript, Tailwind CSS
- **Backend:** FastAPI with Python 3.11
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy + Alembic
- **Authentication:** JWT (access + refresh tokens)
- **Package Manager:** npm (frontend), pip/venv (backend)

## Project Structure

```
/deployable
  /client                 # Next.js frontend
  /server                 # FastAPI backend
  /database               # Database configuration
  docker-compose.yml      # PostgreSQL Docker setup
  README.md              # This file
```

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- npm

## Quick Start

### 1. Start PostgreSQL Database

```bash
# From root directory
docker-compose up -d postgres
```

Verify the database is running:
```bash
docker-compose ps
```

### 2. Setup Backend (FastAPI)

```bash
# Navigate to server directory
cd server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Run Backend:**
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

API Documentation will be available at `http://localhost:8000/docs`

### 3. Setup Frontend (Next.js)

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Test Credentials

Two test users are automatically seeded on backend startup:

1. **Admin User**
   - Email: `admin@deployable.in`
   - Password: `admin123`

2. **Test User**
   - Email: `test@deployable.in`
   - Password: `test123`

## API Endpoints

### Authentication

- `POST /auth/signup` - Create new user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }
  ```

- `POST /auth/login` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
  Returns: `{ "access_token": "...", "token_type": "bearer" }`

- `GET /auth/me` - Get current user info (Protected)
  - Headers: `Authorization: Bearer <token>`

## Frontend Routes

- `/` - Landing page
- `/login` - Login page
- `/signup` - Sign up page
- `/dashboard` - Protected dashboard (requires login)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://deployable_user:deployable_pass@localhost:5432/deployable_db
SECRET_KEY=supersecretkey
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | String | Unique email address |
| hashed_password | String | Bcrypt hashed password |
| full_name | String | User name |
| created_at | DateTime | Account creation timestamp |

## Development

### Backend Development

- FastAPI runs with `--reload` for hot reloading
- Access API docs at `http://localhost:8000/docs`
- Test with provided credentials above

### Frontend Development

- Next.js runs in development mode with fast refresh
- TypeScript is enforced
- Tailwind CSS for styling
- Axios for API requests with automatic token injection

## Production Build

### Backend
```bash
uvicorn app.main:app --port 8000
```

### Frontend
```bash
npm run build
npm start
```

## Stopping Services

```bash
# Stop Docker containers
docker-compose down

# Deactivate Python virtual environment
deactivate
```

## Troubleshooting

### Database Connection Issues
- Ensure Docker is running: `docker-compose ps`
- Check credentials in `.env` match docker-compose.yml
- Wait 5-10 seconds for PostgreSQL to fully start

### Frontend Can't Connect to Backend
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is enabled (configured in backend)

### Python Virtual Environment Issues
- Delete `venv` folder and recreate: `python3 -m venv venv`
- Activate each time: `source venv/bin/activate`

## Notes

- All code follows production-quality standards
- Full type hints are used throughout
- JWT tokens expire after 30 minutes
- Passwords are hashed using bcrypt
- Database credentials should be changed in production
- CORS is restricted to `http://localhost:3000` in development

## License

Proprietary - Deployable Platform
