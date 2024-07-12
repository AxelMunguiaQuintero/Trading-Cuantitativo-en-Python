# -*- coding: utf-8 -*-
# Importar librerías
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import pandas as pd
import time


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


# Ejecutar
if __name__ == "__main__":
    
    # Crear instancia de la clase
    ib = InteractiveBrokers()
    # Conectar a IB TWS o IB Gateway (por defecto, TWS usa el puerto 7497 y Gateway usa el puerto 4001)
    ib.connect(host="127.0.0.1", port=7497, clientId=1)    
    # Iniciar hilo que ejecutará la interfaz de eventos de IB
    api_thread = threading.Thread(target=ib.run)
    api_thread.start()
    # Esperar a que la conexión se establezca
    time.sleep(1)
    print("Conexión Activa:", ib.isConnected())
    

    # Solicitar información de la cuenta
    ib.reqAccountSummary(reqId=1, groupName="All", tags="$LEDGER")

    # Crear un contrato para la acción de Apple (AAPL)
    contrato = Contract()
    contrato.symbol = "AAPL"
    contrato.secType = "STK"
    contrato.exchange = "SMART"
    contrato.currency = "USD"
    ib.reqContractDetails(reqId=1, contract=contrato)

    # Solicitar datos históricos para una acción (AAPL)
    fecha_final = ""
    ib.reqMarketDataType(3)
    ib.reqHistoricalData(reqId=1, contract=contrato, endDateTime=fecha_final, 
                         durationStr="5 Y", barSizeSetting="1 day", whatToShow="TRADES", useRTH=1, formatDate=1, 
                         keepUpToDate=False, chartOptions=[])
    time.sleep(1)
    precios_df = pd.DataFrame(ib.precios[1]).set_index("Date")
    precios_df.index = pd.to_datetime(precios_df.index)
    print(precios_df)

    # Solicitar streaming de datos de precios (tick data)
    ib.reqMarketDataType(3)  # Tipo de datos de mercado en tiempo real (Nivel 3 significa datos retrasados)
    ib.reqMktData(1, contrato, "", False, False, [])
    # Esperar para recibir datos (streaming) y mantener el programa en ejecución
    time.sleep(10)
    # Cancelar Solicitud de Streaming
    ib.cancelMktData(1)

    # Crear una orden de mercado para comprar 100 acciones de Apple (AAPL)
    orden = Order()
    orden.action = "BUY"
    orden.totalQuantity = 100
    orden.orderType = "MKT"
    orden.eTradeOnly = ""
    orden.firmQuoteOnly = ""
    # Solicitar último Id válido
    ib.reqIds(-1)
    time.sleep(1)
    ib.placeOrder(orderId=ib.nextOrderId, contract=contrato, order=orden)

    # Solicitar Ganancia/Pérdida de la cuenta
    ib.reqPnL(reqId=1, account="No.Cuenta", modelCode="")

    # Desconectar de IB
    ib.disconnect()
    
    print("Conexión Activa:", ib.isConnected())
