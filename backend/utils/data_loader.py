"""
Data loader utility for Nativore.
Loads restaurant and user data into the database.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from models import User, Restaurant, Review
from utils.fake_data import generate_restaurants, generate_reviews
from database import SessionLocal, init_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_demo_users(db: Session):
    """Create demo users for testing."""
    demo_users = [
        {
            "email": "admin@nativore.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "role": "admin"
        },
        {
            "email": "demo@nativore.com",
            "username": "demo",
            "password": "demo123",
            "full_name": "Demo User",
            "role": "user"
        },
        {
            "email": "user1@example.com",
            "username": "foodlover",
            "password": "password123",
            "full_name": "Food Lover",
            "role": "user"
        },
        {
            "email": "user2@example.com",
            "username": "chennaiexplorer",
            "password": "password123",
            "full_name": "Chennai Explorer",
            "role": "user"
        },
        {
            "email": "user3@example.com",
            "username": "coimbatorefoodie",
            "password": "password123",
            "full_name": "Coimbatore Foodie",
            "role": "user"
        }
    ]
    
    created_users = []
    for user_data in demo_users:
        # Check if user exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing_user:
            hashed_password = pwd_context.hash(user_data["password"])
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=hashed_password,
                full_name=user_data["full_name"],
                role=user_data["role"]
            )
            db.add(user)
            created_users.append(user)
    
    db.commit()
    
    # Refresh to get IDs
    for user in created_users:
        db.refresh(user)
    
    print(f"✅ Created {len(created_users)} demo users")
    return created_users


def load_restaurants(db: Session, count=100):
    """Load fake restaurant data into database."""
    # Generate restaurants
    restaurants_data = generate_restaurants(count)
    
    created_restaurants = []
    for rest_data in restaurants_data:
        restaurant = Restaurant(**rest_data)
        db.add(restaurant)
        created_restaurants.append(restaurant)
    
    db.commit()
    
    # Refresh to get IDs
    for rest in created_restaurants:
        db.refresh(rest)
    
    print(f"✅ Loaded {len(created_restaurants)} restaurants")
    return created_restaurants


def load_reviews(db: Session, user_ids, restaurant_ids, count=500):
    """Load fake reviews into database."""
    # Generate reviews
    reviews_data = generate_reviews(user_ids, restaurant_ids, count)
    
    created_reviews = []
    for review_data in reviews_data:
        review = Review(**review_data)
        db.add(review)
        created_reviews.append(review)
    
    db.commit()
    
    # Update restaurant ratings and review counts
    for rest_id in restaurant_ids:
        restaurant = db.query(Restaurant).filter(Restaurant.id == rest_id).first()
        if restaurant:
            reviews = db.query(Review).filter(Review.restaurant_id == rest_id).all()
            if reviews:
                avg_rating = sum(r.rating for r in reviews) / len(reviews)
                restaurant.rating = round(avg_rating, 1)
                restaurant.review_count = len(reviews)
    
    db.commit()
    
    print(f"✅ Loaded {len(created_reviews)} reviews")
    return created_reviews


def initialize_data():
    """Initialize database with demo data."""
    print("🚀 Initializing Nativore database...")
    
    # Initialize database tables
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        existing_restaurants = db.query(Restaurant).count()
        
        if existing_users > 0 or existing_restaurants > 0:
            print(f"⚠️  Database already has data ({existing_users} users, {existing_restaurants} restaurants)")
            response = input("Do you want to clear and reload? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Data loading cancelled")
                return
            
            # Clear existing data
            db.query(Review).delete()
            db.query(Restaurant).delete()
            db.query(User).delete()
            db.commit()
            print("🗑️  Cleared existing data")
        
        # Create demo users
        users = create_demo_users(db)
        user_ids = [u.id for u in users]
        
        # Load restaurants
        restaurants = load_restaurants(db, count=150)  # Load 150 restaurants
        restaurant_ids = [r.id for r in restaurants]
        
        # Load reviews
        reviews = load_reviews(db, user_ids, restaurant_ids, count=800)  # Load 800 reviews
        
        print("\n✅ Database initialization complete!")
        print(f"   👥 Users: {len(users)}")
        print(f"   🍽️  Restaurants: {len(restaurants)}")
        print(f"   ⭐ Reviews: {len(reviews)}")
        print("\n🔐 Demo Credentials:")
        print("   Admin: admin / admin123")
        print("   User: demo / demo123")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    initialize_data()
