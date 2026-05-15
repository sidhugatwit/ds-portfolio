// server.js — PilotVault Express Backend
const express = require('express');
const cors = require('cors');
const path = require('path');
const dotenv = require('dotenv');
dotenv.config({ path: path.join(__dirname, '../../.env') });

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../public')));
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Routes
const authRoutes = require('./routes/auth');
const credentialRoutes = require('./routes/credentials');
const healthRoutes = require('./routes/health');
const logbookRoutes = require('./routes/logbook');

app.use('/api/auth', authRoutes);
app.use('/api/credentials', credentialRoutes);
app.use('/api/health', healthRoutes);
app.use('/api/logbook', logbookRoutes);

// Health check
app.get('/api/status', (req, res) => {
    res.json({
        status: 'PilotVault running',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, () => {
    console.log(`PilotVault server running on http://localhost:${PORT}`);
});

module.exports = app;