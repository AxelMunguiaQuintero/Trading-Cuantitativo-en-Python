# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient # Clase que maneja la comunicación hacia el servidor de IB
from ibapi.wrapper import EWrapper # Clase que recibe la respuesta del servidor y la procesa
from ibapi.contract import Contract
from ibapi.order import Order
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
        
        
    def nextValidId(self, orderId):
        
        """
        Obtiene el siguiente ID válido para ejecutar una órden de mercado
        """
        
        # Guardar como atributo
        self.nextOrderId = orderId
        
    
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        
        """
        Este método se llama automáticamente cada vez que el estado de una orden cambie en el servidor
        """
        
        # Mostrarlo por consola
        print(f"Estatus de la Operación - OrderId: {orderId}, Status: {status}")
        
    
    def openOrder(self, orderId, contract, order, orderState):
        
        """
        Este método devuelve las órdenes abiertas de nuestra cuenta
        """
        
        # Mostrar la información
        print("OrderId:", orderId, "Orden:", order, "Status:", orderState)
        
        
# Crear una instancia
ib = InteractiveBrokers()
# Conectarnos a IB TWS o IB Gateway (por defecto, TWS usa el puerto 7497 y Gateway usa el puerto 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
# Inicializar hilo que ejecutará la conexión
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Conexión Activa:", ib.isConnected())

# Crear contrato
contrato = Contract()
contrato.symbol = "MSFT"
contrato.secType = "STK"
contrato.exchange = "SMART"
contrato.currency = "USD"

# Crear una orden
orden = Order()
orden.action = "BUY" # "SELL"
orden.totalQuantity = 100
orden.orderType = "MKT"
# orden.orderType = "LMT"
# orden.lmtPrice = 428
orden.eTradeOnly = ""
orden.firmQuoteOnly = ""

# Solicitar el id
ib.reqIds(-1)
print(ib.nextOrderId)


# Enviar la orden al mercado
ib.placeOrder(orderId=ib.nextOrderId, contract=contrato, order=orden)

# Obtener órdenes abiertas
ib.reqOpenOrders()

# Recordatorio:
#   - Para que se puedan ejecutar órdenes desde Python debemos deshabilitar la casilla de "API Solo Lectura".
