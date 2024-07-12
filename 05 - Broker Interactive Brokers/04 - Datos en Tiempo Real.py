# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time


# Definir clase
class InteractiveBrokers(EClient, EWrapper):
    
    """
    Clase que facilita la interacción con la API de InteractiveBrokers.
    """
    
    def __init__(self):
        
        """
        Constructor
        """
        
        # Inicializar la clase base EClient
        EClient.__init__(self, self)
        
        
    def error(self, reqId, errorCode, errorString):
        
        """
        Método que gestiona los errores que suceden en nuestra aplicación o en nuestras peticiones
        """
        
        # Error
        print(f"Error {reqId} {errorCode}: {errorString}")
        
        
    def tickPrice(self, reqId, tickType, price, attrib):
        
        """
        Método que recibe los precios en tiempo real (datos retrasados)
        """
        
        # Mostrar el precio y el tipo
        print(f"Tick Price. TickerId: {reqId}, Type: {tickType}, Precio: {price}")
        
        
# Crear una instancia
ib = InteractiveBrokers()
# Conectarnos a IB TWS o IB Gateway (por defecto, TWS usa el puerto 7497 y Gateway usa el puerto 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
# Inicializar hilo que ejecutará la conexión
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Conexión Activa:", ib.isConnected())

# Crear un contrato para la acción
contrato = Contract()
contrato.symbol = "AMZN"
contrato.secType = "STK"
contrato.exchange = "SMART"
contrato.currency = "USD"

# Solicitar streaming de datos de precios
ib.reqMarketDataType(3)
ib.reqMktData(reqId=1, contract=contrato, genericTickList="", snapshot=False, regulatorySnapshot=False, mktDataOptions=[])

# Esperar para recibir datos y cesar su ejecución
time.sleep(10)

# Cancelar el streaming
ib.cancelMktData(reqId=1)

# Desconectarnos de IB 
ib.disconnect()

# Recordatorio:
#   - El acceso a datos en tiempo real requiere de suscripciones pagadas. Sin embargo, podemos acceder a datos en tiempo
#     real, pero que tengan un retraso de tiempo (entre 10 y 20 minutos).
