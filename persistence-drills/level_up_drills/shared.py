# shared.py

# --- SQLAlchemy and Pydantic Imports ---
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    DateTime, func, Float, LargeBinary, Boolean, Date, Numeric
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session # Added Session for type hinting
from sqlalchemy.dialects.postgresql import insert as postgres_insert # For upserts
from sqlalchemy.dialects.sqlite import insert as sqlite_insert     # For upserts
from sqlalchemy.dialects import postgresql, sqlite                 # For dialect checking

# --- Async SQLAlchemy Imports (Needed if using async setup) ---
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# --- Pydantic Imports ---
from pydantic import BaseModel, EmailStr # EmailStr requires 'email-validator'
from typing import List, Optional
import datetime # For DateTime fields

# --- Database Setup ---

# --- Option 1: Synchronous SQLite (Default for most beginner/intermediate exercises) ---
DATABASE_URL = "sqlite:///./sql_app.db"
# Use this engine and sessionmaker for sync operations
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Helper function to get a sync database session (less used in simple scripts, but good practice)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Helper function to create tables synchronously
def create_tables():
    print(f"Attempting to create tables for {DATABASE_URL}...")
    # Base.metadata contains all models defined by inheriting from Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created (sync).")


# --- Option 2: Asynchronous PostgreSQL (Needed for async drills and recommended for performance/features in others) ---
# To use this, COMMENT OUT the lines under "Option 1" above
# and UNCOMMENT the lines below.
# Make sure your PostgreSQL database is set up and running
# and you have installed asyncpg: pip install asyncpg
# REPLACE WITH YOUR ACTUAL ASYNC POSTGRESQL CONNECTION DETAILS
# ASYNC_DATABASE_URL = "postgresql+asyncpg://your_user:your_password@localhost:5432/your_db_name"
# # Use this engine and sessionmaker for async operations
# async_engine = create_async_engine(ASYNC_DATABASE_URL)
# AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
# # Helper function to get an async database session
# async def get_async_db():
#     async with AsyncSessionLocal() as db:
#         yield db
# # Helper function to create tables asynchronously
# async def create_async_tables():
#      print(f"Attempting to create tables for {ASYNC_DATABASE_URL}...")
#      async with async_engine.begin() as conn:
#          await conn.run_sync(Base.metadata.create_all) # Run sync create_all in async context
#      print("Database tables created (async).")


# The base class which all your models will inherit from.
Base = declarative_base()

# --- SQLAlchemy Models ---
# Define your database table structures here by inheriting from Base

# User and Post models (from practice exercises)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False) # Added in Drill 1 concept

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Made nullable=False for stronger FK

    author = relationship("User", back_populates="posts")

# Product model for Upsert Drill (Drill 3)
class ProductForUpsert(Base): # Changed name to avoid conflict if another Product model existed
    __tablename__ = "products_for_upsert"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False) # Unique constraint needed for upsert
    price = Column(Float, nullable=False)

# User Email History model for Versioning Drill (Drill 4)
class UserEmailHistory(Base):
    __tablename__ = "user_email_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Link to the user
    email = Column(String, nullable=False) # The email at this version
    changed_at = Column(DateTime, server_default=func.now(), nullable=False)
    # Optional: changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

# Account model for Concurrency Drill (Drill 5)
class Account(Base):
    __tablename__ = "accounts_for_concurrency"
    account_id = Column(Integer, primary_key=True)
    account_holder = Column(String, nullable=False)
    balance = Column(Float, nullable=False) # Added nullable=False

# Models for Large Binary Data Drill (Drill 6)
class UserProfileBlob(Base):
    __tablename__ = "user_profiles_blob"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False) # Link to user
    profile_image = Column(LargeBinary, nullable=False) # Store image bytes

class UserProfileFilePath(Base):
    __tablename__ = "user_profiles_filepath"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False) # Link to user
    image_path = Column(String, nullable=False) # Store the path to the image file

# Models for Schema-First Drill (Drill 7) - Mapping to hypothetical existing tables
class ProductSchemaFirst(Base):
    __tablename__ = "products_schema_first"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False) # Use Numeric for precision
    is_available = Column(Boolean, default=True)
    release_date = Column(Date, nullable=True)

class OrderSchemaFirst(Base):
    __tablename__ = "orders_schema_first"
    order_id = Column(Integer, primary_key=True)
    customer_email = Column(String(255), nullable=False)
    order_date = Column(DateTime, server_default=func.now(), nullable=True) # TIMESTAMP WITH TIME ZONE maps to DateTime

# Product model for Soft Delete Drill (Drill 8)
class ProductSoftDelete(Base):
    __tablename__ = "products_soft_delete"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    deleted_at = Column(DateTime, nullable=True) # The soft delete marker

# Product model for Large Dataset Testing Drill (Drill 9)
class LargeProduct(Base):
    __tablename__ = "products_large_test"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String) # Added another field


# --- Pydantic Schemas ---
# Define data structures for input validation and output serialization

class UserBase(BaseModel):
    name: str
    email: EmailStr # Requires 'email-validator'

class UserCreate(UserBase):
    pass # No extra fields for creation in this model

# Updated for Pydantic V2: 'orm_mode = True' renamed to 'from_attributes = True'
class UserSchema(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True # Allows Pydantic model to read data from SQLAlchemy ORM objects

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None

class PostCreate(PostBase):
    author_id: int # Include author_id when creating a post

# Updated for Pydantic V2
class PostSchema(PostBase):
    id: int
    author_id: int
    # Removed recursive 'author: UserSchema' here to avoid infinite recursion in nested schemas
    # If needed, define separate schemas or handle nesting carefully.

    class Config:
        from_attributes = True

# Pydantic schema for a User with their posts (nested) - Updated for Pydantic V2
class UserWithPostsSchema(UserSchema):
    # This schema includes the nested list of posts using the PostSchema
    posts: List[PostSchema] = []

    class Config:
        from_attributes = True

# Pydantic schemas for other models can be added as needed for API layers
# For example:
# class ProductUpsertSchema(BaseModel):
#     name: str
#     price: float
#
# class AccountSchema(BaseModel):
#     account_id: int
#     account_holder: str
#     balance: float
#     class Config:
#         from_attributes = True
if __name__ == "__main__":
    # This block will run only when you execute shared.py directly
    create_tables() # Or create_async_tables() if you are using the async setup
