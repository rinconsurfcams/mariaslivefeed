import netCDF4 as nc
import pandas as pd
import numpy as np
import json
from datetime import timedelta

# Define URLs for wave and wind data
wave_url = ('http://dm3.caricoos.org/thredds/dodsC/content/'
           'Rincon_Waverider/Realtime/181p1_rt.nc')
wind_url = ('http://dm3.caricoos.org/thredds/dodsC/content/'
           'WindNet/e9889_tpr_realtime.nc')


def fetch_data():
    # Open datasets
    wave_dataset = nc.Dataset(wave_url)
    wind_dataset = nc.Dataset(wind_url)

    # Access variables
    wave_time = wave_dataset.variables['waveTime']
    wave_height = wave_dataset.variables['waveHs']
    wave_period = wave_dataset.variables['waveTp']
    wave_direction = wave_dataset.variables['waveDp']
    wind_time = wind_dataset.variables['time']
    wind_speed = wind_dataset.variables['AvrgWS']
    wind_direction = wind_dataset.variables['DirWS']

    # Get latest data
    latest_index = -1  # Assuming the latest data is at the last index
    
    # Convert MaskedArray to regular array and round
    wave_height_ft = (np.array(wave_height[latest_index]) * 3.28084).round(1)
    wave_period_val = np.array(wave_period[latest_index]).round(1)
    wave_direction_val = np.array(wave_direction[latest_index]).round(0)
    wind_speed_val = (np.array(wind_speed[latest_index]) * 0.868976).round(1)  # Convert mph to knots
    wind_direction_val = np.array(wind_direction[latest_index]).round(0)

    # Convert timestamps to local time (UTC-4)
    wave_timestamp = nc.num2date(wave_time[latest_index], 
                               units=wave_time.units) - timedelta(hours=4)

    # Create data dictionary for JSON with rounded values
    data_dict = {
        'timestamp': wave_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'wave_height_ft': round(float(wave_height_ft), 1),
        'wave_period': round(float(wave_period_val), 1),
        'wave_direction': int(wave_direction_val),
        'wind_speed': round(float(wind_speed_val), 1),
        'wind_direction': int(wind_direction_val)
    }

    # Create DataFrame for HTML table
    df = pd.DataFrame({
        'Timestamp': [wave_timestamp.strftime('%Y-%m-%d %H:%M:%S')],
        'Wave Height (ft)': [wave_height_ft],
        'Wave Period (s)': [wave_period_val],
        'Wave Direction (°)': [wave_direction_val],
        'Wind Speed (mph)': [wind_speed_val],
        'Wind Direction (°)': [wind_direction_val]
    })

    # Close datasets
    wave_dataset.close()
    wind_dataset.close()

    return df, data_dict


def update_files(df, data_dict):
    # Save JSON file for overlay with UTF-8 encoding
    with open('overlay.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False)
    print("Overlay JSON file updated")

    # Convert DataFrame to HTML
    html_content = df.to_html()

    # HTML template with overlay
    html_template = f"""
    <html>
    <head>
    <title>Wave and Wind Data</title>
    <meta charset="utf-8">
    <style>
        #overlay {{
            position: fixed;
            top: 10px;
            left: 10px;
            color: white;
            font-size: 16px;
            background-color: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
        }}
    </style>
    </head>
    <body>
    <div id="overlay">
        🌊 Cargando datos de Rincón...
    </div>
    <h1>Latest Surf Conditions</h1>
    {html_content}
    <script>
    async function updateOverlay() {{
        try {{
            const response = await fetch("overlay.json");
            const data = await response.json();
            document.getElementById("overlay").innerHTML = `
                📅 ${{data.timestamp}}<br>
                🌊 Oleaje: ${{data.wave_height_ft}} pies @ ${{data.wave_period}} s, 
                dirección ${{data.wave_direction}}°<br>
                💨 Viento: ${{data.wind_speed}} nudos, dirección ${{data.wind_direction}}°
            `;
        }} catch (error) {{
            console.error("Error al cargar los datos:", error);
            document.getElementById("overlay").innerHTML = 
                "⚠️ No se pueden cargar los datos.";
        }}
    }}

    updateOverlay();
    setInterval(updateOverlay, 10 * 60 * 1000); // Actualiza cada 10 min
    </script>
    </body>
    </html>
    """

    # Write to HTML file with UTF-8 encoding
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html_template)

    print("HTML file updated with latest data.")


def main():
    df, data_dict = fetch_data()
    update_files(df, data_dict)


if __name__ == '__main__':
    main()
