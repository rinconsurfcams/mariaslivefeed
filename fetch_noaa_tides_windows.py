
import requests
import json
from datetime import datetime, timedelta

def get_tide_predictions(station_id="9759394", date=None):
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    base_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    params = {
        "begin_date": date,
        "end_date": date,
        "station": station_id,
        "product": "predictions",
        "datum": "MLLW",
        "time_zone": "lst_ldt",
        "units": "english",
        "interval": "hilo",
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["predictions"]

def build_overlay_json(predictions):
    tide_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tide_predictions": []
    }
    for p in predictions:
        dt = datetime.strptime(p["t"], "%Y-%m-%d %H:%M")
        time_formatted = dt.strftime("%I:%M %p").lstrip("0")  # Compatible con Windows
        tide_data["tide_predictions"].append({
            "type": "Alta" if p["type"] == "H" else "Baja",
            "time": time_formatted,
            "height_ft": float(p["v"])
        })
    return tide_data

if __name__ == "__main__":
    today = datetime.now().strftime("%Y%m%d")
    predictions = get_tide_predictions(date=today)
    overlay = build_overlay_json(predictions)

    with open("overlay_tides.json", "w", encoding="utf-8") as f:
        json.dump(overlay, f, indent=2)
    print("✅ overlay_tides.json creado correctamente.")
