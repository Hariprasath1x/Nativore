"""
SQLAlchemy models for Nativore platform.
Includes User, Restaurant, and Review models.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="user")  # user or admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Restaurant(Base):
    """Restaurant model for Tamil Nadu food establishments."""
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True)  # Chennai, Coimbatore, etc.
    area = Column(String(255), nullable=False)  # Locality/Area
    cuisine = Column(String(255), nullable=False, index=True)  # South Indian, North Indian, etc.
    avg_price = Column(Float, nullable=False)  # Average price for two people
    rating = Column(Float, default=0.0)  # Average rating (0-5)
    review_count = Column(Integer, default=0)  # Number of reviews
    latitude = Column(Float)
    longitude = Column(Float)
    spending_index = Column(Float, default=0.0)  # Economic indicator
    description = Column(Text)
    image_url = Column(String(500))
    phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Restaurant {self.name} - {self.city}>"


class Review(Base):
    """Review model for restaurant reviews."""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    rating = Column(Float, nullable=False)  # Rating (1-5)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review {self.id} - Rating: {self.rating}>"


# Pydantic schemas for request/response validation
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime as dt

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: dt
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Restaurant Schemas
class RestaurantBase(BaseModel):
    name: str
    city: str
    area: str
    cuisine: str
    avg_price: float
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    rating: float
    review_count: int
    spending_index: float
    is_active: bool
    created_at: dt
    
    class Config:
        from_attributes = True

# Review Schemas
class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    restaurant_id: int

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    restaurant_id: int
    created_at: dt
    
    class Config:
        from_attributes = True
