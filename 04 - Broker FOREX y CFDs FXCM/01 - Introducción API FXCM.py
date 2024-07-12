# Importar librerías
import fxcmpy

# API Token
api_token = "API_TOKEN"

# Crear una instancia de la conexión con la API de FXCM
con = fxcmpy.fxcmpy(access_token=api_token, log_level="error")

# Verificar que estamos conectados
if con.is_connected():
    # Obtener detalles de la cuenta
    cuenta_detalles = con.get_accounts()
    print("Detalles de la cuenta:")
    print(cuenta_detalles)

    # Obtener resumen de la cuenta
    cuenta_info = con.get_account_summary()
    print("\nResumen de la cuenta:")
    print(cuenta_info)

    # Obtener lista de instrumentos disponibles
    instrumentos = con.get_instruments()
    print("\nLista de instrumentos:")
    print(instrumentos)
else:
    print("Error al conectar a la API")

# Desconectarse de la API
con.close()

#- Recordatorio:
#   - La API de FXCM también trabaja con token de autentificación que permite el acceso a la cuenta desde Python.
