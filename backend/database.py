"""
Database configuration and session management for Nativore.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nativore.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True if os.getenv("DEBUG") == "True" else False
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function to get database session.
    Yields a database session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize database
def init_db():
    """
    Initialize database by creating all tables.
    Should be called on application startup.
    """
    from models import User, Restaurant, Review  # Import models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

# Function to drop all tables (for development/testing)
def drop_db():
    """
    Drop all database tables.
    Use with caution - only for development/testing.
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️  All database tables dropped!")
