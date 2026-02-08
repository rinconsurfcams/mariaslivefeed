<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>CariCOOS Live Data</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background: transparent; }
        #overlay {
            position: fixed;
            top: 20px; left: 20px;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: white;
            background: rgba(0, 0, 0, 0.85); 
            padding: 15px; border-radius: 8px;
            border-left: 5px solid #00D2FF; 
            min-width: 280px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .header { font-size: 0.8em; margin-bottom: 10px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 5px; }
        .data-row { margin-bottom: 8px; display: flex; align-items: center; font-size: 1.1em; }
        .label { width: 110px; opacity: 0.8; font-size: 0.9em; }
        .value { font-weight: bold; color: #00D2FF; }
        .footer { margin-top: 10px; font-size: 0.7em; opacity: 0.6; text-align: left; }
    </style>
</head>
<body>
    <div id="overlay">
        <div class="header">📍 BOYA RINCÓN - DATOS EN VIVO</div>
        <div id="content">
            <div class="data-row"><span class="label">Swell Hs:</span><span id="wave-h" class="value">--</span> FT @ <span id="wave-p" class="value">--</span>s</div>
            <div class="data-row"><span class="label">Desde (Dir):</span><span id="wave-card" class="value">--</span> <span id="wave-d" style="margin-left:5px; opacity:0.7">(--°)</span></div>
            <div class="data-row"><span class="label">Viento:</span><span id="wind-s" class="value">--</span> KTS <span id="wind-d" style="margin-left:5px; opacity:0.7">(--°)</span></div>
        </div>
        <div class="footer">FUENTE: CARICOOS.ORG</div>
    </div>

    <script>
        // Función para convertir grados geográficos (0-360) a puntos cardinales
        function getCardinal(angle) {
            const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
            return directions[Math.round(angle / 22.5) % 16];
        }

        async function updateOverlay() {
            try {
                const response = await fetch(`overlay.json?t=${Date.now()}`);
                const data = await response.json();
                
                document.getElementById("wave-h").innerText = data.wave_height_ft;
                document.getElementById("wave-p").innerText = data.wave_period;
                
                // Dirección del Swell: De donde viene (ej. 344 = NNW)
                document.getElementById("wave-d").innerText = `(${data.wave_direction}°)`;
                document.getElementById("wave-card").innerText = getCardinal(data.wave_direction);
                
                document.getElementById("wind-s").innerText = data.wind_speed;
                document.getElementById("wind-d").innerText = `(${data.wind_direction}°)`;
            } catch (e) { console.error("Error:", e); }
        }
        updateOverlay();
        setInterval(updateOverlay, 60000);
    </script>
</body>
</html>
