import netCDF4 as nc
import json
from datetime import datetime

wave_url = 'http://dm3.caricoos.org/thredds/dodsC/content/Rincon_Waverider/Realtime/181p1_rt.nc'
wind_url = 'http://dm3.caricoos.org:8001/thredds/dodsC/WindNet/e9889/e9889_tpr_realtime.nc'

def fetch_data():
    wave_dataset = nc.Dataset(wave_url)
    wind_dataset = nc.Dataset(wind_url)

    i = -1

    wave_time = nc.num2date(wave_dataset.variables['waveTime'][i], wave_dataset.variables['waveTime'].units)
    wave_height = (wave_dataset.variables['waveHs'][i] * 3.28084).round(1)
    wave_period = wave_dataset.variables['waveTp'][i].round(1)
    wave_dir = wave_dataset.variables['waveDp'][i].round(0)

    wind_time = nc.num2date(wind_dataset.variables['time'][i], wind_dataset.variables['time'].units)
    wind_speed = wind_dataset.variables['AvrgWS'][i].round(1)
    wind_dir = wind_dataset.variables['DirWS'][i].round(0)

    timestamp = max(wave_time, wind_time).strftime('%Y-%m-%d %H:%M:%S')

    data = {
        "timestamp": timestamp,
        "wave_height_ft": float(wave_height),
        "wave_period": float(wave_period),
        "wave_direction": int(wave_dir),
        "wind_speed": float(wind_speed),
        "wind_direction": int(wind_dir)
    }

    with open("overlay.json", "w") as f:
        json.dump(data, f)

    print("✅ overlay.json actualizado")

    wave_dataset.close()
    wind_dataset.close()

if __name__ == "__main__":
    fetch_data()
