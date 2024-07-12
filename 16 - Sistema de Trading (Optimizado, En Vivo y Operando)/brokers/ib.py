# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

# Definir clase
class InteractiveBrokers(EClient, EWrapper):
    
    """
    Clase que facilita la interacción con la API de InteractiveBrokers.
    """
    
    def __init__(self) -> None:
        
        """
        Constructor.
        """
        
        # Inicializar Cliente
        EClient.__init__(self, self)
        # Atributos
        self.precios = {}
        self.nextOrderId = None


    def error(self, reqId, errorCode, errorString):
        
        """
        Función de manejo de errores.
        """
        
        print(f"Error {reqId} {errorCode} {errorString}")
        

    def accountSummary(self, reqId, account, tag, value, currency):
        
        """
        Recibe información de la cuenta.
        """
        
        print(f"Account Summary - Account: {account}, Tag: {tag}, Value: {value}, Currency: {currency}")


    def contractDetails(self, reqId, contractDetails):
        
        """
        Devuelve los detalles del contrato de un activo.
        """
        
        print("Detalles del Contrato:\n")
        print(f"Id: {reqId}\n")
        print(f"Contrato: {contractDetails}")


    def historicalData(self, reqId, bar):
        
        """
        Recibe los datos históricos de un activo y los guarda en un diccionario.
        """
        
        datos = {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "Volume": bar.volume}
        if reqId not in self.precios:
            self.precios[reqId] = []
        self.precios[reqId].append(datos)


    def historicalDataEnd(self, reqId, start, end):
        
        """
        Método llamado una vez que se han recibido todos los datos históricos.
        """
        
        print(f"Datos descargados para Id: {reqId}, En el periodo: {start}-{end}")


    def tickPrice(self, reqId, tickType, price, attrib):
        
        """
        Método que recibe los precios en tiempo real (Datos retrasados).
        """
        
        print(f"Tick Price. TickerId: {reqId}, Type: {tickType}, Price: {price}")


    def nextValidId(self, orderId: int):
        
        """
        Obtiene el siguiente Id válido para ejecutar una órden.
        """
        
        self.nextOrderId = orderId


    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        
        """
        Método llamado cada vez que el estado de una orden cambia en el servidor.
        """
        
        print(f"Order Status - OrderId: {orderId}, Status: {status}")


    def openOrder(self, orderId, contract, order, orderState):
        
        """
        Método que devuelve las órdenes abiertas de nuestra cuenta.
        """
        
        print("Orden Id:", orderId, "Orden:", order, "Status:", orderState)


    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):
        
        """
        Método que devuelve la Ganancia/Pérdida de la cuenta.
        """
        
        print("ReqId:", reqId, "\n",
              "Ganancia/Pérdida Diaria:", dailyPnL, "\n",
              "Ganancia/Pérdida No Realizada:", unrealizedPnL, "\n",
              "Ganancia/Pérdida Realizada:", realizedPnL)
