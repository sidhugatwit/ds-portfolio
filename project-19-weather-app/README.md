# Project 19 — Weather Data Pipeline

A Python weather application that retrieves city weather data, caches current temperature values in SQLite, and visualizes a 24-hour forecast with Matplotlib.

## Overview

This project demonstrates a simple end-to-end data workflow:

- city input from the command line
- geocoding and weather retrieval through Open-Meteo APIs
- local caching with SQLite
- forecast visualization with Matplotlib

It is designed as a lightweight, modular application with separate layers for API access, storage, plotting, and execution.

## Features

- command-line city lookup
- Open-Meteo geocoding and forecast API integration
- SQLite caching for current temperature
- 24-hour temperature forecast plot
- modular Python structure

## Architecture

`main.py` → CLI entry point  
`service.py` → API requests and weather retrieval  
`database.py` → SQLite caching and persistence  
`plotter.py` → forecast visualization

## Example Usage

Run the app:

```bash
python main.py Boston
