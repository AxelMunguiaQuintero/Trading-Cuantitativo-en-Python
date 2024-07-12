# Importar librerías
import threading
import time
# Librerías Propias
from brokers.oanda import Oanda
from brokers.fxcm import FXCM
from brokers.ib import InteractiveBrokers

# Definir clase
class Brokers:
    
    """
    Clase que nos permite acceder a cada una de las clases que hemos programado para diferentes brokers
    """
    
    def __init__(self):
        
        """
        Constructor
        """
        
        self.oanda = None
        self.fxcm = None
        self.ib = None
        
        
    def Inicializar_Oanda(self, config_file: str) -> None:
        
        """
        Genera una conexión con Oanda.
        """
        
        # Generar conexión
        oanda_api = Oanda(conf_file=config_file)
        self.oanda = oanda_api
        
       
    def Inicializar_FXCM(self, token: str) -> None:
        
        """
        Genera una conexión con FXCM.
        """
        
        # Generar conexión
        fxcm_api = FXCM(token=token)
        self.fxcm = fxcm_api
        
    
    def Inicializar_IB(self, localhost: str = "127.0.0.1", port: int = 7497, clientId: int = 1) -> None:
        
        """
        Genera una conexión con IB.
        """
        
        # Crear instancia de la clase
        ib = InteractiveBrokers()
        # Conexión a IB TWS o IB Gateway
        ib.connect(host=localhost, port=port, clientId=clientId)
        # Inicializar hilo que ejecutará la interfaz de eventos de IB
        api_thread = threading.Thread(target=ib.run)
        api_thread.start()
        # Esperar a que la conexión se establezca
        time.sleep(1)
        self.ib = ib
        

# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Generar conexión con algún broker
    config_file_oanda = "brokers/credenciales/config.cfg"
    brokers = Brokers()
    brokers.Inicializar_Oanda(config_file_oanda)  
    # Hacer una petición de los instrumentos
    print(brokers.oanda.instrumentos())      
