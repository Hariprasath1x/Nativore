"""
Recommendation routes for Nativore platform.
AI-powered location and business recommendations.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from database import get_db
from models import Restaurant, User
from routes.auth import get_current_active_user

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/best-locations")
async def get_best_locations(
    city: str = Query(..., description="City name"),
    cuisine: Optional[str] = Query(None, description="Cuisine type"),
    db: Session = Depends(get_db)
):
    """
    Get best locations for opening a new restaurant.
    
    Analyzes:
    - Competition density
    - Average ratings
    - Spending index
    - Gap analysis for underserved areas
    """
    # Get all areas in the city
    query = db.query(
        Restaurant.area,
        func.count(Restaurant.id).label('restaurant_count'),
        func.avg(Restaurant.rating).label('avg_rating'),
        func.avg(Restaurant.avg_price).label('avg_price'),
        func.avg(Restaurant.spending_index).label('avg_spending_index')
    ).filter(Restaurant.city == city)
    
    if cuisine:
        query = query.filter(Restaurant.cuisine == cuisine)
    
    areas = query.group_by(Restaurant.area).all()
    
    recommendations = []
    
    for area in areas:
        # Calculate opportunity score
        # Lower competition + higher spending = better opportunity
        competition_factor = max(0, 10 - area.restaurant_count)
        spending_factor = area.avg_spending_index * 3
        rating_factor = area.avg_rating
        
        opportunity_score = (competition_factor + spending_factor + rating_factor) / 3
        
        recommendations.append({
            "area": area.area,
            "city": city,
            "current_restaurants": area.restaurant_count,
            "avg_rating": round(area.avg_rating, 2),
            "avg_price": round(area.avg_price, 2),
            "spending_index": round(area.avg_spending_index, 2),
            "opportunity_score": round(opportunity_score, 2),
            "recommendation": get_recommendation_text(opportunity_score, area.restaurant_count)
        })
    
    # Sort by opportunity score
    recommendations.sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    return {
        "city": city,
        "cuisine": cuisine or "All",
        "top_locations": recommendations[:10],
        "analysis_summary": {
            "total_areas_analyzed": len(areas),
            "best_opportunity": recommendations[0]["area"] if recommendations else None,
            "highest_competition": max(areas, key=lambda x: x.restaurant_count).area if areas else None
        }
    }


@router.get("/market-gaps")
async def find_market_gaps(
    city: str = Query(..., description="City name"),
    db: Session = Depends(get_db)
):
    """
    Identify underserved cuisines and areas.
    
    Helps entrepreneurs find market gaps and opportunities.
    """
    # Get all cuisines in the city
    cuisine_distribution = db.query(
        Restaurant.cuisine,
        func.count(Restaurant.id).label('count')
    ).filter(
        Restaurant.city == city
    ).group_by(
        Restaurant.cuisine
    ).all()
    
    total_restaurants = sum(c.count for c in cuisine_distribution)
    
    # Calculate market saturation
    cuisine_analysis = []
    for cuisine in cuisine_distribution:
        market_share = (cuisine.count / total_restaurants) * 100
        saturation = "High" if market_share > 20 else "Medium" if market_share > 10 else "Low"
        
        cuisine_analysis.append({
            "cuisine": cuisine.cuisine,
            "restaurant_count": cuisine.count,
            "market_share": round(market_share, 2),
            "saturation": saturation,
            "opportunity": "Low" if saturation == "High" else "Medium" if saturation == "Medium" else "High"
        })
    
    # Sort by opportunity (low count = high opportunity)
    cuisine_analysis.sort(key=lambda x: x["restaurant_count"])
    
    # Area analysis
    area_gaps = db.query(
        Restaurant.area,
        func.count(func.distinct(Restaurant.cuisine)).label('cuisine_variety'),
        func.count(Restaurant.id).label('restaurant_count')
    ).filter(
        Restaurant.city == city
    ).group_by(
        Restaurant.area
    ).having(
        func.count(Restaurant.id) < 5  # Areas with low competition
    ).all()
    
    underserved_areas = [
        {
            "area": area.area,
            "restaurant_count": area.restaurant_count,
            "cuisine_variety": area.cuisine_variety,
            "opportunity": "High" if area.restaurant_count < 3 else "Medium"
        }
        for area in area_gaps
    ]
    
    return {
        "city": city,
        "cuisine_opportunities": cuisine_analysis[:5],
        "underserved_areas": underserved_areas[:10],
        "summary": {
            "total_cuisines": len(cuisine_analysis),
            "high_opportunity_cuisines": len([c for c in cuisine_analysis if c["opportunity"] == "High"]),
            "underserved_areas_count": len(underserved_areas)
        }
    }


@router.get("/similar-restaurants")
async def get_similar_restaurants(
    restaurant_id: int = Query(..., description="Restaurant ID"),
    limit: int = Query(5, ge=1, le=20, description="Number of similar restaurants"),
    db: Session = Depends(get_db)
):
    """
    Find similar restaurants based on cuisine, price, and location.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        return {"error": "Restaurant not found"}
    
    # Find similar restaurants
    similar = db.query(Restaurant).filter(
        Restaurant.id != restaurant_id,
        Restaurant.cuisine == restaurant.cuisine,
        Restaurant.city == restaurant.city,
        Restaurant.is_active == True
    ).all()
    
    # Score by price similarity and rating
    scored_restaurants = []
    for rest in similar:
        price_diff = abs(rest.avg_price - restaurant.avg_price)
        price_score = max(0, 100 - (price_diff / 10))
        rating_score = rest.rating * 20
        
        total_score = (price_score + rating_score) / 2
        
        scored_restaurants.append({
            "restaurant": rest,
            "similarity_score": round(total_score, 2)
        })
    
    # Sort by score
    scored_restaurants.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return {
        "reference_restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "cuisine": restaurant.cuisine,
            "city": restaurant.city,
            "avg_price": restaurant.avg_price
        },
        "similar_restaurants": [
            {
                "id": item["restaurant"].id,
                "name": item["restaurant"].name,
                "area": item["restaurant"].area,
                "rating": item["restaurant"].rating,
                "avg_price": item["restaurant"].avg_price,
                "similarity_score": item["similarity_score"]
            }
            for item in scored_restaurants[:limit]
        ]
    }


