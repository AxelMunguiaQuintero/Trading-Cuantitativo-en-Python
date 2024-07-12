# Importar librerías
import tpqoa
import pandas as pd
import numpy as np
import threading 
import time


# Conexión
archivo_config = "config.cfg"
oanda = tpqoa.tpqoa(conf_file=archivo_config)

# Parámetros
ticker = "EUR_USD"
n_precios = 5 

# Streaming 
try:
    oanda.stream_data(instrument=ticker, stop=n_precios)
except Exception as error:
    print("El tiempo de espera para un nuevo precio se ha excedido. Error ->", error)
    
# Crear un DataFrame para almacenar los precios
df_precios = pd.DataFrame(columns=["time", "bid", "ask"])

# Función
def on_success(ticker, time_, bid, ask):
    
    """
    Función que se mandará a llamar cada vez que se reciba un tick de información
    """
    
    global df_precios
    # Crear un nuevo registro con los datos recibidos
    nuevo_registro = pd.DataFrame(data = [[time_, bid, ask]], columns=["time", "bid", "ask"])
    # Añadir el nuevo registro a los datos existentes
    df_precios = pd.concat([df_precios, nuevo_registro], ignore_index=True)
    # Imprimir los precios recibidos
    print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
    
# Streaming con la función on_success
try:
    oanda.stream_data(instrument=ticker, stop=n_precios, callback=on_success)
    print(df_precios)
except Exception as error:
    print("El tiempo de espera para un nuevo precio se ha excedido. Error ->", error)
    
# Hacer Manual
datos = pd.DataFrame(columns=["time", "bid", "ask"])
detener_streaming = False
def streaming_datos(ticker, n) -> None:
    
    """
    Método que se encarga de darle tratamiento a los datos recibidos
    """
    
    contador = 0
    while contador <= n:
        time_, bid, ask = oanda.get_prices(instrument=ticker)
        print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
        nuevo_registro = pd.DataFrame(data = [[time_, bid, ask]], columns=["time", "bid", "ask"])
        # Concactenar
        global datos
        datos = pd.concat([datos, nuevo_registro], ignore_index=True)
        # Revisar si cesar la ejecución
        global detener_streaming
        if detener_streaming:
            break
        else:
            time.sleep(1)
        # Incrementar el contador
        contador += 1
        
# Ejecutar función
streaming_datos(ticker=ticker, n=5)
print(datos)
    
# Ejecutar infinitamente en paralelo
threading.Thread(target=streaming_datos, args=(ticker, np.inf)).start()
time.sleep(15)
detener_streaming = True    
    
# Recordatorio:
#   - Es vital dar un correcto tratamiento a la información que se recibe en tiempo real y crear una estructura adecuada
#     que nos permita seguir ejecutando nuestro programa.
