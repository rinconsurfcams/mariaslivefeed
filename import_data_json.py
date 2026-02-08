import netCDF4 as nc
import json
import time
from datetime import datetime, timedelta

# URLs con bypass de caché
WAVE_URL = f'http://dm3.caricoos.org/thredds/dodsC/content/Rincon_Waverider/Realtime/181p1_rt.nc?t={int(time.time())}'
WIND_URL = f'http://dm1.caricoos.org/thredds/dodsC/content/WindNet/e9889_tpr_realtime.nc?t={int(time.time())}'

def fetch_data():
    try:
        w_ds = nc.Dataset(WAVE_URL)
        wind_ds = nc.Dataset(WIND_URL)

        # Buscar el último dato de ola real (retrocediendo desde el final)
        h_var = w_ds.variables['waveHs']
        idx = -1
        for i in range(len(h_var)-1, -1, -1):
            val = h_var[i]
            if val is not None and str(val) != '--' and str(val) != 'nan':
                idx = i
                break

        # Buscar el último dato de viento real
        ws_var = wind_ds.variables['AvrgWS']
        w_idx = -1
        for i in range(len(ws_var)-1, -1, -1):
            if ws_var[i] is not None and str(ws_var[i]) != '--':
                w_idx = i
                break

        t_var = w_ds.variables['waveTime']
        # Ajuste a hora de Puerto Rico (UTC-4)
        local_dt = nc.num2date(t_var[idx], units=t_var.units) - timedelta(hours=4)

        data = {
            'timestamp': local_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'wave_height_ft': round(float(h_var[idx] * 3.28084), 1),
            'wave_period': round(float(w_ds.variables['waveTp'][idx]), 1),
            'wave_direction': int(w_ds.variables['waveDp'][idx]),
            'wind_speed': round(float(wind_ds.variables['AvrgWS'][w_idx] * 1.94384), 1),
            'wind_direction': int(wind_ds.variables['DirWS'][w_idx])
        }
        w_ds.close()
        wind_ds.close()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    res = fetch_data()
    if res:
        with open('overlay.json', 'w') as f:
            json.dump(res, f, indent=2)
        print("✅ Overlay actualizado con éxito")