@router.get("/investment-insights")
async def get_investment_insights(
    city: str = Query(..., description="City name"),
    budget: float = Query(..., gt=0, description="Investment budget in INR"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get investment insights and ROI predictions.
    Requires authentication.
    """
    # Analyze market conditions
    restaurants = db.query(Restaurant).filter(Restaurant.city == city).all()
    
    if not restaurants:
        return {"error": f"No data available for {city}"}
    
    # Calculate market metrics
    avg_price = sum(r.avg_price for r in restaurants) / len(restaurants)
    avg_rating = sum(r.rating for r in restaurants) / len(restaurants)
    avg_spending = sum(r.spending_index for r in restaurants) / len(restaurants)
    
    # Budget categorization
    if budget < 1000000:  # < 10 lakhs
        category = "Small Scale"
        suggested_type = "Cloud Kitchen / Street Food"
    elif budget < 5000000:  # 10-50 lakhs
        category = "Medium Scale"
        suggested_type = "Casual Dining / Quick Service"
    else:  # > 50 lakhs
        category = "Large Scale"
        suggested_type = "Fine Dining / Multi-Cuisine"
    
    # ROI estimation (simplified)
    estimated_monthly_revenue = budget * 0.05  # 5% of budget
    estimated_profit_margin = 0.15  # 15%
    estimated_monthly_profit = estimated_monthly_revenue * estimated_profit_margin
    breakeven_months = round(budget / estimated_monthly_profit) if estimated_monthly_profit > 0 else 0
    
    return {
        "city": city,
        "budget": budget,
        "investment_category": category,
        "suggested_business_type": suggested_type,
        "market_analysis": {
            "avg_price_point": round(avg_price, 2),
            "avg_market_rating": round(avg_rating, 2),
            "spending_index": round(avg_spending, 2),
            "competition_level": "High" if len(restaurants) > 100 else "Medium" if len(restaurants) > 50 else "Low"
        },
        "roi_projection": {
            "estimated_monthly_revenue": round(estimated_monthly_revenue, 2),
            "estimated_profit_margin": f"{int(estimated_profit_margin * 100)}%",
            "estimated_monthly_profit": round(estimated_monthly_profit, 2),
            "breakeven_period_months": breakeven_months,
            "note": "These are rough estimates based on market averages"
        }
    }


def get_recommendation_text(score: float, competition: int) -> str:
    """Generate recommendation text based on score."""
    if score > 8:
        return "Excellent opportunity! High demand with manageable competition."
    elif score > 6:
        return "Good potential. Consider entering this market."
    elif score > 4:
        return "Moderate opportunity. Requires differentiation strategy."
    else:
        return "High competition. Challenging market conditions."
