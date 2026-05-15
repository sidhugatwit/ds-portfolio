# Project 29 — Health & Pilot Credentials Vault

## Overview

A full-stack web application for pilots to securely store FAA credentials,
maintain a digital logbook, and track health records. Built with Node.js,
Express, SQLite, and JWT authentication — fully offline and private.

## Features

### Authentication

- JWT-based login and registration
- bcrypt password hashing
- 7-day token expiry with localStorage persistence

### FAA Credentials Manager

- Store PPL, IFR, CPL, Medical certificates, BFR records
- Certificate number, issue date, expiry date tracking
- File upload support for scanned documents
- Delete credentials with confirmation

### Pilot Logbook

- Full FAA-style flight logging
- Tracks total time, PIC, IFR, night time, landings
- Automatic totals calculation
- Aircraft type, registration, departure, destination

### Health Records

- Blood pressure, heart rate, weight, blood glucose tracking
- FAA Medical certificate status
- Chronological health timeline

### Dashboard

- Live stats: total flights, hours, IFR time, credentials count
- Real-time data from all modules

## Stack

Node.js · Express · SQLite3 · JWT · bcryptjs · Multer · HTML/CSS/JS

## How to Run

```bash
cd project-29-health-pilot-vault
npm install
npm run dev
```
Open <http://localhost:3000>

## Files

- `src/server.js` — Express server entry point
- `src/db/database.js` — SQLite schema and connection
- `src/middleware/auth.js` — JWT authentication middleware
- `src/routes/auth.js` — Register and login endpoints
- `src/routes/credentials.js` — FAA credentials CRUD
- `src/routes/logbook.js` — Pilot logbook with totals
- `src/routes/health.js` — Health records tracking
- `public/index.html` — Full frontend dashboard