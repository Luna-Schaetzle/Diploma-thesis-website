// middlewares/authMiddleware.js
const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  // JWT aus dem Header abrufen
  const token = req.header('Authorization')?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Kein Token, Zugriff verweigert.' });
  }

  try {
    // Token verifizieren
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // Benutzerinformationen zum Request hinzufügen
    next();
  } catch (error) {
    res.status(401).json({ message: 'Token ist ungültig.' });
  }
};

module.exports = authMiddleware;

