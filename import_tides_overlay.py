
import requests
import json
from datetime import datetime, timedelta

def fetch_tide_predictions():
    begin_date = datetime.now().strftime("%Y%m%d")
    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date={begin_date}&end_date={end_date}&datum=MLLW&station=9759394&time_zone=lst_ldt&units=english&interval=hilo&format=json"

    response = requests.get(url)
    data = response.json()

    predictions = []
    for pred in data['predictions']:
        time = datetime.strptime(pred['t'], "%Y-%m-%d %H:%M")
        predictions.append({
            'time': time.strftime("%I:%M %p"),
            'type': 'Alta' if pred['type'] == 'H' else 'Baja',
            'height_ft': float(pred['v'])
        })

    return predictions

def main():
    tide_predictions = fetch_tide_predictions()

    overlay_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tide_predictions": tide_predictions
    }

    with open("overlay_tides.json", "w") as f:
        json.dump(overlay_data, f, indent=4)

if __name__ == "__main__":
    main()
