// routes/ai.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');
const { useAIService } = require('../controllers/aiController');

// Beispielroute für eine KI-Funktion
router.post('/use-service', authMiddleware, useAIService);

module.exports = router;

