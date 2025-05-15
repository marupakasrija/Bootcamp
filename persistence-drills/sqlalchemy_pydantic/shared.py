# sqlalchemy_pydantic/shared.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

# --- Database Setup ---
# For Beginner/Intermediate, start with SQLite
DATABASE_URL = "sqlite:///./sql_app.db"

# For Advanced/Level-Up, switch to PostgreSQL
# Make sure your PostgreSQL database is set up and running
# Replace with your actual PostgreSQL connection details when you get to advanced drills
# DATABASE_URL = "postgresql://your_user:your_password@localhost:5432/your_db_name"


# The base class which all your models will inherit from.
Base = declarative_base()

# Create a database engine
# `connect_args` is needed for SQLite if using check_same_thread=False (common for web apps)
# For PostgreSQL, this is not needed.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Helper function to get a database session (useful for larger apps/frameworks)
# For these simple scripts, we will manually create and close sessions for clarity
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to create tables (run this once initially)
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

# --- SQLAlchemy Models ---
# Define your database table structure here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # Added for advanced drill (schema evolution implicitly)
    created_at = Column(DateTime, server_default=func.now())

    # Define a relationship to the Post table (defined later)
    # 'User.posts' will be a list of Post objects associated with this user
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id")) # Foreign key linking to users table

    # Define a relationship back to the User table
    # 'Post.author' will be a single User object
    author = relationship("User", back_populates="posts")


# --- Pydantic Schemas ---
# Define data structures for input validation and output serialization
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    # Add validation specific to creation if needed (e.g., password, though not in model yet)
    pass

class UserSchema(UserBase):
    id: int
    # Include other fields you want to expose
    created_at: datetime.datetime

    class Config:
        orm_mode = True # Allows Pydantic model to read data from SQLAlchemy ORM objects
        # Use from_orm = True in Pydantic V1

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None

class PostCreate(PostBase):
    author_id: int # Include author_id when creating a post

class PostSchema(PostBase):
    id: int
    author_id: int # Include author_id in the schema
    # Add a nested UserSchema to show the author's info - uncomment later for advanced
    # author: UserSchema # This causes recursion unless you handle it or exclude it

    class Config:
        orm_mode = True
        # Use from_orm = True in Pydantic V1


# Pydantic schema for a User with their posts (nested)
# Note: This schema refers to PostSchema, which should ideally NOT recursively refer back to UserSchema
# To avoid infinite recursion in Pydantic models, either exclude the 'author' field in PostSchema
# when nesting, or use Pydantic's UpdateForwardRefs after all models are defined.
# For simplicity in this example, we'll uncomment the 'author' field in PostSchema later if needed
# and might just show fetching separately or manually construct the nested dict.
# A common pattern is to have separate schemas for read/write and different levels of nesting.

class UserWithPostsSchema(UserSchema):
    posts: List[PostSchema] = [] # List of PostSchema objects

    class Config:
        orm_mode = True
        # Use from_orm = True in Pydantic V1