
import json
from datetime import datetime

with open("overlay_tides.json", "r", encoding="utf-8") as f:
    data = json.load(f)

predicciones = data["tide_predictions"]
ahora = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
minutos_ahora = ahora.hour * 60 + ahora.minute

def hora_a_minutos(hora_str):
    t = datetime.strptime(hora_str, "%I:%M %p")
    return t.hour * 60 + t.minute

for p in predicciones:
    p["minutos"] = hora_a_minutos(p["time"])

pasadas = [p for p in predicciones if p["minutos"] < minutos_ahora]
futuras = [p for p in predicciones if p["minutos"] >= minutos_ahora]

ultima = pasadas[-1] if pasadas else None
siguiente = futuras[0] if futuras else None
tendencia = "SUBIENDO" if ultima and siguiente and ultima["type"] == "Baja" and siguiente["type"] == "Alta" else "BAJANDO"

proxima_alta = next((p for p in futuras if p["type"] == "Alta"), None)
proxima_baja = next((p for p in futuras if p["type"] == "Baja"), None)

html_content = f"""
<div id='tide-ticker' style='position: absolute; bottom: 0; width: 100%; background: rgba(0, 0, 128, 0.85); color: white; font-size: 18px; font-weight: bold; white-space: nowrap; overflow: hidden; z-index: 9999; padding: 5px 0;'>
  <div id='tide-content' style='display: inline-block; padding-left: 100%; animation: scroll-left 20s linear infinite;'>
    🌊 Marea {tendencia} | 📈 Alta: {proxima_alta["height_ft"]:.2f} pies @ {proxima_alta["time"]} | 📉 Baja: {proxima_baja["height_ft"]:.2f} pies @ {proxima_baja["time"]} | ⏱️ {data["timestamp"]}
  </div>
</div>

<style>
@keyframes scroll-left {
  0% { transform: translateX(0%); }
  100% { transform: translateX(-100%); }
}
</style>
"""

with open("overlay_tides_static.html", "w", encoding="utf-8") as f:
    f.write(html_content)
