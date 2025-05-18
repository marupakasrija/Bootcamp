from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

# --- Database Setup ---
DATABASE_URL = "sqlite:///./sql_app.db"
Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

# --- SQLAlchemy Models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id")) 
    author = relationship("User", back_populates="posts")


# --- Pydantic Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True 

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None

class PostCreate(PostBase):
    author_id: IndentationError

class PostSchema(PostBase):
    id: int
    author_id: int 

    class Config:
        orm_mode = True

class UserWithPostsSchema(UserSchema):
    posts: List[PostSchema] = [] 

    class Config:
        orm_mode = True