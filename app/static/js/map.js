let map, markers = [];

function initGeolocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        document.getElementById("status").innerText = "Геолокація не підтримується у вашому браузері.";
    }
}

function success(position) {

    // const lat = 50.4667; //київ
    // const lon = 30.4886;
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById("status").innerText = `Ваше місцезнаходження: ${lat}, ${lon}`;


    // відправка координат
    fetch("/labs_nearby", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Лабораторії отримано:", data);
        initializeMap(lat, lon, data);
    })
    .catch(error => {
        console.error("Помилка:", error);
        document.getElementById("status").innerText = "Не вдалося отримати дані лабораторій.";
    });
}

function error() {
    document.getElementById("status").innerText = "Геолокацію відхилено. Використовуємо координати Івано-Франківська.";

    const lat = 48.9226; // Івано-Франківськ
    const lon = 24.7111;

    fetch("/labs_nearby", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ latitude: lat, longitude: lon })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Лабораторії отримано:", data);
        initializeMap(lat, lon, data);
    })
    .catch(error => {
        console.error("Помилка:", error);
        document.getElementById("status").innerText = "не вдалося отримати дані лабораторій.";
    });
}

function initializeMap(userLat, userLon, labs) {
    map = L.map("map").setView([userLat, userLon], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([userLat, userLon]).addTo(map)
        .bindPopup("Ваше місцезнаходження");

    // маркери лабораторій
    labs.forEach(lab => {
        const lat = lab.coordinates[0];
        const lon = lab.coordinates[1];


        const labIcon = L.icon({
            iconUrl: lab.icon,
            iconSize: [41, 41],
            iconAnchor: [15, 30],
            popupAnchor: [0, -30]
        });

        L.marker([lat, lon], { icon: labIcon }).addTo(map)
            .bindPopup(`${lab.lab_name} (Відстань: ${lab.distance.toFixed(2)} км)`);
    });

    document.getElementById("loading-spinner").style.display = "none";
    document.getElementById("footer-margin-top").style.display = "none";
    document.getElementById("map").style.display = "block";


    map.invalidateSize();
}

window.onload = initGeolocation;