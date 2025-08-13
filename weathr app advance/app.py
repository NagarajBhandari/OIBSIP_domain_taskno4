from flask import Flask, render_template, request, jsonify
import requests
import config

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    params = {
        "q": city,
        "appid": config.API_KEY,
        "units": config.DEFAULT_UNITS
    }

    response = requests.get(config.CURRENT_URL, params=params)
    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
