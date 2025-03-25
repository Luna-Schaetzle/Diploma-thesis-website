// routes/protected.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');

// Beispiel für eine geschützte Route
router.get('/dashboard', authMiddleware, (req, res) => {
  res.status(200).json({ message: `Willkommen, ${req.user.username}! Dies ist Ihr Dashboard.` });
});

module.exports = router;

