// routes/auth.js — Register & Login
const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../db/database');
const router = express.Router();

const JWT_SECRET = process.env.JWT_SECRET || 'pilotvault-secret-2025';

// Register
router.post('/register', (req, res) => {
    const { username, email, password, full_name } = req.body;
    if (!username || !email || !password)
        return res.status(400).json({ error: 'All fields required' });

    const hash = bcrypt.hashSync(password, 10);
    db.run(
        'INSERT INTO users (username, email, password, full_name) VALUES (?,?,?,?)',
        [username, email, hash, full_name],
        function (err) {
            if (err) return res.status(400).json({ error: 'User already exists' });
            const token = jwt.sign({ id: this.lastID, username }, JWT_SECRET, { expiresIn: '7d' });
            res.json({ token, username, message: 'Registration successful' });
        }
    );
});

// Login
router.post('/login', (req, res) => {
    const { username, password } = req.body;
    db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
        if (err || !user) return res.status(401).json({ error: 'Invalid credentials' });
        if (!bcrypt.compareSync(password, user.password))
            return res.status(401).json({ error: 'Invalid credentials' });
        const token = jwt.sign({ id: user.id, username }, JWT_SECRET, { expiresIn: '7d' });
        res.json({ token, username, full_name: user.full_name });
    });
});

module.exports = router;