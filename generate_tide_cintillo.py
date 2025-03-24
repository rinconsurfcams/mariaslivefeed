
import json
from datetime import datetime

def hora_a_minutos(hora_str):
    t = datetime.strptime(hora_str, "%I:%M %p")
    return t.hour * 60 + t.minute

with open("overlay_tides.json", "r", encoding="utf-8") as f:
    overlay_data = json.load(f)

now = datetime.strptime(overlay_data["timestamp"], "%Y-%m-%d %H:%M:%S")
now_minutes = now.hour * 60 + now.minute

for p in overlay_data["tide_predictions"]:
    p["minutes"] = hora_a_minutos(p["time"])

# Ordenar por minutos por si acaso no vienen ordenadas
overlay_data["tide_predictions"].sort(key=lambda p: p["minutes"])

past = [p for p in overlay_data["tide_predictions"] if p["minutes"] < now_minutes]
future = [p for p in overlay_data["tide_predictions"] if p["minutes"] >= now_minutes]

last = past[-1] if past else None
next_tide = future[0] if future else None

# Lógica flexible para determinar la tendencia
if last and next_tide:
    if last["type"] == "Baja" and next_tide["type"] == "Alta":
        trend = "SUBIENDO"
    elif last["type"] == "Alta" and next_tide["type"] == "Baja":
        trend = "BAJANDO"
    else:
        trend = "CAMBIANTE"
elif next_tide and next_tide["type"] == "Alta":
    trend = "SUBIENDO"
elif next_tide and next_tide["type"] == "Baja":
    trend = "BAJANDO"
else:
    trend = "NO DISPONIBLE"

next_high = next((p for p in future if p["type"] == "Alta"), None)
next_low = next((p for p in future if p["type"] == "Baja"), None)

high_text = f"{next_high['height_ft']} pies @ {next_high['time']}" if next_high else "N/A"
low_text = f"{next_low['height_ft']} pies @ {next_low['time']}" if next_low else "N/A"

html_cintillo = f"""<div id='tide-ticker' style='
  position: absolute;
  bottom: 0;
  width: 100%;
  background: rgba(0, 0, 128, 0.5);
  color: white;
  font-family: Helvetica, Arial, sans-serif;
  font-size: 17px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  z-index: 9999;
  padding: 6px 0;
'>
  <div id='tide-content' style='
    display: inline-block;
    padding-left: 100%;
    animation: scroll-left 25s linear infinite;
  '>
    🌊 Marea {trend} | 📈 Alta: {high_text} | 📉 Baja: {low_text} | ⏱️ {overlay_data["timestamp"]}
  </div>
</div>

<style>
@keyframes scroll-left {{
  0%   {{ transform: translateX(0%); }}
  100% {{ transform: translateX(-100%); }}
}}
</style>"""

with open("tide_overlay_cintillo.html", "w", encoding="utf-8") as f:
    f.write(html_cintillo)

print("✅ tide_overlay_cintillo.html generado correctamente.")
