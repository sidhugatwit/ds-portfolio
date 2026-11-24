# Pilot Credentials Vault

I built a local app for pilot credentials, logbook entries and health records, with a database and a browser interface.

## Architecture

Browser interface → Express routes and JWT checks → SQLite records and local uploads.

## Run locally

Use Node.js 22. Copy the sample configuration to a local ignored environment file and generate your own signing secret. Run `npm ci` and `npm start` in this folder.

## Results

TODO · Record api startup check with a reproducible artifact.

## Demo and deployment

TODO · Record a demo and verify any deployment. Capture a thumbnail from a real output or demo.

## Next steps

Record a demo with synthetic data and verify authentication, uploads and secret configuration before considering a deployment.

## Implementation notes

> **Not for official record keeping.** This is an educational project. Your official logbook, FAA certificates and medical records remain the legal source of truth.

## Overview

A full-stack web application for pilots to securely store FAA credentials,
maintain a digital logbook, and track health records. Built with Node.js,
Express, SQLite, and JWT authentication — intended for local use with sample data.

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
