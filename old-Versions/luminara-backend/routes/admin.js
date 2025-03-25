// routes/admin.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');
const adminMiddleware = require('../middlewares/adminMiddleware');
const { getUsers, updateUserTokens, promoteUser } = require('../controllers/userController');

// Alle Benutzer anzeigen (nur für Admins)
router.get('/users', authMiddleware, adminMiddleware, getUsers);

// Benutzer-Tokens aktualisieren (nur für Admins)
router.put('/users/:id/tokens', authMiddleware, adminMiddleware, updateUserTokens);

// Benutzer befördern (Student zu Student+) (nur für Admins)
router.put('/users/:id/promote', authMiddleware, adminMiddleware, promoteUser);

module.exports = router;
