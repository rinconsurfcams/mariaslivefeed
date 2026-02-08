import netCDF4 as nc
import json
import time
from datetime import datetime, timedelta

WAVE_URL = f'http://dm3.caricoos.org/thredds/dodsC/content/Rincon_Waverider/Realtime/181p1_rt.nc?t={int(time.time())}'
WIND_URL = f'http://dm1.caricoos.org/thredds/dodsC/content/WindNet/e9889_tpr_realtime.nc?t={int(time.time())}'

def fetch_data():
    try:
        wave_ds = nc.Dataset(WAVE_URL)
        wind_ds = nc.Dataset(WIND_URL)

        # Olas - Buscamos el último dato no nulo manualmente
        h_var = wave_ds.variables['waveHs']
        p_var = wave_ds.variables['waveTp']
        d_var = wave_ds.variables['waveDp']
        t_var = wave_ds.variables['waveTime']

        # Encontrar último índice válido sin usar numpy
        idx = -1
        for i in range(len(h_var) - 1, -1, -1):
            if h_var[i] is not None and str(h_var[i]) != '--' and str(h_var[i]) != 'nan':
                idx = i
                break
        
        # Viento - Buscamos el último dato no nulo
        ws_var = wind_ds.variables['AvrgWS']
        wd_var = wind_ds.variables['DirWS']
        w_idx = -1
        for i in range(len(ws_var) - 1, -1, -1):
            if ws_var[i] is not None and str(ws_var[i]) != '--':
                w_idx = i
                break

        data = {
            'timestamp': (nc.num2date(t_var[idx], units=t_var.units) - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
            'wave_height_ft': round(float(h_var[idx] * 3.28084), 1),
            'wave_period': round(float(p_var[idx]), 1),
            'wave_direction': int(d_var[idx]),
            'wind_speed': round(float(ws_var[w_idx] * 1.94384), 1),
            'wind_direction': int(wd_var[w_idx])
        }
        
        wave_ds.close()
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
        print("✅ Overlay actualizado correctamente")
