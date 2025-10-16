import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Navbar from './components/Navbar';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Insights from './pages/Insights';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Landing Page Component
const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-6xl font-display font-bold text-gray-900 mb-6">
            Welcome to <span className="text-primary-600">Nativore</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            AI-powered food market analytics platform for Tamil Nadu. 
            Discover trends, analyze consumer preferences, and make data-driven business decisions.
          </p>
          
          <div className="flex justify-center gap-4 mb-16">
            <a
              href="/signup"
              className="bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 transition transform hover:scale-105"
            >
              Get Started
            </a>
            <a
              href="/login"
              className="bg-white text-primary-600 border-2 border-primary-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-50 transition"
            >
              Login
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="p-6 bg-white rounded-xl shadow-lg">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-2">Market Analytics</h3>
              <p className="text-gray-600">
                Real-time insights on food trends across Tamil Nadu cities
              </p>
            </div>
            
            <div className="p-6 bg-white rounded-xl shadow-lg">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-2">Smart Recommendations</h3>
              <p className="text-gray-600">
                AI-powered location suggestions for new businesses
              </p>
            </div>
            
            <div className="p-6 bg-white rounded-xl shadow-lg">
              <div className="text-4xl mb-4">💡</div>
              <h3 className="text-xl font-bold mb-2">Market Gaps</h3>
              <p className="text-gray-600">
                Identify underserved areas and cuisine opportunities
              </p>
            </div>
          </div>

          <div className="mt-16 p-8 bg-blue-50 rounded-2xl">
            <h3 className="text-2xl font-bold mb-4">Covering Tamil Nadu Cities</h3>
            <div className="flex flex-wrap justify-center gap-4">
              {['Chennai', 'Coimbatore', 'Tiruppur', 'Madurai', 'Thoothukudi'].map((city) => (
                <span
                  key={city}
                  className="px-4 py-2 bg-white rounded-full text-primary-600 font-semibold shadow"
                >
                  {city}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="App min-h-screen">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/insights"
            element={
              <ProtectedRoute>
                <Insights />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  );
}

export default App;
