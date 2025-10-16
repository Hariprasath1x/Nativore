import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiTrendingUp, FiMapPin, FiDollarSign } from 'react-icons/fi';
import { analyticsAPI, recommendationsAPI } from '../api/api';
import CitySelector from '../components/CitySelector';
import Chart3D from '../components/Chart3D';
import { toast } from 'react-toastify';

const Insights = () => {
  const [selectedCity, setSelectedCity] = useState('Chennai');
  const [cityComparison, setCityComparison] = useState(null);
  const [areaInsights, setAreaInsights] = useState(null);
  const [marketGaps, setMarketGaps] = useState(null);
  const [bestLocations, setBestLocations] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllInsights();
  }, [selectedCity]);

  const fetchAllInsights = async () => {
    setLoading(true);
    try {
      const [comparisonRes, gapsRes] = await Promise.all([
        analyticsAPI.getCityComparison(),
        recommendationsAPI.getMarketGaps(selectedCity),
      ]);

      setCityComparison(comparisonRes.data);
      setMarketGaps(gapsRes.data);

      // Fetch area insights only if city is selected
      if (selectedCity) {
        const [areaRes, locationsRes] = await Promise.all([
          analyticsAPI.getAreaInsights(selectedCity),
          recommendationsAPI.getBestLocations(selectedCity),
        ]);
        setAreaInsights(areaRes.data);
        setBestLocations(locationsRes.data);
      }
    } catch (error) {
      console.error('Error fetching insights:', error);
      toast.error('Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading insights...</p>
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
            Market Insights
          </h1>
          <p className="text-gray-600">
            AI-powered analytics and business recommendations
          </p>
        </motion.div>

        <CitySelector
          selectedCity={selectedCity}
          onCityChange={setSelectedCity}
          cities={cityComparison?.cities?.map(c => c.city) || []}
        />

        {/* 3D Visualization */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl shadow-2xl mb-8 overflow-hidden"
        >
          <Chart3D />
        </motion.div>

        {/* City Comparison */}
        {cityComparison && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <FiTrendingUp className="mr-2 text-primary-600" />
              City Comparison
            </h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">City</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Restaurants</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Rating</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Avg Price</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Top Cuisine</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {cityComparison.cities.map((city, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap font-semibold">{city.city}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{city.total_restaurants}</td>
                      <td className="px-6 py-4 whitespace-nowrap">⭐ {city.avg_rating}</td>
                      <td className="px-6 py-4 whitespace-nowrap">₹{city.avg_price}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{city.top_cuisine}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}

        {/* Best Locations */}
        {bestLocations && bestLocations.top_locations && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <FiMapPin className="mr-2 text-primary-600" />
              Best Locations for New Business - {selectedCity}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {bestLocations.top_locations.slice(0, 6).map((location, index) => (
                <div
                  key={index}
                  className="p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 transition"
                >
                  <h3 className="font-bold text-lg mb-2">{location.area}</h3>
                  <div className="space-y-1 text-sm">
                    <p className="text-gray-600">Restaurants: {location.current_restaurants}</p>
                    <p className="text-gray-600">Avg Price: ₹{location.avg_price}</p>
                    <p className="text-gray-600">Rating: ⭐ {location.avg_rating}</p>
                    <div className="mt-2 pt-2 border-t">
                      <p className="font-semibold text-primary-600">
                        Score: {location.opportunity_score}/10
                      </p>
                      <p className="text-xs text-gray-500 mt-1">{location.recommendation}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Market Gaps */}
        {marketGaps && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <FiDollarSign className="mr-2 text-primary-600" />
              Market Opportunities - {selectedCity}
            </h2>
            
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-4">High Opportunity Cuisines</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {marketGaps.cuisine_opportunities?.slice(0, 5).map((cuisine, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-lg border-2 ${
                      cuisine.opportunity === 'High'
                        ? 'bg-green-50 border-green-300'
                        : cuisine.opportunity === 'Medium'
                        ? 'bg-yellow-50 border-yellow-300'
                        : 'bg-red-50 border-red-300'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">{cuisine.cuisine}</span>
                      <span
                        className={`px-2 py-1 rounded text-xs font-bold ${
                          cuisine.opportunity === 'High'
                            ? 'bg-green-200 text-green-800'
                            : cuisine.opportunity === 'Medium'
                            ? 'bg-yellow-200 text-yellow-800'
                            : 'bg-red-200 text-red-800'
                        }`}
                      >
                        {cuisine.opportunity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-2">
                      {cuisine.restaurant_count} restaurants • {cuisine.market_share}% market share
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {marketGaps.underserved_areas && marketGaps.underserved_areas.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Underserved Areas</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {marketGaps.underserved_areas.map((area, index) => (
                    <div key={index} className="p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
                      <h4 className="font-semibold text-blue-900">{area.area}</h4>
                      <p className="text-sm text-blue-700 mt-1">
                        {area.restaurant_count} restaurants
                      </p>
                      <p className="text-sm text-blue-700">
                        {area.cuisine_variety} cuisine types
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Insights;
