// routes/user.js
const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const User = require('../models/User');

// Benutzerprofil abrufen
router.get('/profile', auth, async (req, res) => {
    try {
        const user = await User.findById(req.user.id);
        if (!user) {
            return res.status(404).json({ message: 'Benutzer nicht gefunden.' });
        }

        // Benutzerinformationen ohne Passwort zurückgeben
        const { password, ...userData } = user;
        res.status(200).json(userData);
    } catch (error) {
        console.error('Fehler beim Abrufen des Profils:', error);
        res.status(500).json({ message: 'Serverfehler' });
    }
});

module.exports = router;

