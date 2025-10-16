/**
 * API Configuration and HTTP client for Nativore
 */
import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  signup: (data) => api.post('/api/auth/signup', data),
  login: (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  getProfile: () => api.get('/api/auth/me'),
  refreshToken: () => api.post('/api/auth/refresh'),
};

// Restaurants API
export const restaurantsAPI = {
  getAll: (params) => api.get('/api/restaurants/', { params }),
  getById: (id) => api.get(`/api/restaurants/${id}`),
  create: (data) => api.post('/api/restaurants/', data),
  update: (id, data) => api.put(`/api/restaurants/${id}`, data),
  delete: (id) => api.delete(`/api/restaurants/${id}`),
  search: (query) => api.get('/api/restaurants/search/by-name', { params: { q: query } }),
  getCities: () => api.get('/api/restaurants/cities/list'),
  getCuisines: () => api.get('/api/restaurants/cuisines/list'),
};

// Analytics API
export const analyticsAPI = {
  getTrends: (city) => api.get('/api/analytics/trends', { params: { city } }),
  getSpending: (city) => api.get('/api/analytics/spending', { params: { city } }),
  getTopCuisines: (city, limit = 10) => api.get('/api/analytics/top-cuisines', { params: { city, limit } }),
  getCityComparison: () => api.get('/api/analytics/city-comparison'),
  getTopRated: (city, limit = 10) => api.get('/api/analytics/top-rated', { params: { city, limit } }),
  getAreaInsights: (city) => api.get('/api/analytics/area-insights', { params: { city } }),
  getDashboardStats: () => api.get('/api/analytics/dashboard-stats'),
};

// Recommendations API
export const recommendationsAPI = {
  getBestLocations: (city, cuisine) => api.get('/api/recommendations/best-locations', { params: { city, cuisine } }),
  getMarketGaps: (city) => api.get('/api/recommendations/market-gaps', { params: { city } }),
  getSimilar: (restaurantId, limit = 5) => api.get('/api/recommendations/similar-restaurants', { params: { restaurant_id: restaurantId, limit } }),
  getInvestmentInsights: (city, budget) => api.get('/api/recommendations/investment-insights', { params: { city, budget } }),
};

export default api;
