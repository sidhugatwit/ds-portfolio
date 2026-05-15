// routes/health.js — Health Records
const express = require('express');
const auth = require('../middleware/auth');
const db = require('../db/database');
const router = express.Router();

// Get health records
router.get('/', auth, (req, res) => {
    db.all('SELECT * FROM health_records WHERE user_id = ? ORDER BY recorded_at DESC',
        [req.user.id], (err, rows) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(rows);
        });
});

// Add health record
router.post('/', auth, (req, res) => {
    const { record_type, value, unit, notes } = req.body;
    db.run(
        'INSERT INTO health_records (user_id, record_type, value, unit, notes) VALUES (?,?,?,?,?)',
        [req.user.id, record_type, value, unit, notes],
        function (err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ id: this.lastID, message: 'Health record saved' });
        }
    );
});

// Get summary stats
router.get('/summary', auth, (req, res) => {
    db.all(
        `SELECT record_type, COUNT(*) as count, 
         MAX(recorded_at) as latest
         FROM health_records WHERE user_id = ?
         GROUP BY record_type`,
        [req.user.id], (err, rows) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(rows);
        });
});

module.exports = router;