"""
Fake data generator for Tamil Nadu restaurants.
Generates realistic restaurant data for Chennai, Coimbatore, Tiruppur, Madurai, Thoothukudi.
"""
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')  # Indian locale for realistic Indian names

# Tamil Nadu Cities
CITIES = {
    "Chennai": {
        "areas": [
            "T. Nagar", "Anna Nagar", "Velachery", "Adyar", "Mylapore",
            "Porur", "Tambaram", "OMR", "ECR", "Nungambakkam",
            "Besant Nagar", "Alwarpet", "Chrompet", "Guindy"
        ],
        "coords": (13.0827, 80.2707)
    },
    "Coimbatore": {
        "areas": [
            "RS Puram", "Saibaba Colony", "Gandhipuram", "Peelamedu", "Singanallur",
            "Saravanampatti", "Vadavalli", "Race Course", "Town Hall", "Ukkadam"
        ],
        "coords": (11.0168, 76.9558)
    },
    "Tiruppur": {
        "areas": [
            "Kumaran Road", "Avinashi Road", "Kangeyam Road", "Palladam Road",
            "Velampalayam", "Mannarai", "Chettipalayam", "Angeripalayam"
        ],
        "coords": (11.1085, 77.3411)
    },
    "Madurai": {
        "areas": [
            "Anna Nagar", "K. Pudur", "Goripalayam", "SS Colony", "Villapuram",
            "Narimedu", "Thirunagar", "Pasumalai", "Simmakkal", "Town Hall"
        ],
        "coords": (9.9252, 78.1198)
    },
    "Thoothukudi": {
        "areas": [
            "Palayamkottai Road", "Ettayapuram Road", "New Colony", "VOC Ground",
            "Millerpuram", "Muthialpet", "Caldwell Colony", "Jothi Nagar"
        ],
        "coords": (8.7642, 78.1348)
    }
}

# Cuisines popular in Tamil Nadu
CUISINES = [
    "South Indian",
    "North Indian", 
    "Chinese",
    "Chettinad",
    "Tamil Vegetarian",
    "Continental",
    "Multi-Cuisine",
    "Seafood",
    "Biryani Specialist",
    "Street Food",
    "Fast Food",
    "Kerala",
    "Andhra",
    "Italian",
    "Café"
]

# Restaurant name prefixes and suffixes
NAME_PREFIXES = [
    "Saravana", "Annapoorna", "Arya", "Sangeetha", "Hotel", "The", "Sri",
    "Anjappar", "Ambur", "Junior", "Ponnusamy", "Amma", "Royal", "Grand",
    "Paradise", "Star", "Raj", "Kumarakom", "Madurai", "Coimbatore"
]

NAME_SUFFIXES = [
    "Bhavan", "Hotel", "Restaurant", "Mess", "Kitchen", "Palace", "Corner",
    "Foods", "Biriyani", "Café", "Grill", "Express", "Delights", "Paradise",
    "Center", "House", "Garden", "Spice", "Curry", "Dosa"
]

# Popular dishes for descriptions
DISHES = [
    "masala dosa", "biryani", "chettinad chicken", "fish curry", "parotta",
    "idli", "vada", "sambar", "rasam", "pongal", "uttapam", "kothu parotta",
    "mutton chukka", "chicken 65", "gobi manchurian", "fried rice", "noodles"
]


def generate_restaurant_name():
    """Generate realistic Tamil Nadu restaurant name."""
    if random.random() < 0.3:
        # Just use suffix
        return f"{random.choice(NAME_SUFFIXES)} {random.choice(NAME_PREFIXES)}"
    else:
        return f"{random.choice(NAME_PREFIXES)} {random.choice(NAME_SUFFIXES)}"


