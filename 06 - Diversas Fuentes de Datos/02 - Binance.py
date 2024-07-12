# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import requests

# Definir urls
url_base = "https://api.binance.com"
conectividad_endpoint = "/api/v3/ping"
instrumentos_endpoint = "/api/v3/exchangeInfo"
datos_endpoint = "/api/v3/klines"

# Comprobar Conectividad
r = requests.get(url=url_base + conectividad_endpoint)
contenido = r.json()
if contenido == {}:
    print("Conectividad con la API de Binance fue comprobada con éxito")
    

# Obtener lista de símbolos
r = requests.get(url=url_base + instrumentos_endpoint)
contenido = r.json()
instrumentos_lista = []
for instrumento in contenido["symbols"]:
    instrumentos_lista.append(instrumento["symbol"])
print(len(instrumentos_lista))
print(instrumentos_lista[:10])
    

# Obtener Datos históricos
def obtener_datos(ticker, fecha_inicio, fecha_final, intervalo) -> pd.DataFrame:
    
    """
    Obtiene datos históricos para un activo mediante la API de Binance.
    """
    
    # Realizar la petición
    params = {
        "symbol": ticker,
        "interval": intervalo,
        "startTime": int(pd.to_datetime(fecha_inicio).timestamp() * 1_000),
        "limit": 1_000
        }
    if fecha_final:
        params["endTime"] = int(pd.to_datetime(fecha_final).timestamp() * 1_000)
        
    r = requests.get(url=url_base + datos_endpoint, params=params)
    contenido = r.json()
    precios = []
    for dato in contenido:
        fecha = pd.to_datetime(dato[0], unit="ms")
        precio_open = float(dato[1])
        precio_high = float(dato[2])
        precio_low = float(dato[3])
        precio_close = float(dato[4])
        volume = float(dato[5])
        precios.append([fecha, precio_open, precio_high, precio_low, precio_close, volume])
        
    # Convertir a DataFrame
    df = pd.DataFrame(data=precios, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    df.set_index("Date", inplace=True)
    
    return df


# Descargar Datos
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final="2024-01-01", intervalo="1d")
print(df)    
    
# Información en diferentes intervalos

# Datos en intervalos de 1 segundo
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="1s")
print(df)
# Datos en intervalos de 1 minuto
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="1m")
print(df)
# Datos en intervalos de 15 minutos
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="15m")
print(df)
# Datos en intervalos de 1 hora
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="1h")
print(df)
# Datos en intervalos de 6 horas
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="6h")
print(df)
# Datos en intervalos de 12 horas
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="12h")
print(df)
# Datos en intervalos de 1 día
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="1d")
print(df)
# Datos en intervalos de 1 Mes
df = obtener_datos(ticker="BTCUSDT", fecha_inicio="2022-01-01", fecha_final=None, intervalo="1M")
print(df)

# Recordatorio:
#   - La API de Binance permite obtener datos en varios intervalos de tiempo, lo cual es útil para diferentes
#     tios de análisis y estrategias de trading.
