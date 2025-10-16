#!/bin/bash

# Nativore Startup Script
echo "🚀 Starting Nativore Application..."

# Start backend
echo "📡 Starting backend server..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start frontend
echo "💻 Starting frontend development server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Nativore is running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Demo Credentials:"
echo "   Admin: admin@nativore.com / admin123"
echo "   User: demo@nativore.com / demo123"
echo ""
echo "Press Ctrl+C to stop both servers"

# Handle Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