def generate_description(cuisine, city):
    """Generate restaurant description."""
    templates = [
        f"Authentic {cuisine} restaurant in {city}. Famous for our {random.choice(DISHES)}.",
        f"Experience the best {cuisine} cuisine in {city}. Specializing in {random.choice(DISHES)} and {random.choice(DISHES)}.",
        f"Family-friendly {cuisine} restaurant serving delicious {random.choice(DISHES)} since {random.randint(1990, 2020)}.",
        f"Premium {cuisine} dining experience. Must try our signature {random.choice(DISHES)}.",
        f"Traditional {cuisine} flavors with modern presentation. Popular for {random.choice(DISHES)}."
    ]
    return random.choice(templates)


def generate_phone():
    """Generate Indian phone number."""
    return f"+91 {random.randint(90000, 99999)} {random.randint(10000, 99999)}"


def generate_restaurants(count=100):
    """
    Generate fake restaurant data.
    
    Args:
        count: Number of restaurants to generate
        
    Returns:
        List of restaurant dictionaries
    """
    restaurants = []
    
    for _ in range(count):
        city = random.choice(list(CITIES.keys()))
        city_data = CITIES[city]
        area = random.choice(city_data["areas"])
        cuisine = random.choice(CUISINES)
        
        # Generate coordinates near city center
        base_lat, base_lng = city_data["coords"]
        lat = base_lat + random.uniform(-0.05, 0.05)
        lng = base_lng + random.uniform(-0.05, 0.05)
        
        # Average price for two (in INR)
        avg_price = random.choice([
            random.randint(150, 300),    # Budget
            random.randint(300, 600),    # Mid-range
            random.randint(600, 1500),   # Premium
        ])
        
        # Rating (0-5)
        rating = round(random.uniform(2.5, 5.0), 1)
        
        # Review count (more reviews for higher ratings)
        review_count = random.randint(
            int(rating * 50), 
            int(rating * 200)
        )
        
        # Spending index (economic indicator)
        spending_index = round(random.uniform(0.5, 2.5), 2)
        
        restaurant = {
            "name": generate_restaurant_name(),
            "city": city,
            "area": area,
            "cuisine": cuisine,
            "avg_price": avg_price,
            "rating": rating,
            "review_count": review_count,
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "spending_index": spending_index,
            "description": generate_description(cuisine, city),
            "phone": generate_phone(),
            "address": f"{random.randint(1, 999)}, {area}, {city}, Tamil Nadu",
            "image_url": f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600",
            "is_active": True
        }
        
        restaurants.append(restaurant)
    
    return restaurants


def generate_reviews(users, restaurants, count=500):
    """
    Generate fake reviews.
    
    Args:
        users: List of user IDs
        restaurants: List of restaurant IDs
        count: Number of reviews to generate
        
    Returns:
        List of review dictionaries
    """
    reviews = []
    
    review_comments = [
        "Amazing food! Must visit.",
        "Great taste and ambiance. Highly recommended.",
        "Good food but service could be better.",
        "Excellent! Will come again.",
        "Loved the authentic flavors.",
        "Bit overpriced but food quality is top-notch.",
        "Perfect place for family dinners.",
        "Quick service and delicious food.",
        "One of the best in the city!",
        "Average experience. Nothing special.",
        "Outstanding! The biryani was incredible.",
        "Friendly staff and great food.",
        "Could be better. Food was cold.",
        "Absolutely loved it! 5 stars!",
        "Decent food at reasonable prices.",
    ]
    
    for _ in range(count):
        rating = round(random.uniform(1, 5), 1)
        
        review = {
            "user_id": random.choice(users),
            "restaurant_id": random.choice(restaurants),
            "rating": rating,
            "comment": random.choice(review_comments) if random.random() > 0.3 else None,
        }
        
        reviews.append(review)
    
    return reviews


if __name__ == "__main__":
    # Generate sample data
    restaurants = generate_restaurants(100)
    print(f"Generated {len(restaurants)} restaurants")
    
    # Print sample
    for i, r in enumerate(restaurants[:3], 1):
        print(f"\n{i}. {r['name']} - {r['city']}")
        print(f"   Cuisine: {r['cuisine']}, Price: ₹{r['avg_price']}, Rating: {r['rating']}")
