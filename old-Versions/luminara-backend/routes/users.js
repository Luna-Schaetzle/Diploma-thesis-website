// routes/users.js
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/authMiddleware');
const { getUsers, updateUserTokens, promoteUser } = require('../controllers/userController');

// Alle Benutzer anzeigen (nur für Admins)
router.get('/', authMiddleware, async (req, res) => {
  try {
    // Prüfen, ob der Benutzer ein Admin ist (tokens = NULL)
    if (req.user.tokens !== null) {
      return res.status(403).json({ message: 'Zugriff verweigert.' });
    }

    const [users] = await db.query('SELECT id, username, email, tokens, created_at FROM users');

    res.status(200).json({ users });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Serverfehler' });
  }
});

// Benutzer-Tokens aktualisieren (nur für Admins)
router.put('/update-tokens/:id', authMiddleware, updateUserTokens);

// Benutzer befördern (Student zu Student+) (nur für Admins)
router.put('/promote/:id', authMiddleware, promoteUser);

module.exports = router;

