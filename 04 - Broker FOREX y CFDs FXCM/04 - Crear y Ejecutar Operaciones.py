# Importar librerías
import fxcmpy
import time

# Clave API
api_token = "API_TOKEN"

# Crear una instancia de la conexión con la API de FXCM
con = fxcmpy.fxcmpy(access_token=api_token, log_level="error")

# Verificar que estamos conectados
if con.is_connected():
    # Definir el instrumento y los parámetros de la orden
    instrumento = "EUR/USD"
    cantidad = 10  # Tamaño de la posición (en lotes)
    es_compra = True  # True para compra, False para venta
    tipo_orden = "AtMarket"  # Tipo de orden

    # Enviar orden de compra
    orden = con.open_trade(symbol=instrumento, is_buy=es_compra, amount=cantidad, time_in_force="GTC", order_type=tipo_orden)
    print(f"Orden enviada para {instrumento}:")
    
    # Esperar a que se ejecute
    time.sleep(1)

    # Mostrar detalles de la orden
    print(orden)

    # Obtener posiciones abiertas
    posiciones_abiertas = con.get_open_positions()
    print("\nPosiciones abiertas:")
    print(posiciones_abiertas)

    # Cerrar la posición después de un tiempo
    time.sleep(10)  # Esperar 10 segundos antes de cerrar la posición

    # Revisar que hay posiciones abiertas
    if not posiciones_abiertas.empty:
        id_posicion = posiciones_abiertas.iloc[0]["tradeId"]  # Obtener el ID de la posición
        con.close_trade(trade_id=id_posicion, amount=cantidad)
        print(f"\nPosición {id_posicion} cerrada.")
    
    # Obtener posiciones abiertas después de cerrar
    posiciones_abiertas = con.get_open_positions()
    print("\nPosiciones abiertas después de cerrar:")
    print(posiciones_abiertas)

else:
    print("Error al conectar a la API")

# Desconectarse de la API
con.close()

#- Recordatorio: 
#   - La gestión de creación y ejecución de órdenes debe de realizarse con mucho cuidado. 
