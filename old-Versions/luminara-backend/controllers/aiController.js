// controllers/aiController.js
const db = require('../config/db');

// Beispiel für die Nutzung einer KI-Funktion
exports.useAIService = async (req, res) => {
  try {
    const userId = req.user.id;

    // Benutzer suchen
    const [user] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);

    if (user.length === 0) {
      return res.status(404).json({ message: 'Benutzer nicht gefunden.' });
    }

    const currentTokens = user[0].tokens;

    // Prüfen, ob der Benutzer genug Token hat
    if (currentTokens === null) {
      // Admin hat unbegrenzte Token
      // Hier KI-Funktion ausführen
      // Beispiel: res.status(200).json({ message: 'KI-Funktion ausgeführt.' });
      return res.status(200).json({ message: 'KI-Funktion ausgeführt (Admin).' });
    }

    if (currentTokens <= 0) {
      return res.status(403).json({ message: 'Keine Token mehr verfügbar.' });
    }

    // Token reduzieren
    const newTokens = currentTokens - 1;
    await db.query('UPDATE users SET tokens = ? WHERE id = ?', [newTokens, userId]);

    // Hier KI-Funktion ausführen
    // Beispiel: res.status(200).json({ message: 'KI-Funktion ausgeführt.', remainingTokens: newTokens });

    res.status(200).json({ message: 'KI-Funktion ausgeführt.', remainingTokens: newTokens });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Serverfehler' });
  }
};

