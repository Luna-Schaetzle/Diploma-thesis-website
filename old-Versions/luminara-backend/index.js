// index.js
const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const adminRoutes = require('./routes/admin');
const protectedRoutes = require('./routes/protected');
const aiRoutes = require('./routes/ai');

dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routen
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/protected', protectedRoutes);
app.use('/api/ai', aiRoutes);

// Starten des Servers
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server läuft auf Port ${PORT}`);
});
