"""
Analytics routes for Nativore platform.
Provides data insights on Tamil Nadu food market trends.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from database import get_db
from models import Restaurant, Review, User
from routes.auth import get_current_active_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/trends")
async def get_trends(
    city: Optional[str] = Query(None, description="Filter by city"),
    db: Session = Depends(get_db)
):
    """
    Get food trend analytics for Tamil Nadu cities.
    
    Returns:
    - Top cuisines by popularity
    - Average spending by city
    - Rating distribution
    - Growth trends
    """
    # Base query
    query = db.query(Restaurant)
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    restaurants = query.all()
    
    if not restaurants:
        return {
            "city": city or "All Cities",
            "total_restaurants": 0,
            "top_cuisines": [],
            "avg_price": 0,
            "avg_rating": 0
        }
    
    # Cuisine distribution
    cuisine_counts = {}
    total_price = 0
    total_rating = 0
    
    for rest in restaurants:
        cuisine_counts[rest.cuisine] = cuisine_counts.get(rest.cuisine, 0) + 1
        total_price += rest.avg_price
        total_rating += rest.rating
    
    # Sort cuisines by count
    top_cuisines = sorted(
        [{"cuisine": k, "count": v, "percentage": round(v/len(restaurants)*100, 1)} 
         for k, v in cuisine_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:10]
    
    return {
        "city": city or "All Cities",
        "total_restaurants": len(restaurants),
        "top_cuisines": top_cuisines,
        "avg_price": round(total_price / len(restaurants), 2),
        "avg_rating": round(total_rating / len(restaurants), 2)
    }


@router.get("/spending")
async def get_spending_analysis(
    city: Optional[str] = Query(None, description="Filter by city"),
    db: Session = Depends(get_db)
):
    """
    Get spending pattern analysis.
    
    Returns spending distribution across price ranges and cities.
    """
    query = db.query(Restaurant)
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    restaurants = query.all()
    
    # Price range categorization
    budget = []  # < 300
    mid_range = []  # 300-600
    premium = []  # > 600
    
    for rest in restaurants:
        if rest.avg_price < 300:
            budget.append(rest)
        elif rest.avg_price < 600:
            mid_range.append(rest)
        else:
            premium.append(rest)
    
    total = len(restaurants)
    
    return {
        "city": city or "All Cities",
        "total_restaurants": total,
        "price_ranges": {
            "budget": {
                "count": len(budget),
                "percentage": round(len(budget)/total*100, 1) if total > 0 else 0,
                "avg_price": round(sum(r.avg_price for r in budget)/len(budget), 2) if budget else 0,
                "range": "< ₹300"
            },
            "mid_range": {
                "count": len(mid_range),
                "percentage": round(len(mid_range)/total*100, 1) if total > 0 else 0,
                "avg_price": round(sum(r.avg_price for r in mid_range)/len(mid_range), 2) if mid_range else 0,
                "range": "₹300 - ₹600"
            },
            "premium": {
                "count": len(premium),
                "percentage": round(len(premium)/total*100, 1) if total > 0 else 0,
                "avg_price": round(sum(r.avg_price for r in premium)/len(premium), 2) if premium else 0,
                "range": "> ₹600"
            }
        },
        "avg_spending_index": round(sum(r.spending_index for r in restaurants)/total, 2) if total > 0 else 0
    }


@router.get("/top-cuisines")
async def get_top_cuisines(
    city: Optional[str] = Query(None, description="Filter by city"),
    limit: int = Query(10, description="Number of top cuisines to return"),
    db: Session = Depends(get_db)
):
    """
    Get top cuisines by rating and popularity.
    """
    query = db.query(
        Restaurant.cuisine,
        func.count(Restaurant.id).label('count'),
        func.avg(Restaurant.rating).label('avg_rating'),
        func.avg(Restaurant.avg_price).label('avg_price')
    ).group_by(Restaurant.cuisine)
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    results = query.order_by(desc('count')).limit(limit).all()
    
    top_cuisines = [
        {
            "cuisine": r.cuisine,
            "restaurant_count": r.count,
            "avg_rating": round(r.avg_rating, 2),
            "avg_price": round(r.avg_price, 2)
        }
        for r in results
    ]
    
    return {
        "city": city or "All Cities",
        "top_cuisines": top_cuisines
    }


@router.get("/city-comparison")
async def get_city_comparison(db: Session = Depends(get_db)):
    """
    Compare all Tamil Nadu cities in the platform.
    """
    cities_data = []
    
    cities = db.query(Restaurant.city).distinct().all()
    
    for (city,) in cities:
        city_restaurants = db.query(Restaurant).filter(Restaurant.city == city).all()
        
        if city_restaurants:
            cities_data.append({
                "city": city,
                "total_restaurants": len(city_restaurants),
                "avg_rating": round(sum(r.rating for r in city_restaurants) / len(city_restaurants), 2),
                "avg_price": round(sum(r.avg_price for r in city_restaurants) / len(city_restaurants), 2),
                "spending_index": round(sum(r.spending_index for r in city_restaurants) / len(city_restaurants), 2),
                "top_cuisine": max(set([r.cuisine for r in city_restaurants]), 
                                 key=[r.cuisine for r in city_restaurants].count)
            })
    
    # Sort by restaurant count
    cities_data.sort(key=lambda x: x["total_restaurants"], reverse=True)
    
    return {
        "cities": cities_data,
        "total_cities": len(cities_data)
    }


@router.get("/top-rated")
async def get_top_rated_restaurants(
    city: Optional[str] = Query(None, description="Filter by city"),
    limit: int = Query(10, description="Number of restaurants to return"),
    db: Session = Depends(get_db)
):
    """
    Get top-rated restaurants.
    """
    query = db.query(Restaurant).filter(Restaurant.review_count > 0)
    
    if city:
        query = query.filter(Restaurant.city == city)
    
    restaurants = query.order_by(
        desc(Restaurant.rating),
        desc(Restaurant.review_count)
    ).limit(limit).all()
    
    return {
        "city": city or "All Cities",
        "top_rated": [
            {
                "id": r.id,
                "name": r.name,
                "city": r.city,
                "area": r.area,
                "cuisine": r.cuisine,
                "rating": r.rating,
                "review_count": r.review_count,
                "avg_price": r.avg_price
            }
            for r in restaurants
        ]
    }


@router.get("/area-insights")
async def get_area_insights(
    city: str = Query(..., description="City name"),
    db: Session = Depends(get_db)
):
    """
    Get insights for different areas within a city.
    Helps identify high-demand localities.
    """
    areas = db.query(
        Restaurant.area,
        func.count(Restaurant.id).label('count'),
        func.avg(Restaurant.rating).label('avg_rating'),
        func.avg(Restaurant.avg_price).label('avg_price'),
        func.avg(Restaurant.spending_index).label('avg_spending_index')
    ).filter(
        Restaurant.city == city
    ).group_by(
        Restaurant.area
    ).order_by(
        desc('count')
    ).all()
    
    area_data = [
        {
            "area": a.area,
            "restaurant_count": a.count,
            "avg_rating": round(a.avg_rating, 2),
            "avg_price": round(a.avg_price, 2),
            "spending_index": round(a.avg_spending_index, 2),
            "demand_score": round(a.count * a.avg_rating * a.avg_spending_index, 2)
        }
        for a in areas
    ]
    
    # Sort by demand score
    area_data.sort(key=lambda x: x["demand_score"], reverse=True)
    
    return {
        "city": city,
        "areas": area_data,
        "total_areas": len(area_data)
    }


@router.get("/dashboard-stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard statistics.
    Requires authentication.
    """
    total_restaurants = db.query(Restaurant).count()
    total_reviews = db.query(Review).count()
    total_cities = db.query(Restaurant.city).distinct().count()
    
    avg_rating = db.query(func.avg(Restaurant.rating)).scalar() or 0
    avg_price = db.query(func.avg(Restaurant.avg_price)).scalar() or 0
    
    # Top cuisine
    top_cuisine = db.query(
        Restaurant.cuisine,
        func.count(Restaurant.id).label('count')
    ).group_by(Restaurant.cuisine).order_by(desc('count')).first()
    
    # Most reviewed restaurant
    most_reviewed = db.query(Restaurant).order_by(desc(Restaurant.review_count)).first()
    
    return {
        "overview": {
            "total_restaurants": total_restaurants,
            "total_reviews": total_reviews,
            "total_cities": total_cities,
            "avg_rating": round(avg_rating, 2),
            "avg_price": round(avg_price, 2)
        },
        "top_cuisine": top_cuisine.cuisine if top_cuisine else "N/A",
        "most_reviewed_restaurant": {
            "name": most_reviewed.name,
            "city": most_reviewed.city,
            "review_count": most_reviewed.review_count,
            "rating": most_reviewed.rating
        } if most_reviewed else None,
        "user": {
            "username": current_user.username,
            "role": current_user.role
        }
    }
