// routes/auth.js
const express = require('express');
const router = express.Router();
const { registerUser, loginUser } = require('../controllers/authController');

// Registrierung
router.post('/register', registerUser);

// Login
router.post('/login', loginUser);

module.exports = router;
