// routes/credentials.js — FAA Certificate Storage
const express = require('express');
const multer = require('multer');
const path = require('path');
const auth = require('../middleware/auth');
const db = require('../db/database');
const router = express.Router();

const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null, Date.now() + path.extname(file.originalname))
});
const upload = multer({ storage });

// Get all credentials
router.get('/', auth, (req, res) => {
    db.all('SELECT * FROM credentials WHERE user_id = ?',
        [req.user.id], (err, rows) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json(rows);
        });
});

// Add credential
router.post('/', auth, upload.single('file'), (req, res) => {
    const { type, certificate_no, issued_date, expiry_date, notes } = req.body;
    const file_path = req.file ? req.file.filename : null;
    db.run(
        `INSERT INTO credentials 
        (user_id, type, certificate_no, issued_date, expiry_date, notes, file_path)
        VALUES (?,?,?,?,?,?,?)`,
        [req.user.id, type, certificate_no, issued_date, expiry_date, notes, file_path],
        function (err) {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ id: this.lastID, message: 'Credential saved' });
        }
    );
});

// Delete credential
router.delete('/:id', auth, (req, res) => {
    db.run('DELETE FROM credentials WHERE id = ? AND user_id = ?',
        [req.params.id, req.user.id], (err) => {
            if (err) return res.status(500).json({ error: err.message });
            res.json({ message: 'Credential deleted' });
        });
});

module.exports = router;