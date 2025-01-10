# -*- coding: utf-8 -*-
# Importar librerías
import tpqoa 
import json
import configparser
import os

# Crear un documento con las credenciales
config = configparser.ConfigParser()

# Agregar la sección y las opciones con sus valores
config["oanda"] = {
    "account_id": "numero_cuenta",
    "access_token": "TOKEN",
    "account_type": "practice"
    }

# Crear el archivo de configuración
archivo = "config.cfg"
if not os.path.isfile(archivo):
    with open(archivo, "w") as configfile:
        config.write(configfile)
        
# Conectar a OANDA
oanda = tpqoa.tpqoa(conf_file=archivo)

# Imprimir Datos de Conexión
print("Número de Cuenta:", oanda.account_id)
print("Token de Acceso:", oanda.access_token)
print("Tipo de Cuenta:", oanda.account_type)
print("Hostname:", oanda.hostname)

# Obtener Información de la Cuenta
cuenta_info = oanda.get_account_summary()
print(json.dumps(cuenta_info, indent=4))

# Instrumentos Disponibles
instrumentos = oanda.get_instruments()
for nombre, ticker in instrumentos:
    print(f"Nombre del Instrumento: {nombre} / Ticker: {ticker}")
    
print("Número total de instrumentos:", len(instrumentos))

# Recordatorio:
#   - La librería de tpqoa es un wrapper de la librería oficial de OANDA (v20) que facilita el acceso a la API REST de OANDA.
