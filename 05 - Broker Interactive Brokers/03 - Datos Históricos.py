# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import pandas as pd

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
        # Diccionario donde se guardarán los precios
        self.precios = {}
        
        
    def error(self, reqId, errorCode, errorString):
        
        """
        Método que gestiona los errores que suceden en nuestra aplicación o en nuestras peticiones
        """
        
        # Error
        print(f"Error {reqId} {errorCode}: {errorString}")
        
        
    def historicalData(self, reqId, bar):
        
        """
        Recibe los datos históricos de un activo y los guarda en un diccionario
        """
        
        datos = {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "volume": bar.volume}
        if reqId not in self.precios:
            self.precios[reqId] = []
        # Apprendizar los datos
        self.precios[reqId].append(datos)
        
    
    def historicalDataEnd(self, reqId, start, end):
        
        """
        Este método se manda a llamar una vez que se han recibido todos los datos.
        """
        
        # Imprimir que ha finalizado
        print(f"Datos descargados para ID: {reqId}, En el periodo {start}-{end}")
        

# Crear una instancia
ib = InteractiveBrokers()
# Conectarnos a IB TWS o IB Gateway (por defecto, TWS usa el puerto 7497 y Gateway usa el puerto 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
# Inicializar hilo que ejecutará la conexión
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Conexión Activa:", ib.isConnected())

# Crear un contrato
contrato_accion = Contract()
contrato_accion.symbol = "AAPL"
contrato_accion.secType = "STK"
contrato_accion.exchange = "SMART"
contrato_accion.currency = "USD"

# Ejecutar el comando
fecha_final = ""
ib.reqMarketDataType(3)
ib.reqHistoricalData(reqId=1, contract=contrato_accion, endDateTime=fecha_final, durationStr="5 Y", 
                     barSizeSetting="1 day", whatToShow="TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
                     chartOptions=[])

# Obtener datos
precios = pd.DataFrame(data=ib.precios[1])
precios["Date"] = pd.to_datetime(precios["Date"])
precios.set_index("Date", inplace=True)
print(precios)

# Recordatorio:
#   - El acceso a datos históricos en Interactive Brokers requiere de un procesamiento de datos adecuado para su uso y análisis.
