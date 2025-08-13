# weather.py
import requests
from config import API_KEY, BASE_URL

def get_weather(city):
    """Fetch weather data for the given city."""
    if API_KEY == "YOUR_REAL_API_KEY" or not API_KEY.strip():
        return {"error": "API key is missing. Please add your key in config.py"}

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if response.status_code == 200:
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"].capitalize()
            }
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your key in config.py"}
        elif response.status_code == 404:
            return {"error": f"City '{city}' not found. Please check the spelling."}
        else:
            return {"error": data.get("message", "Unexpected error occurred")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
