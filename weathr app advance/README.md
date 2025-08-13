# Advanced Weather App (Tkinter GUI)

A desktop weather client with a clean GUI. Search by city or use “Use My Location” (IP-based). Shows current conditions, hourly forecast, and 5-day daily forecast with icons and unit toggle.

## Features
- 🌍 City input + “Use My Location”
- 🌦️ Current: temp, feels-like, humidity, pressure, wind (speed & direction)
- 🕒 Hourly (next ~24h in 3h steps)
- 📅 Daily (5 days, min/max) with icons
- 🔁 Units: Celsius (metric) / Fahrenheit (imperial)
- 🧯 Error handling (network, invalid key, city not found)

## Tech
- Python 3.9+
- Tkinter (GUI)
- requests, Pillow (for icons)

## Setup
1. Get an API key from OpenWeatherMap: https://home.openweathermap.org/api_keys
2. Edit `config.py` and set:
   ```python
   API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
