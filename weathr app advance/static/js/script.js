function fetchWeather() {
  const city = document.getElementById("cityInput").value;
  if (!city) {
    alert("Please enter a city name.");
    return;
  }

  fetch("/get_weather", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ city: city })
  })
  .then(res => res.json())
  .then(data => {
    const resultDiv = document.getElementById("weatherResult");
    if (data.error) {
      resultDiv.innerHTML = `<p style='color:red;'>${data.error}</p>`;
    } else {
      resultDiv.innerHTML = `
        <h2>${data.name}, ${data.sys.country}</h2>
        <p>Temperature: ${data.main.temp}°C</p>
        <p>Weather: ${data.weather[0].description}</p>
      `;
    }
  });
}
