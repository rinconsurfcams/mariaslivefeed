import netCDF4 as nc
import numpy as np
import json
from datetime import datetime, timedelta

# URLs oficiales de CariCOOS
WAVE_URL = 'http://dm3.caricoos.org/thredds/dodsC/content/Rincon_Waverider/Realtime/181p1_rt.nc'
WIND_URL = 'http://dm1.caricoos.org/thredds/dodsC/content/WindNet/e9889_tpr_realtime.nc'

def fetch_data():
    try:
        # Conexión a los servidores
        wave_ds = nc.Dataset(WAVE_URL)
        wind_ds = nc.Dataset(WIND_URL)

        # --- PROCESAMIENTO DE OLESA (Waverider Rincón) ---
        wave_h_raw = np.array(wave_ds.variables['waveHs'][:])
        wave_p_raw = np.array(wave_ds.variables['waveTp'][:])
        wave_d_raw = np.array(wave_ds.variables['waveDp'][:])
        wave_times = wave_ds.variables['waveTime']

        # Buscamos el último índice que NO sea un valor nulo (NaN)
        valid_wave_indices = np.where(~np.isnan(wave_h_raw))[0]
        if len(valid_wave_indices) == 0:
            raise ValueError("No hay datos de oleaje válidos")
        
        w_idx = valid_wave_indices[-1] # El último dato real

        # Conversión a Pies (1m = 3.28084ft)
        h_ft = round(float(wave_h_raw[w_idx] * 3.28084), 1)
        p_sec = round(float(wave_p_raw[w_idx]), 1)
        d_deg = int(wave_d_raw[w_idx])

        # --- PROCESAMIENTO DE VIENTO (Estación Rincón dm1) ---
        wind_s_raw = np.array(wind_ds.variables['AvrgWS'][:])
        wind_d_raw = np.array(wind_ds.variables['DirWS'][:])

        valid_wind_indices = np.where(~np.isnan(wind_s_raw))[0]
        if len(valid_wind_indices) == 0:
            raise ValueError("No hay datos de viento válidos")
        
        wind_idx = valid_wind_indices[-1]

        # Conversión a Nudos (1 m/s = 1.94384 kts)
        # Nota: Si CariCOOS ya reporta en mph, usa 0.868976 para Nudos
        wind_kts = round(float(wind_s_raw[wind_idx] * 0.868976), 1)
        wind_deg = int(wind_d_raw[wind_idx])

        # --- TIMESTAMP (Ajuste a hora de Puerto Rico UTC-4) ---
        dt = nc.num2date(wave_times[w_idx], units=wave_times.units) - timedelta(hours=4)

        data_dict = {
            'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'wave_height_ft': h_ft,
            'wave_period': p_sec,
            'wave_direction': d_deg,
            'wind_speed': wind_kts,
            'wind_direction': wind_deg
        }

        wave_ds.close()
        wind_ds.close()
        return data_dict

    except Exception as e:
        print(f"❌ Error obteniendo datos: {e}")
        return None

def main():
    data = fetch_data()
    if data:
        # Guardar como JSON para el HTML de OBS
        with open('overlay.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✅ JSON actualizado: {data['wave_height_ft']}ft @ {data['wave_period']}s, Dir: {data['wave_direction']}°")
    else:
        print("⚠️ No se pudo actualizar el archivo JSON.")

if __name__ == "__main__":
    main()
