# API Documentation & Architecture

## Backend Architecture

The FastAPI backend follows a layered architecture:

```
app/
├── main.py              # FastAPI app entry, routes setup, seed data
├── api/
│   └── auth.py         # Auth endpoints (signup, login, me)
├── core/
│   ├── config.py       # Settings from environment
│   └── security.py     # JWT & password utilities
├── models/
│   └── user.py         # SQLAlchemy User model
├── schemas/
│   └── user.py         # Pydantic request/response schemas
├── services/
│   └── user.py         # Business logic for user operations
└── db/
    ├── base.py         # SQLAlchemy declarative base
    └── database.py     # Database connection & session
```

### Key Design Patterns

1. **Separation of Concerns:**
   - Models: Database layer (SQLAlchemy)
   - Schemas: API contract (Pydantic)
   - Services: Business logic
   - API: Route handlers

2. **Dependency Injection:**
   - FastAPI Depends() for database sessions
   - Automatic dependency resolution

3. **Type Safety:**
   - Full Python type hints
   - Pydantic validation
   - SQLAlchemy typing

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_users_email ON users(email);
```

**Columns:**
- `id` (UUID): Primary key, auto-generated
- `email` (String): Unique, indexed for fast login
- `hashed_password` (String): bcrypt hashed
- `full_name` (String): User's display name
- `created_at` (DateTime): Account creation timestamp

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### API Reference

#### 1. Sign Up
Create a new user account.

**Endpoint:** `POST /auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Success Response (200):**
```json
{
  "message": "User created successfully"
}
```

**Error Responses:**
- `400 Bad Request` - Email already registered
  ```json
  {"detail": "Email already registered"}
  ```
- `422 Unprocessable Entity` - Invalid input format

**cURL Example:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "pass123",
    "full_name": "John Doe"
  }'
```

---

#### 2. Login
Authenticate user and get JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "admin@deployable.in",
  "password": "admin123"
}
```

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
  ```json
  {"detail": "Invalid credentials"}
  ```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@deployable.in",
    "password": "admin123"
  }'
```

**Token Info:**
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Expiry: 30 minutes
- Use format: `Authorization: Bearer <token>`

---

#### 3. Get Current User
Retrieve authenticated user's information.

**Endpoint:** `GET /auth/me`

**Headers (Required):**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "admin@deployable.in",
  "full_name": "Admin User",
  "created_at": "2026-03-27T10:30:00"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
  ```json
  {"detail": "Invalid authentication credentials"}
  ```
- `404 Not Found` - User not found

**cURL Example:**
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Authentication Flow

### 1. Sign Up Flow
```
[User] → Fill signup form
        ↓
[POST /auth/signup] → Validate email
                     ↓ Check if exists
                     ↓ Hash password
                     ↓ Save to database
                     ↓
        [201 Created] ← Success
        [400 Error]   ← Email exists
```

### 2. Login Flow
```
[User] → Enter email + password
        ↓
[POST /auth/login] → Find user by email
                    ↓ Verify password
                    ↓ Generate JWT token
                    ↓
        [Token] ← Success
        [401]   ← Invalid credentials
```

### 3. Protected Request Flow
```
[Client] → API Request + Bearer Token
          ↓
[GET /auth/me] → Extract token
                ↓ Verify signature
                ↓ Check expiry
                ↓ Get user from payload
                ↓
         [User Data] ← Success
         [401]       ← Invalid token
```

---

## JWT Token Structure

**Payload:**
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "exp": 1743379800
}
```

- `sub`: Subject (user ID)
- `exp`: Expiration time (unix timestamp, 30 min from issue)

**Usage:**
```javascript
// Client-side (JavaScript/TypeScript)
const token = response.data.access_token;
localStorage.setItem("token", token);

// Auto-inject in future requests
const headers = {
  Authorization: `Bearer ${token}`
};
```

---

## Security Features

1. **Password Security:**
   - bcrypt hashing
   - Salted by default
   - Rainbow table resistant

2. **JWT Security:**
   - HS256 signing
   - Secret key validation
   - Expiration enforcement
   - Bearer scheme

3. **Data Validation:**
   - Pydantic schemas
   - Email format validation
   - Type checking

4. **Database Security:**
   - Parameterized queries (SQLAlchemy ORM)
   - SQL injection protection
   - Unique constraints on email

5. **CORS:**
   - Restricted to localhost:3000 in dev
   - Should be configured per environment

---

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error description here"
}
```

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input (email exists, validation failed)
- `401 Unauthorized` - Auth failed or missing token
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error in request body
- `500 Internal Server Error` - Unexpected server error

---

## Rate Limiting

Currently, no rate limiting is configured. For production, consider:
- Limit login attempts to 5 per minute
- Limit signup to 10 per hour per IP
- Use middleware like `slowapi`

---

## Testing Endpoints

### Using Swagger UI
1. Go to `http://localhost:8000/docs`
2. Click on endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using cURL

**Test signup:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

**Test login:**
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@deployable.in","password":"admin123"}' \
  | jq -r '.access_token')
echo $TOKEN
```

**Test protected endpoint:**
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Using Postman
1. Install Postman
2. Import API documentation from `http://localhost:8000/openapi.json`
3. Create POST request to `/auth/login`
4. Get token from response
5. Add to Authorization tab (Bearer Token)
6. Test `/auth/me` with auto token injection

---

## API Response Examples

### Successful Signup
```bash
$ curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"pass123","full_name":"Alice"}'

Response (200):
{
  "message": "User created successfully"
}
```

### Successful Login
```bash
$ curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"pass123"}'

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ZTY2YjI3YS1hMzA1LTRkNzCtOTJkYS1hNWQ2YTk4ZmI5ODIiLCJleHAiOjE3NDMzNzkyMjl9.X-Z9_qxFbN2X3...",
  "token_type": "bearer"
}
```

### Successful Get Me
```bash
$ curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

Response (200):
{
  "id": "7e66b27a-a305-4d7c-92da-a5d6a98fb982",
  "email": "alice@example.com",
  "full_name": "Alice",
  "created_at": "2026-03-27T10:30:00"
}
```

---

## Extending the API

### Adding New Endpoint

1. **Create schema** in `/app/schemas/`:
```python
class ProductCreate(BaseModel):
    name: str
    price: float
```

2. **Create service** in `/app/services/`:
```python
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    return db_product
```

3. **Create route** in `/app/api/`:
```python
@router.post("/products")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)
```

4. **Include router** in `main.py`:
```python
app.include_router(product.router)
```

---

## Monitoring & Debugging

### Enable Detailed Logging
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database State
```bash
psql -h localhost -U deployable_user -d deployable_db
SELECT email, full_name, created_at FROM users;
```

### Verify JWT Token (online)
Go to https://jwt.io and paste your token to see decoded payload.

---

See [README.md](README.md) for general setup and [SETUP.md](SETUP.md) for step-by-step instructions.
