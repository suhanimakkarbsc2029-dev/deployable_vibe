from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password
from typing import Optional


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, credentials: UserLogin) -> Optional[User]:
    user = get_user_by_email(db, credentials.email)
    if not user:
        return None
    if not verify_password(credentials.password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    from uuid import UUID
    try:
        uuid_obj = UUID(user_id)
        return db.query(User).filter(User.id == uuid_obj).first()
    except (ValueError, TypeError):
        return None
