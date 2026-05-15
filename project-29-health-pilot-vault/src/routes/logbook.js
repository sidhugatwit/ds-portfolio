// routes/logbook.js — Pilot Logbook
const express = require('express');
const auth = require('../middleware/auth');
const db = require('../db/database');
const router = express.Router();

// Get all logbook entries
router.get('/', auth, (req, res) => {
    db.all('SELECT * FROM logbook WHERE user_id = ? ORDER BY date DESC',
        [req.user.id], (err, rows) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(rows);
        });
});

// Add logbook entry
router.post('/', auth, (req, res) => {
    const { date, aircraft_type, aircraft_reg, departure, destination,
        total_time, pic_time, ifr_time, night_time,
        landings_day, landings_night, remarks } = req.body;
    db.run(
        `INSERT INTO logbook 
        (user_id, date, aircraft_type, aircraft_reg, departure, destination,
         total_time, pic_time, ifr_time, night_time, landings_day, landings_night, remarks)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)`,
        [req.user.id, date, aircraft_type, aircraft_reg, departure, destination,
            total_time, pic_time, ifr_time, night_time, landings_day, landings_night, remarks],
        function (err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ id: this.lastID, message: 'Flight logged' });
        }
    );
});

// Get logbook totals
router.get('/totals', auth, (req, res) => {
    db.get(
        `SELECT 
         COUNT(*) as total_flights,
         ROUND(SUM(total_time), 1) as total_hours,
         ROUND(SUM(pic_time), 1) as pic_hours,
         ROUND(SUM(ifr_time), 1) as ifr_hours,
         ROUND(SUM(night_time), 1) as night_hours,
         SUM(landings_day) + SUM(landings_night) as total_landings
         FROM logbook WHERE user_id = ?`,
        [req.user.id], (err, row) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(row);
        });
});

module.exports = router;