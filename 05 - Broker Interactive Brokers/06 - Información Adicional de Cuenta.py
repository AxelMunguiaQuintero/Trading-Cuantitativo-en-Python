# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient # Clase que maneja la comunicación hacia el servidor de IB
from ibapi.wrapper import EWrapper # Clase que recibe la respuesta del servidor y la procesa
import threading


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
        
    
    def accountSummary(self, reqId, account, tag, value, currency):
        
        """
        Recibe la información de la cuenta
        """
        
        # Imprimir información
        print(f"Account Summary - Account: {account}, Tag: {tag}, Value: {value}, Currency: {currency}")
        
        
    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        
        """
        Este método devuelve la Ganancia/Pérdida de la cuenta.
        """
        
        # Mostrar por consola
        print("ReqId:", reqId, "\n",
              "Ganancia/Pérdida Diaria:", dailyPnL, "\n",
              "Ganancia/Pérdida No realizada:", unrealizedPnL, "\n",
              "Ganancia/Pérdida Realizada:", realizedPnL)
        
        
# Crear una instancia
ib = InteractiveBrokers()
# Conectarnos a IB TWS o IB Gateway (por defecto, TWS usa el puerto 7497 y Gateway usa el puerto 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
# Inicializar hilo que ejecutará la conexión
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Conexión Activa:", ib.isConnected())

# Solicitar la informacón de la cuenta
ib.reqAccountSummary(reqId=1, groupName="All", tags="$LEDGER")

# Solicitar Ganancia/Pérdida de la cuenta
ib.reqPnL(reqId=2, account="No.Cuenta", modelCode="")

# Recordatorio:
#   - La mayoría de los métodos de la clase base EWrapper deben de reescribirse para un correcto procesamiento de información.
