import requests

def obtener_euribor():
    # Euribor 12 meses - ultimas 24 observaciones del BCE
    url = "https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA?lastNObservations=24&detail=dataonly&format=jsondata"
    try:
        respuesta = requests.get(url, timeout=5)
        datos = respuesta.json()

        # En jsondata las observaciones vienen en una lista de [valor, ...]
        observaciones = datos["dataSets"][0]["series"]["0:0:0:0:0:0:0"]["observations"]
        # Las claves son índices "0", "1", ... el último es el más reciente
        ultimo_indice = str(max(int(k) for k in observaciones.keys()))
        valor = observaciones[ultimo_indice][0]
        return round(valor, 3)
    except Exception as e:
        print(f"⚠️  Error obteniendo Euribor: {e}")
        return 2.407  # fallback

euribor = obtener_euribor()
print(f"Euribor 12M: {euribor}%")