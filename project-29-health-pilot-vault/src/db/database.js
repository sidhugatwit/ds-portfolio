// database.js — SQLite setup with all tables
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, '../../data/pilotvault.db');

// Ensure data directory exists
const fs = require('fs');
const dataDir = path.join(__dirname, '../../data');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) console.error('Database error:', err);
    else console.log('PilotVault database connected');
});

// Create all tables
db.serialize(() => {
    // Users table
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT UNIQUE NOT NULL,
        email       TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL,
        full_name   TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // FAA Credentials table
    db.run(`CREATE TABLE IF NOT EXISTS credentials (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL,
        type            TEXT NOT NULL,
        certificate_no  TEXT,
        issued_date     TEXT,
        expiry_date     TEXT,
        issuing_authority TEXT DEFAULT 'FAA',
        notes           TEXT,
        file_path       TEXT,
        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )`);

    // Health records table
    db.run(`CREATE TABLE IF NOT EXISTS health_records (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        record_type TEXT NOT NULL,
        value       TEXT,
        unit        TEXT,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes       TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )`);

    // Pilot logbook table
    db.run(`CREATE TABLE IF NOT EXISTS logbook (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL,
        date            TEXT NOT NULL,
        aircraft_type   TEXT,
        aircraft_reg    TEXT,
        departure       TEXT,
        destination     TEXT,
        total_time      REAL,
        pic_time        REAL,
        ifr_time        REAL,
        night_time      REAL,
        landings_day    INTEGER DEFAULT 0,
        landings_night  INTEGER DEFAULT 0,
        remarks         TEXT,
        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )`);

    console.log('All tables initialized');
});

module.exports = db;