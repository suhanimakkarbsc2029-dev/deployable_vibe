# Complete Setup Guide - Deployable Monorepo

This guide walks you through setting up and running the entire Deployable platform locally.

## System Requirements

- macOS 11+, Linux, or Windows (WSL2)
- Docker Desktop installed and running
- Python 3.11+
- Node.js 18+ & npm 9+
- Git
- Terminal/Command line access

## Step-by-Step Setup

### Phase 1: PostgreSQL Database (Docker)

**1. Start the database container:**

```bash
cd /path/to/deployable
docker-compose up -d postgres
```

**2. Verify PostgreSQL is running:**

```bash
docker-compose ps
```

Expected output shows `postgres` container with status `Up`.

**3. Test database connection (optional):**

```bash
# Install postgres client (if not available)
# macOS: brew install libpq
# Ubuntu: sudo apt-get install postgresql-client

psql -h localhost -U deployable_user -d deployable_db
# Password: deployable_pass
```

Press `Ctrl+D` to exit psql.

---

### Phase 2: FastAPI Backend Setup

**1. Navigate to server directory:**

```bash
cd server
```

**2. Create and activate Python virtual environment:**

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

**3. Verify activation:**

Your terminal prompt should show `(venv)` prefix.

**4. Install dependencies:**

```bash
pip install -r requirements.txt
```

**5. Verify installation:**

```bash
pip list
```

Should show: fastapi, sqlalchemy, psycopg2-binary, etc.

**6. Start the backend server:**

```bash
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**7. Verify backend is working:**

Open in browser: `http://localhost:8000/docs`

You should see the Swagger API documentation with three auth endpoints:
- POST /auth/signup
- POST /auth/login
- GET /auth/me

**8. Test seed users:** 

Open `http://localhost:8000/docs`, click "Try it out" on POST /auth/login:
```json
{
  "email": "admin@deployable.in",
  "password": "admin123"
}
```

Should return access token.

**NOTE:** Keep the backend terminal running. Open a new terminal for Phase 3.

---

### Phase 3: Next.js Frontend Setup

**1. Open NEW terminal window and navigate to client:**

```bash
cd path/to/deployable/client
```

**2. Install dependencies:**

```bash
npm install
```

This will install React, Next.js, Tailwind CSS, axios, etc.

**3. Start frontend development server:**

```bash
npm run dev
```

Expected output:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

**4. Access the application:**

Open browser: `http://localhost:3000`

You should see the Deployable landing page with "AI-Powered Recruitment" headline.

---

## Using the Application

### Landing Page
- URL: `http://localhost:3000`
- Shows headline, subtext, and CTA buttons
- "Get Started" button → Signup
- "Login" button → Login page

### Sign Up
1. Click "Get Started" or go to `/signup`
2. Fill in:
   - Full Name: (any name)
   - Email: user@example.com
   - Password: (any password)
3. Click "Sign up"
4. Redirects to login page

### Login
1. URL: `http://localhost:3000/login`
2. Use test credentials:
   - Email: `admin@deployable.in`
   - Password: `admin123`
   - OR: `test@deployable.in` / `test123`
3. Click "Sign in"
4. On success → Redirects to `/dashboard`

### Dashboard
- URL: `http://localhost:3000/dashboard` (protected)
- Shows welcome message
- Displays logged-in user info
- "Logout" button returns to landing page

---

## Troubleshooting

### Database Issues

**Error: "connection refused"**
```bash
# Check if Docker is running
docker-compose ps

# If not running, start it
docker-compose up -d postgres

# Wait 5-10 seconds for database to be ready
```

**Error: "password authentication failed"**
- Check credentials in `/server/.env`
- Should match docker-compose.yml
- Default: user=`deployable_user`, password=`deployable_pass`

**Error: "database does not exist"**
- Docker will create it automatically
- Wait 10 seconds after docker-compose up and restart backend

### Backend Issues

**Error: "ModuleNotFoundError"**
```bash
# Ensure venv is activated (should see (venv) in prompt)
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

**Error: "port 8000 already in use"**
```bash
# Kill process on port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Backend won't connect to database:**
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check DATABASE_URL in `/server/.env`
- Wait 10 seconds after starting Docker

### Frontend Issues

**Error: "NEXT_PUBLIC_API_URL not set"**
- Check `/client/.env.local` exists
- Should contain: `NEXT_PUBLIC_API_URL=http://localhost:8000`

**Error: "Cannot find module 'react'"**
```bash
# Reinstall node modules
rm -rf node_modules
npm install
```

**Error: "port 3000 already in use"**
```bash
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Frontend can't reach backend:**
- Ensure backend is running: `http://localhost:8000`
- Check `.env.local` has correct API_URL
- Check browser Console (F12) for CORS errors
- Refresh page with Ctrl+Shift+R (hard refresh)

### Authentication Issues

**"Invalid credentials" when logging in**
- Use correct test credentials:
  - Email: `admin@deployable.in` or `test@deployable.in`
  - Password: `admin123` or `test123`
- If custom user doesn't work, restart backend to re-seed

**Stuck on login redirect loop**
- Clear browser localStorage: F12 → Application → Clear
- Clear cookies
- Logout and try again

**"Token expired" after 30 minutes**
- This is expected - login again
- In production, refresh tokens would be used

---

## Development Workflow

### Common Tasks

**Check backend logs:**
```bash
# Terminal running backend shows all logs in real-time
```

**Check frontend logs:**
```bash
# Terminal running frontend shows build logs
```

**Rebuild frontend after package changes:**
```bash
cd client
npm install
npm run dev
```

**Test API directly:**
```bash
# Using curl to test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@deployable.in","password":"admin123"}'
```

**Access database directly:**
```bash
psql -h localhost -U deployable_user -d deployable_db

# List tables
\dt

# Query users
SELECT * FROM users;

# Exit
\q
```

---

## Stopping All Services

**Terminal 1 - Frontend (Press Ctrl+C):**
```
^C
npm dev stopped
```

**Terminal 2 - Backend (Press Ctrl+C):**
```
^C
(shutdown message)
```

**Terminal 3 - Stop PostgreSQL:**
```bash
docker-compose down
```

---

## Running Production Build

### Frontend Production Build
```bash
cd client
npm run build
npm start
```

### Backend Production
```bash
cd server
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## File Locations Reference

| Item | Path |
|------|------|
| Backend code | `/server/app/` |
| Backend models | `/server/app/models/user.py` |
| Backend auth | `/server/app/api/auth.py` |
| Frontend code | `/client/app/` |
| Frontend pages | `/client/app/(page/login/signup/dashboard)` |
| Frontend API client | `/client/lib/api.ts` |
| Database config | `/docker-compose.yml` |
| Backend config | `/server/.env` |
| Frontend config | `/client/.env.local` |

---

## Next Steps

After successful setup, you can:

1. Customize the Landing page design
2. Add more API endpoints
3. Create additional database models
4. Implement more frontend pages
5. Configure production environment variables
6. Set up CI/CD pipeline
7. Enable HTTPS for production
8. Configure advanced JWT with refresh tokens

Refer to main [README.md](README.md) for additional information.
