// config.js — one place for secrets and settings
const crypto = require('crypto');

let jwtSecret = process.env.JWT_SECRET;
if (!jwtSecret) {
    if (process.env.NODE_ENV === 'production') {
        throw new Error('JWT_SECRET must be set in production. Copy .env.example to .env and set it.');
    }
    // Local dev: random per-run secret, so no secret ever lives in the repo.
    jwtSecret = crypto.randomBytes(32).toString('hex');
    console.warn('[config] JWT_SECRET not set; using a random dev secret (logins reset on restart).');
}

module.exports = { JWT_SECRET: jwtSecret };
