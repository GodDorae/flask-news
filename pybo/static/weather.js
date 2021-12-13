const API_KEY = "56424122f66d0c315b22ba6055180341"

function onGeoOk(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  console.log("You live in", lat, lon);
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
  fetch(url)
  .then((response) => response.json())
  .then((data) => {
    const weather = document.getElementById("weather");
    const city = document.getElementById("region");
    city.innerText = data.name;
    weather.innerText = `${data.weather[0].main} / ${data.main.temp}°C`;
  });
}
function onGeoError() {
  alert("Can't find you. No weather for you.")
}

navigator.geolocation.getCurrentPosition(onGeoOk, onGeoError);
