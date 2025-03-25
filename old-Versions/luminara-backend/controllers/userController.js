// controllers/userController.js
const db = require('../config/db');

// Alle Benutzer anzeigen (Admin-Funktion)
exports.getUsers = async (req, res) => {
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
};

// Benutzer-Tokens aktualisieren (Admin-Funktion)
exports.updateUserTokens = async (req, res) => {
  const userId = req.params.id;
  const { tokens } = req.body;

  if (tokens === undefined) {
    return res.status(400).json({ message: 'Token-Anzahl erforderlich.' });
  }

  try {
    // Prüfen, ob der Benutzer ein Admin ist (tokens = NULL)
    const [adminUser] = await db.query('SELECT * FROM users WHERE id = ?', [req.user.id]);
    if (adminUser[0].tokens !== null) {
      return res.status(403).json({ message: 'Zugriff verweigert.' });
    }

    // Benutzer suchen
    const [user] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
    if (user.length === 0) {
      return res.status(404).json({ message: 'Benutzer nicht gefunden.' });
    }

    // Token aktualisieren
    await db.query('UPDATE users SET tokens = ? WHERE id = ?', [tokens, userId]);

    res.status(200).json({ message: 'Token-Anzahl aktualisiert.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Serverfehler' });
  }
};

// Benutzer befördern (Student zu Student+) (Admin-Funktion)
exports.promoteUser = async (req, res) => {
  const userId = req.params.id;

  try {
    // Prüfen, ob der Benutzer ein Admin ist (tokens = NULL)
    const [adminUser] = await db.query('SELECT * FROM users WHERE id = ?', [req.user.id]);
    if (adminUser[0].tokens !== null) {
      return res.status(403).json({ message: 'Zugriff verweigert.' });
    }

    // Benutzer suchen
    const [user] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
    if (user.length === 0) {
      return res.status(404).json({ message: 'Benutzer nicht gefunden.' });
    }

    // Befördern: erhöhen Sie die Token-Anzahl für Student+ (z.B. von 100 auf 200)
    const newTokens = (user[0].tokens || 0) + 100;

    await db.query('UPDATE users SET tokens = ? WHERE id = ?', [newTokens, userId]);

    res.status(200).json({ message: 'Benutzer wurde zu Student+ befördert.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Serverfehler' });
  }
};
