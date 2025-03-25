// middlewares/adminMiddleware.js
const db = require('../config/db');

const adminMiddleware = async (req, res, next) => {
  try {
    const userId = req.user.id;

    // Benutzer suchen
    const [user] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);

    if (user.length === 0) {
      return res.status(404).json({ message: 'Benutzer nicht gefunden.' });
    }

    // Prüfen, ob tokens NULL sind (Admin)
    if (user[0].tokens !== null) {
      return res.status(403).json({ message: 'Admin-Zugriff erforderlich.' });
    }

    next();
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Serverfehler' });
  }
};

module.exports = adminMiddleware;

