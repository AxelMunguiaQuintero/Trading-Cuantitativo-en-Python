# -*- coding: utf-8 -*-
# Importar librerías
import fxcmpy

# API obtenida de FXCM
api_token = "API_TOKEN"

# Crear una instancia de la conexión con la API de FXCM
con = fxcmpy.fxcmpy(access_token=api_token, log_level="error")

# Verificar que estamos conectados
if con.is_connected():
    
    # Obtener datos históricos de mercado para EUR/USD
    instrumento = "EUR/USD"
    periodo = "D1"  # Periodo de las velas (D1 = diario)
    numero_velas = 100  # Número de velas a obtener

    # Obtener cierto número de velas
    datos = con.get_candles(instrumento, period=periodo, number=numero_velas)
    print(f"Datos más recientes de {instrumento}:")
    print(datos)
    
    # Obtener datos entre fechas
    inicio = "2023-01-01"
    final = "2024-01-01"
    precios = con.get_candles(instrumento, start=inicio, end=final, period=periodo)
    print(f"Datos históricos de {instrumento}:")
    print(precios)
    
    # Marcos de Tiempo Disponibles
    # "m1", "m5", "m15", "m30", "H1", "H2", "H3", "H4", "H6", "H8", "D1", "W1", "M1"
    
    # Obtener Precio más Reciente
    precio_actual = con.get_last_price(instrumento)
    print(f"El precio más reciente de {instrumento} es:")
    print(precio_actual)
    
else:
    print("Error al conectar a la API")

# Desconectarse de la API
con.close()

#- Recordatorio:
#   - Existe una limitación de 10 mil filas de información cuando se realiza una consulta.
