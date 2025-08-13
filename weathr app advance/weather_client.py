# weather_client.py
import requests
from datetime import datetime
from collections import defaultdict
from config import API_KEY, CURRENT_URL, FORECAST_URL, GEOLOCATE_URL

class WeatherError(Exception):
    pass

def _check_key():
    if not API_KEY or API_KEY.strip() in ("YOUR_OPENWEATHERMAP_API_KEY", ""):
        raise WeatherError("API key is missing. Add it in config.py.")

def geolocate_city():
    """
    Returns a (city, countryCode) tuple using IP-based geolocation, or raises WeatherError.
    """
    try:
        r = requests.get(GEOLOCATE_URL, timeout=5)
        data = r.json()
        if data.get("status") == "success":
            city = data.get("city")
            country = data.get("countryCode")
            if city:
                return city, country
        raise WeatherError("Could not detect location from IP.")
    except requests.RequestException as e:
        raise WeatherError(f"Geolocation failed: {e}")

def fetch_current(city, units="metric"):
    """
    Returns dict with current weather for a city.
    """
    _check_key()
    params = {"q": city, "appid": API_KEY, "units": units}
    try:
        r = requests.get(CURRENT_URL, params=params, timeout=8)
        data = r.json()

        if r.status_code == 401:
            raise WeatherError("Invalid API key.")
        if r.status_code == 404:
            raise WeatherError(f"City '{city}' not found.")
        if r.status_code != 200:
            raise WeatherError(data.get("message", "Unexpected error from API."))

        return {
            "city": data["name"],
            "country": data["sys"].get("country", ""),
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"].get("deg", 0),
            "description": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"],
            "dt": data["dt"],
            "timezone": data.get("timezone", 0),
        }
    except requests.RequestException as e:
        raise WeatherError(f"Network error: {e}")

def fetch_forecast(city, units="metric"):
    """
    Returns dict with:
      - hourly: next ~8 slots (3-hour steps) with time, temp, icon, description
      - daily: next 5 days aggregated with min/max, icon, description
    """
    _check_key()
    params = {"q": city, "appid": API_KEY, "units": units}
    try:
        r = requests.get(FORECAST_URL, params=params, timeout=10)
        data = r.json()

        if r.status_code == 401:
            raise WeatherError("Invalid API key.")
        if r.status_code == 404:
            raise WeatherError(f"City '{city}' not found.")
        if r.status_code != 200:
            raise WeatherError(data.get("message", "Unexpected error from API."))

        list_ = data.get("list", [])
        city_info = data.get("city", {})

        # Hourly (next 8 entries ≈ next 24 hours)
        hourly = []
        for item in list_[:8]:
            ts = item["dt"]
            hourly.append({
                "time": ts,
                "temp": item["main"]["temp"],
                "description": item["weather"][0]["description"].capitalize(),
                "icon": item["weather"][0]["icon"],
            })

        # Daily aggregation (by date)
        by_date = defaultdict(list)
        for item in list_:
            dt_obj = datetime.utcfromtimestamp(item["dt"] + city_info.get("timezone", 0))
            date_key = dt_obj.date().isoformat()
            by_date[date_key].append(item)

        daily = []
        for date_key, items in list(by_date.items())[:5]:
            temps = [x["main"]["temp"] for x in items]
            # pick the icon/description closest to midday if possible
            midday = min(items, key=lambda x: abs(datetime.utcfromtimestamp(x["dt"]).hour - 12))
            daily.append({
                "date": date_key,
                "min": round(min(temps), 1),
                "max": round(max(temps), 1),
                "description": midday["weather"][0]["description"].capitalize(),
                "icon": midday["weather"][0]["icon"],
            })

        return {"hourly": hourly, "daily": daily, "city": city_info.get("name", ""), "timezone": city_info.get("timezone", 0)}
    except requests.RequestException as e:
        raise WeatherError(f"Network error: {e}")

def deg_to_compass(deg: int) -> str:
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
            "S","SSW","SW","WSW","W","WNW","NW","NNW"]
    ix = int((deg/22.5)+0.5) % 16
    return dirs[ix]
