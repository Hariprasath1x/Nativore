"""
Restaurant routes for Nativore platform.
CRUD operations for restaurants.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Restaurant, RestaurantCreate, RestaurantResponse, User
from routes.auth import get_current_active_user

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


@router.get("/", response_model=List[RestaurantResponse])
async def get_restaurants(
    city: Optional[str] = Query(None, description="Filter by city"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    max_price: Optional[float] = Query(None, gt=0, description="Maximum price"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get list of restaurants with optional filters.
    
    Query parameters:
    - city: Filter by city name
    - cuisine: Filter by cuisine type
    - min_rating: Minimum rating (0-5)
    - max_price: Maximum average price
    - skip: Pagination offset
    - limit: Number of results (max 100)
    """
    query = db.query(Restaurant).filter(Restaurant.is_active == True)
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    
    if min_rating is not None:
        query = query.filter(Restaurant.rating >= min_rating)
    
    if max_price is not None:
        query = query.filter(Restaurant.avg_price <= max_price)
    
    restaurants = query.offset(skip).limit(limit).all()
    
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific restaurant by ID.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    return restaurant


@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    restaurant: RestaurantCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new restaurant.
    Requires authentication. Admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create restaurants"
        )
    
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a restaurant.
    Requires authentication. Admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update restaurants"
        )
    
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not db_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    for key, value in restaurant.dict().items():
        setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a restaurant (soft delete by setting is_active to False).
    Requires authentication. Admin only.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete restaurants"
        )
    
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not db_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    db_restaurant.is_active = False
    db.commit()
    
    return None


@router.get("/search/by-name")
async def search_restaurants_by_name(
    q: str = Query(..., min_length=2, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Search restaurants by name.
    """
    restaurants = db.query(Restaurant).filter(
        Restaurant.name.ilike(f"%{q}%"),
        Restaurant.is_active == True
    ).limit(20).all()
    
    return {
        "query": q,
        "results": [
            {
                "id": r.id,
                "name": r.name,
                "city": r.city,
                "area": r.area,
                "cuisine": r.cuisine,
                "rating": r.rating,
                "avg_price": r.avg_price
            }
            for r in restaurants
        ]
    }


@router.get("/cities/list")
async def get_cities(db: Session = Depends(get_db)):
    """
    Get list of all cities with restaurant counts.
    """
    cities = db.query(
        Restaurant.city,
        db.func.count(Restaurant.id).label('count')
    ).filter(
        Restaurant.is_active == True
    ).group_by(
        Restaurant.city
    ).all()
    
    return {
        "cities": [
            {"name": city, "restaurant_count": count}
            for city, count in cities
        ]
    }


@router.get("/cuisines/list")
async def get_cuisines(db: Session = Depends(get_db)):
    """
    Get list of all cuisines with restaurant counts.
    """
    cuisines = db.query(
        Restaurant.cuisine,
        db.func.count(Restaurant.id).label('count')
    ).filter(
        Restaurant.is_active == True
    ).group_by(
        Restaurant.cuisine
    ).all()
    
    return {
        "cuisines": [
            {"name": cuisine, "restaurant_count": count}
            for cuisine, count in cuisines
        ]
    }
