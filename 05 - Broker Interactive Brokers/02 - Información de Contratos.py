# Importar librerías
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
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
        
    
    def contractDetails(self, reqId, contractDetails):
        
        """
        Devuelve los detalles del contrato de un activo
        """
        
        # Imprimir respuesta
        print("Detalles del contrato:\n")
        print(f"Id: {reqId}\n")
        print(f"Contrato: {contractDetails}")
        
        return contractDetails
        
        
        
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
contrato.symbol = "AAPL"
contrato.secType = "STK"
# Tipos de Contratos:
#   "STK": Acciones
#   "FUT": Futuros
#   "IND": Índices
#   "CASH": Divisas
#   "BOND": Bonos
contrato.exchange = "SMART"
# "SMART": Sistema de Enrutamiento Inteligente
# "NYSE": New York Stock Exchange
# "NASDAQ": National Association of Securities Dealers Automated Quotations
# "AMEX": American Stock Exchange
# "CBOE": Chicago Board Options Exchange
# "FOREX": Foreign Exchange Market
contrato.currency = "USD"

# Solicitar información detallada del contrato
contrato_detalles = ib.reqContractDetails(reqId=1, contract=contrato)

# Cerrar conexión
ib.disconnect()

print("Conexión Activa:", ib.isConnected())

# Recordatorio:
#   - La función contractDetails() proporciona detalles completos sobre el contrato del activo, lo que facilita la
#     comprensión de los parámetros y características del contrato solicitado.
#   - Los contratos son fundamentales para una amplia gama de operaciones, como solicitar datos históricos, ejecutar
#     órdenes de mercado y obtener datos en tiempo real. Esto se debe a la extensa variedad de instrumentos disponibles
#     en Interactive Brokers, que requieren una especificación precisa y detallada.
