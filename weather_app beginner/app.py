# app.py
from weather import get_weather

def main():
    print("🌦️ Welcome to the Python Weather App!")
    city = input("Enter city name: ").strip()

    if not city:
        print("⚠️ Please enter a valid city name.")
        return

    result = get_weather(city)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(f"\n📍 Weather in {result['city']}:")
        print(f"🌡️ Temperature: {result['temperature']}°C")
        print(f"💧 Humidity: {result['humidity']}%")
        print(f"☁️ Condition: {result['condition']}")

if __name__ == "__main__":
    main()
