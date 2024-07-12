# Importar librerías
import tpqoa
import pandas as pd
import time
import threading


# Definir clase
class Oanda:
    
    """
    Clase que facilita la interacción con la API de OANDA.
    """
    
    def __init__(self, conf_file: str) -> None:
        
        """
        Constructor.
        """
        
        self.conf_file = conf_file
        self.oanda_api = tpqoa.tpqoa(conf_file=self.conf_file)
        self.precios = {}   
        self.streaming = {}
        self.detener_streaming = False
        
        
    def info_cuenta(self) -> dict:
        
        """
        Devuelve la información relacionada con la cuenta.
        """
        
        return self.oanda_api.get_account_summary()
    
    
    def instrumentos(self) -> list:
        
        """
        Devuelve una lista con los instrumentos disponibles en OANDA.
        """
        
        return self.oanda_api.get_instruments()
    
    
    def obtener_datos(self, tickers, inicio, final, granulidad) -> None:
        
        """
        Obtiene datos históricos para un ticker o un conjunto de ellos.
        """
        
        # Descargar datos
        tickers = [tickers] if not isinstance(tickers, list) else tickers
        
        for instrument in tickers:
            precios = self.oanda_api.get_history(instrument=instrument, start=inicio, end=final, 
                                                 granularity=granulidad, price="M")
            self.precios[instrument] = precios
            
    
    def streaming_datos(self, ticker: str, n: int) -> None:
        
        """
        Método que se encarga de darle tratamiento a los datos recibidos
        """
    
        # Revisar si ya existe el ticker
        if ticker not in self.streaming:
            self.streaming[ticker] = pd.DataFrame(columns=["time", "bid", "ask"])
        contador = 0
        while contador <= n:
            time_, bid, ask = self.oanda_api.get_prices(instrument=ticker)
            print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
            nuevo_registro = pd.DataFrame([[time_, bid, ask]], columns=["time", "bid", "ask"])
            # Concatenar
            self.streaming[ticker] = pd.concat([self.streaming[ticker], nuevo_registro], ignore_index=True)
            # Revisar si cesar ejecución
            if self.detener_streaming:
                break
            else: 
                time.sleep(1)
            # Incrementar contador
            contador += 1
            
            
    def streaming_datos_paralelizado(self, ticker: str, n: int) -> None:
        
        """
        Función que paraleliza la ejecución del método 'streaming_datos'
        """
       
        # Paralelizar
        threading.Thread(target=self.streaming_datos, args=(ticker, n)).start()
