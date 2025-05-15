# level_up_drills/02_model_boundary_enforcement/services.py

from shared import SessionLocal, User # Import SQLAlchemy models and session maker
from sqlalchemy.orm import Session # Import Session type for type hinting
from typing import List, Optional

# This layer interacts directly with SQLAlchemy models and the database session.
# It should not know about Pydantic models.

def get_user_from_db(db: Session, user_id: int) -> Optional[User]:
    """Fetches a SQLAlchemy User model by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_users_from_db(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Fetches a list of SQLAlchemy User models."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user_in_db(db: Session, user: User) -> User:
    """Adds a new SQLAlchemy User model to the database."""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_email_in_db(db: Session, user: User, new_email: str) -> User:
    """Updates the email of an existing SQLAlchemy User model."""
    user.email = new_email
    db.commit()
    db.refresh(user)
    return user

# Add other database operations here...