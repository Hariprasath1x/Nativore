import React from 'react';
import { motion } from 'framer-motion';

const CitySelector = ({ selectedCity, onCityChange, cities = [] }) => {
  const defaultCities = [
    'All Cities',
    'Chennai',
    'Coimbatore',
    'Tiruppur',
    'Madurai',
    'Thoothukudi'
  ];

  const cityList = cities.length > 0 ? ['All Cities', ...cities] : defaultCities;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select City
      </label>
      <select
        value={selectedCity}
        onChange={(e) => onCityChange(e.target.value)}
        className="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
      >
        {cityList.map((city) => (
          <option key={city} value={city === 'All Cities' ? '' : city}>
            {city}
          </option>
        ))}
      </select>
    </motion.div>
  );
};

export default CitySelector;
