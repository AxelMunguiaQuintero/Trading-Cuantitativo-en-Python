# -*- coding: utf-8 -*-
# Importar librerías
import fxcmpy
import time

# API Token de FXCM
api_token = "API_TOKEN"

# Crear una instancia de la conexión con la API de FXCM
con = fxcmpy.fxcmpy(access_token=api_token, log_level="error")

# Callback para procesar los datos de streaming
def print_data(data, dataframe):
    print("Datos recibidos:")
    # Imprimir la última fila de datos
    print(dataframe.tail(1)) 

# Verificar que estamos conectados
if con.is_connected():
    # Instrumento a suscribirse
    instrumento = "EUR/USD"

    # Suscribirse al instrumento (Esto empezará a recibir los datos)
    con.subscribe_market_data(instrumento, (print_data,))
    print(f"Suscrito a los datos de {instrumento}.")

    # Tiempo de inicio
    inicio_tiempo = time.time()
    duracion = 30  # Duración en segundos

    # Mantener el script en ejecución y recibir datos durante el tiempo especificado
    while time.time() - inicio_tiempo < duracion:
        time.sleep(1)  # Espera 1 segundo entre iteraciones

    # Desuscribirse y cerrar la conexión después de 30 segundos
    con.unsubscribe_market_data(instrumento)
    con.close()
    print("Desconectado y suscripción cancelada después de 30 segundos.")
    
else:
    print("Error al conectar a la API")

#- Recordatorio:
#   - Se debe de dar un correcto tratamiento a los datos recibidos en tiempo real para poderlos aprovechar adecuadamente.
