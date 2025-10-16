# 🍽️ Nativore - AI-Powered Food Market Analytics Platform

<div align="center">

**Tamil Nadu Food Industry Intelligence & Location Analytics**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=flat&logo=react)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat)](https://www.sqlalchemy.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4.1-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-api-endpoints) • [🎯 Features](#-features) • [💻 Demo](#-demo-credentials)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 📋 Overview

Nativore is a **production-grade web application** that helps food investors and entrepreneurs discover location-based food trends, analyze consumer taste preferences, spending patterns, and get data-driven recommendations for new business locations across Tamil Nadu.

### 🎯 Target Cities
- Chennai
- Coimbatore  
- Tiruppur
- Madurai
- Thoothukudi

### 📸 Screenshots

<div align="center">

![Nativore Dashboard](https://via.placeholder.com/800x400/f58700/ffffff?text=Nativore+Dashboard)

*Interactive Analytics Dashboard with City-based Food Trends*

</div>

## ✨ Features

### 🔐 Authentication System
- JWT-based secure authentication
- User registration and login
- Session management with token refresh

### 📊 Analytics Dashboard
- **City-based Trends**: Real-time food trend analysis per city
- **Spending Insights**: Average spending patterns and price analytics
- **Top Cuisines**: Popular cuisine rankings with visual charts
- **Area Analysis**: Locality-wise business opportunities

### 🎨 Interactive Visualizations
- 3D animated charts using React Three Fiber
- Responsive bar charts and pie charts (Recharts)
- Smooth animations with Framer Motion
- Real-time data filtering by city

### 🗺️ Location Intelligence
- 150+ restaurants across 5 Tamil Nadu cities
- Cuisine diversity: South Indian, North Indian, Chinese, Continental, etc.
- Area-specific insights with coordinates
- Business location recommendations

### 💡 Recommendation Engine
- Best locations for new ventures
- Cuisine gap analysis
- Market saturation indicators
- Investment opportunity scoring

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.6
- **Database**: SQLAlchemy 2.0.36 (SQLite/PostgreSQL)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Data Generation**: Faker 33.3.0
- **Server**: Uvicorn 0.34.0

### Frontend
- **Framework**: React 18.3.1
- **Build Tool**: Vite 5.4.20
- **Styling**: Tailwind CSS 3.4.1
- **3D Graphics**: React Three Fiber 8.18.11
- **Charts**: Recharts 2.15.0
- **Animations**: Framer Motion 11.15.0
- **HTTP Client**: Axios 1.7.9
- **Routing**: React Router DOM 7.1.3

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hariprasath1x/Nativore.git
cd Nativore
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
# Already created: backend/.env
# Contains: DATABASE_URL, JWT_SECRET, ALLOWED_ORIGINS
```

4. **Initialize Database**
```bash
# Create tables
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Load demo data (150 restaurants, 5 users, 800 reviews)
python utils/data_loader.py
```

5. **Frontend Setup**
```bash
cd ../frontend
npm install
```

### Running the Application

#### Option 1: Using the startup script (Recommended)
```bash
# From project root
./start.sh
```

#### Option 2: Manual start
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 🔐 Demo Credentials

```
Admin Account:
Email: admin@nativore.com
Password: admin123

User Account:
Email: demo@nativore.com  
Password: demo123
```

## 📂 Project Structure

```
nativore/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py            # SQLAlchemy configuration
│   ├── models.py              # Database models & schemas
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── routes/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── analytics.py      # Analytics & insights
│   │   ├── restaurants.py    # Restaurant CRUD
│   │   └── recommendations.py # Business recommendations
│   └── utils/
│       ├── fake_data.py      # Tamil Nadu data generator
│       └── data_loader.py    # Database initialization
├── frontend/
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # Tailwind setup
│   ├── package.json          # Node dependencies
│   ├── public/
│   │   └── index.html        # HTML template
│   └── src/
│       ├── App.jsx           # Main React component
│       ├── index.jsx         # Entry point
│       ├── api/
│       │   └── api.js        # Axios instance
│       ├── components/
│       │   ├── Navbar.jsx    # Navigation
│       │   ├── CitySelector.jsx
│       │   ├── Card.jsx
│       │   └── Chart3D.jsx   # 3D visualizations
│       └── pages/
│           ├── Login.jsx
│           ├── Signup.jsx
│           ├── Dashboard.jsx
│           └── Insights.jsx
├── database/
│   └── schema.sql            # PostgreSQL schema
├── docker-compose.yml        # Docker deployment
└── start.sh                  # Startup script
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/verify` - Token verification

### Analytics  
- `GET /analytics/trends` - City-based food trends
- `GET /analytics/spending` - Spending patterns
- `GET /analytics/top_cuisines` - Popular cuisines
- `GET /analytics/area_insights` - Area-wise analysis

### Restaurants
- `GET /restaurants/` - List restaurants
- `GET /restaurants/{id}` - Get restaurant details
- `POST /restaurants/` - Create restaurant (admin)
- `PUT /restaurants/{id}` - Update restaurant (admin)
- `DELETE /restaurants/{id}` - Delete restaurant (admin)

### Recommendations
- `GET /recommendations/locations` - Best business locations
- `GET /recommendations/business` - Business opportunities

## 📊 Database Schema

### Users
- id, email, username, hashed_password, full_name, role, created_at

### Restaurants  
- id, name, city, area, cuisine, avg_price, rating, review_count
- latitude, longitude, spending_index, description, phone, address

### Reviews
- id, user_id, restaurant_id, rating, comment, created_at

## 🐳 Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Services:
# - PostgreSQL: localhost:5432
# - Backend: localhost:8000  
# - Frontend: localhost:3000
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test
```

## 📈 Data Insights

The platform includes:
- **150 Restaurants** across 5 cities
- **15 Cuisine Types**: South Indian, North Indian, Chinese, Continental, Seafood, etc.
- **800+ Reviews** with ratings and comments
- **50+ Localities** with geographic coordinates
- **Real Tamil Dish Names**: Idli, Dosa, Chettinad Chicken, Kongunadu Mutton, etc.

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=sqlite:///./nativore.db
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (vite.config.js)
```javascript
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

## 🌟 Key Highlights

✅ **Production-Ready**: Complete authentication, error handling, CORS configuration  
✅ **Modern Stack**: Latest versions of FastAPI, React, Vite  
✅ **Real Tamil Nadu Data**: Authentic restaurant names, localities, cuisines  
✅ **Interactive UI**: 3D charts, smooth animations, responsive design  
✅ **Comprehensive API**: RESTful endpoints with auto-generated documentation  
✅ **Database Seeded**: 150 restaurants, 800 reviews ready to explore  
✅ **Docker Ready**: One-command deployment with docker-compose  

## 📝 Development Notes

- Built with Python 3.13 compatibility
- Uses SQLite for development (easy migration to PostgreSQL)
- JWT tokens expire in 30 minutes
- CORS configured for local development
- Hot reload enabled for both frontend and backend

## 🐛 Troubleshooting

### Port already in use
```bash
# Find process on port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Database errors
```bash
# Reset database
rm backend/nativore.db
# Reinitialize
python utils/data_loader.py
```

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Future Enhancements

- [ ] Machine Learning models for trend prediction
- [ ] Real-time data integration (Zomato/Swiggy APIs)
- [ ] PDF/Excel report generation
- [ ] Heat maps with geographic visualization
- [ ] WhatsApp/Email notification system
- [ ] Multi-language support (Tamil, English)
- [ ] Mobile app (React Native)
- [ ] Advanced filtering and search
- [ ] User review and rating system
- [ ] Admin dashboard for data management

## 👨‍💻 Developer

**Harith Chandrasekaran**  
B.Tech – Artificial Intelligence and Data Science  
3rd Year Student  
Sona Institute of Engineering and Technology

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for educational and portfolio use. All data used is ethically sourced and generated using the Faker library.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub: [github.com/Hariprasath1x/Nativore/issues](https://github.com/Hariprasath1x/Nativore/issues)
- Contact: hariprasathc@example.com

---

<div align="center">

**⭐ If you found this project helpful, please star it! ⭐**

Built with ❤️ for the Tamil Nadu food industry

</div>

