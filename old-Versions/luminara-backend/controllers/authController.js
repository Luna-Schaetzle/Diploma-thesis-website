// controllers/authController.js
const db = require('../config/db');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// Benutzerregistrierung
exports.registerUser = async (req, res) => {
  const { username, email, password } = req.body;

  // Validierung
  if (!username || !email || !password) {
    console.warn('Registrierung fehlgeschlagen: Fehlende Felder');
    return res.status(400).json({ message: 'Bitte alle Felder ausfüllen.' });
  }

  try {
    // Überprüfen, ob Benutzer bereits existiert
    const [existingUser] = await db.query(
      'SELECT * FROM users WHERE username = ? OR email = ?',
      [username, email]
    );

    if (existingUser.length > 0) {
      console.warn(`Registrierung fehlgeschlagen: Benutzername oder E-Mail bereits vergeben - ${username}, ${email}`);
      return res.status(400).json({ message: 'Benutzername oder E-Mail bereits vergeben.' });
    }

    // Passwort hashen
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Initiale Token basierend auf Benutzerrolle
    const initialTokens = 100;

    // Benutzer in der Datenbank speichern
    const [result] = await db.query(
      'INSERT INTO users (username, email, password, tokens) VALUES (?, ?, ?, ?)',
      [username, email, hashedPassword, initialTokens]
    );

    // JWT generieren
    const token = jwt.sign(
      { id: result.insertId, username, email },
      process.env.JWT_SECRET, // Verwendet das Secret aus der .env-Datei
      { expiresIn: process.env.JWT_EXPIRES_IN }
    );

    console.log(`Neuer Benutzer registriert: ${username} (${email})`);
    res.status(201).json({ token, user: { id: result.insertId, username, email, tokens: initialTokens } });
  } catch (error) {
    console.error('Fehler bei der Benutzerregistrierung:', error);
    res.status(500).json({ message: 'Serverfehler', error: error.message });
  }
};
