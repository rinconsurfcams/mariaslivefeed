
import requests
import pandas as pd
import netCDF4 as nc
from datetime import datetime
import json

def fetch_data():
    wave_url = "http://dm3.caricoos.org/thredds/dodsC/content/Rincon_Waverider/Realtime/181p1_rt.nc"
    dataset = nc.Dataset(wave_url)

    # Extraer datos de olas
    wave_heights = dataset.variables["WVHT"][:]
    times = nc.num2date(dataset.variables["time"][:], units=dataset.variables["time"].units)

    df = pd.DataFrame({
        "time": times,
        "significant_wave_height": wave_heights
    })

    # Filtrar la última observación válida
    latest = df.dropna().iloc[-1]

    return {
        "timestamp": latest["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "significant_wave_height": round(float(latest["significant_wave_height"]), 2)
    }

def main():
    data = fetch_data()

    with open("overlay.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ overlay.json actualizado con altura significativa de oleaje.")

if __name__ == "__main__":
    main()
