const statusEl = document.getElementById("status");

const map = L.map("map", {
  worldCopyJump: true,
  minZoom: 2,
}).setView([18, 0], 2);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 5,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

const TLE_SOURCE =
  "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle";
const MAX_OBJECTS = 50;
const REFRESH_MS = 10_000;

let trackedObjects = [];
let markers = [];

function updateStatus(text) {
  statusEl.textContent = text;
}

function parseTLEBlocks(rawText) {
  const lines = rawText
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const objects = [];

  for (let i = 0; i + 2 < lines.length && objects.length < MAX_OBJECTS; i += 3) {
    const name = lines[i];
    const tle1 = lines[i + 1];
    const tle2 = lines[i + 2];

    if (!tle1.startsWith("1 ") || !tle2.startsWith("2 ")) {
      continue;
    }

    const satrec = satellite.twoline2satrec(tle1, tle2);
    objects.push({ name, satrec });
  }

  return objects;
}

function getSubpoint(satrec, atDate = new Date()) {
  const pv = satellite.propagate(satrec, atDate);

  if (!pv.position) {
    return null;
  }

  const gmst = satellite.gstime(atDate);
  const geodetic = satellite.eciToGeodetic(pv.position, gmst);

  return {
    latitude: satellite.degreesLat(geodetic.latitude),
    longitude: satellite.degreesLong(geodetic.longitude),
  };
}

function renderPositions() {
  const now = new Date();

  for (const entry of markers) {
    map.removeLayer(entry.marker);
  }

  markers = [];

  for (const obj of trackedObjects) {
    const subpoint = getSubpoint(obj.satrec, now);
    if (!subpoint) continue;

    const { latitude, longitude } = subpoint;
    const marker = L.circleMarker([latitude, longitude], {
      radius: 4,
      color: "#ffc857",
      fillColor: "#ffd991",
      fillOpacity: 0.9,
      weight: 1,
    }).addTo(map);

    marker.bindTooltip(
      `<strong>${obj.name}</strong><br>Lat: ${latitude.toFixed(2)}°<br>Lon: ${longitude.toFixed(2)}°`,
      { direction: "top", sticky: true }
    );

    markers.push({ marker, name: obj.name });
  }

  updateStatus(
    `Showing ${markers.length} live objects · Updated ${now.toLocaleTimeString()}`
  );
}

async function loadTLE() {
  updateStatus("Loading TLE data from Celestrak...");

  try {
    const response = await fetch(TLE_SOURCE);
    if (!response.ok) {
      throw new Error(`TLE request failed (${response.status})`);
    }

    const text = await response.text();
    trackedObjects = parseTLEBlocks(text);

    if (trackedObjects.length < 20) {
      throw new Error("Loaded fewer than 20 valid TLE objects.");
    }

    renderPositions();
    setInterval(renderPositions, REFRESH_MS);
  } catch (error) {
    console.error(error);
    updateStatus(`Unable to load live data: ${error.message}`);
  }
}

loadTLE();
