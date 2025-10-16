import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Card from '../components/Card';
import CitySelector from '../components/CitySelector';
import { analyticsAPI } from '../api/api';
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [selectedCity, setSelectedCity] = useState('');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [trends, setTrends] = useState(null);
  const [spending, setSpending] = useState(null);
  const [loading, setLoading] = useState(true);

  const COLORS = ['#f58700', '#00af73', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    if (dashboardStats) {
      fetchCityData();
    }
  }, [selectedCity]);

  const fetchDashboardData = async () => {
    try {
      const response = await analyticsAPI.getDashboardStats();
      setDashboardStats(response.data);
      await fetchCityData();
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const fetchCityData = async () => {
    try {
      const [trendsRes, spendingRes] = await Promise.all([
        analyticsAPI.getTrends(selectedCity),
        analyticsAPI.getSpending(selectedCity),
      ]);
      setTrends(trendsRes.data);
      setSpending(spendingRes.data);
    } catch (error) {
      console.error('Error fetching city data:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-2">
            Dashboard
          </h1>
          <p className="text-gray-600">
            Tamil Nadu Food Market Analytics
          </p>
        </motion.div>

        <CitySelector selectedCity={selectedCity} onCityChange={setSelectedCity} />

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card
            title="Total Restaurants"
            value={dashboardStats?.overview?.total_restaurants || 0}
            icon="🍽️"
            color="primary"
          />
          <Card
            title="Total Reviews"
            value={dashboardStats?.overview?.total_reviews || 0}
            icon="⭐"
            color="secondary"
          />
          <Card
            title="Avg Rating"
            value={dashboardStats?.overview?.avg_rating || 0}
            subtitle="Out of 5.0"
            icon="📊"
            color="blue"
          />
          <Card
            title="Avg Price"
            value={`₹${dashboardStats?.overview?.avg_price || 0}`}
            subtitle="For two people"
            icon="💰"
            color="green"
          />
        </div>

        {/* Cuisine Distribution */}
        {trends && trends.top_cuisines && trends.top_cuisines.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Top Cuisines - {trends.city}
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={trends.top_cuisines}
                    dataKey="count"
                    nameKey="cuisine"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={(entry) => `${entry.cuisine} (${entry.percentage}%)`}
                  >
                    {trends.top_cuisines.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>

              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={trends.top_cuisines}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="cuisine" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#f58700" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}

        {/* Spending Analysis */}
        {spending && spending.price_ranges && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Spending Distribution - {spending.city}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-4 bg-green-50 rounded-lg border-2 border-green-200">
                <h3 className="text-lg font-semibold text-green-800 mb-2">Budget</h3>
                <p className="text-sm text-green-600 mb-2">{spending.price_ranges.budget.range}</p>
                <p className="text-3xl font-bold text-green-700">
                  {spending.price_ranges.budget.percentage}%
                </p>
                <p className="text-sm text-green-600 mt-2">
                  Avg: ₹{spending.price_ranges.budget.avg_price}
                </p>
              </div>

              <div className="p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
                <h3 className="text-lg font-semibold text-blue-800 mb-2">Mid-Range</h3>
                <p className="text-sm text-blue-600 mb-2">{spending.price_ranges.mid_range.range}</p>
                <p className="text-3xl font-bold text-blue-700">
                  {spending.price_ranges.mid_range.percentage}%
                </p>
                <p className="text-sm text-blue-600 mt-2">
                  Avg: ₹{spending.price_ranges.mid_range.avg_price}
                </p>
              </div>

              <div className="p-4 bg-purple-50 rounded-lg border-2 border-purple-200">
                <h3 className="text-lg font-semibold text-purple-800 mb-2">Premium</h3>
                <p className="text-sm text-purple-600 mb-2">{spending.price_ranges.premium.range}</p>
                <p className="text-3xl font-bold text-purple-700">
                  {spending.price_ranges.premium.percentage}%
                </p>
                <p className="text-sm text-purple-600 mt-2">
                  Avg: ₹{spending.price_ranges.premium.avg_price}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
