// routes/auth.js
const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const dotenv = require('dotenv');

dotenv.config();

// Benutzer registrieren
router.post('/register', async (req, res) => {
    const { username, email, password } = req.body;

    // Einfache Validierung
    if (!username || !email || !password) {
        return res.status(400).json({ message: 'Bitte alle Felder ausfüllen.' });
    }

    try {
        // Überprüfen, ob der Benutzer bereits existiert
        const existingUser = await User.findByEmail(email);
        if (existingUser) {
            return res.status(400).json({ message: 'Benutzer mit dieser E-Mail existiert bereits.' });
        }

        // Passwort hashen
        const hashedPassword = await bcrypt.hash(password, 10);

        // Benutzer erstellen
        const userId = await User.create(username, email, hashedPassword);

        // JWT generieren
        const token = jwt.sign({ id: userId }, process.env.JWT_SECRET, { expiresIn: '1h' });

        res.status(201).json({ token });
    } catch (error) {
        console.error('Registrierungsfehler:', error);
        res.status(500).json({ message: 'Serverfehler' });
    }
});

// Benutzer login
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    // Einfache Validierung
    if (!email || !password) {
        return res.status(400).json({ message: 'Bitte alle Felder ausfüllen.' });
    }

    try {
        // Benutzer finden
        const user = await User.findByEmail(email);
        if (!user) {
            return res.status(400).json({ message: 'Ungültige E-Mail oder Passwort.' });
        }

        // Passwort überprüfen
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ message: 'Ungültige E-Mail oder Passwort.' });
        }

        // JWT generieren
        const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET, { expiresIn: '1h' });

        res.status(200).json({ token });
    } catch (error) {
        console.error('Loginfehler:', error);
        res.status(500).json({ message: 'Serverfehler' });
    }
});

module.exports = router;

