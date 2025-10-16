// Import dependencies
const express = require("express");
const cors = require("cors");

// Create the app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Mock food trend data
const mockData = {
  chennai: [
    { name: "Idli & Dosa", trend: "High", avgSpend: "₹150" },
    { name: "Biryani", trend: "Medium", avgSpend: "₹250" }
  ],
  mumbai: [
    { name: "Vada Pav", trend: "High", avgSpend: "₹50" },
    { name: "Pav Bhaji", trend: "Medium", avgSpend: "₹120" }
  ]
};

// Default route
app.get("/", (req, res) => {
  res.send("Hello from Nativore backend!");
});

// Trends API
app.get("/trends/:location", (req, res) => {
  const location = req.params.location.toLowerCase();
  res.json(mockData[location] || []);
});

// Start server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

