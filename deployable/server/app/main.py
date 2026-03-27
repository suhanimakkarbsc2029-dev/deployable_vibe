from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db.base import Base
from app.api import auth
from app.models.user import User
from app.db.database import SessionLocal
from app.core.security import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Deployable API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)


def seed_data():
    """Seed test users on startup"""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_exists = db.query(User).filter(User.email == "admin@deployable.in").first()
        if not admin_exists:
            admin_user = User(
                email="admin@deployable.in",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
            )
            db.add(admin_user)
        
        # Check if test user exists
        test_exists = db.query(User).filter(User.email == "test@deployable.in").first()
        if not test_exists:
            test_user = User(
                email="test@deployable.in",
                hashed_password=hash_password("test123"),
                full_name="Test User",
            )
            db.add(test_user)
        
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    seed_data()


@app.get("/")
async def root():
    return {"message": "Welcome to Deployable API"}
