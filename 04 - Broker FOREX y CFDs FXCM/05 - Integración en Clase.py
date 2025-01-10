# -*- coding: utf-8 -*-
# Importar librerías
import fxcmpy
import pandas as pd
import time
import threading


# Definir Clase
class FXCM:

    """
    Clase que facilita la interacción con la API de FXCM.
    """
    
    def __init__(self, token: str) -> None:
        
        """
        Constructor.
        """
        
        self.token_api = token
        self.conexion = fxcmpy.fxcmpy(access_token=self.token_api, log_level='error')
        self.precios = {}
        self.streaming = {}
        self.detener_streaming = False
    
    
    def info_cuenta(self) -> dict:
        
        """
        Devuelve la información relacionada con la cuenta.
        """
        
        return self.conexion.get_accounts().T.to_dict()


    def instrumentos(self) -> list:
        
        """
        Devuelve una lista con los instrumentos disponibles en FXCM.
        """
        
        return self.conexion.get_instruments()


    def obtener_datos_historicos(self, simbolos, inicio, fin, periodo) -> None:
        
        """
        Obtiene datos históricos para un símbolo o varios.
        """
        
        simbolos = [simbolos] if not isinstance(simbolos, list) else simbolos
        for simbolo in simbolos:
            datos = self.conexion.get_candles(simbolo, period=periodo, start=inicio, stop=fin)
            self.precios[simbolo] = datos


    def streaming_datos(self, simbolo: str, n: int) -> None:
        
        """
        Método que procesa los datos de streaming.
        """
        
        # Revisar si ya existe el ticker
        if simbolo not in self.streaming:
            self.streaming[simbolo] = pd.DataFrame(columns=["fecha", "bid", "ask"])
            
        contador = 0
        while contador <= n:
            precios = self.conexion.get_last_price(simbolo)
            fecha = precios.index[0]
            bid, ask = precios["Bid"], precios["Ask"]
            nueva_fila = pd.DataFrame([[fecha, bid, ask]], columns=["fecha", "bid", "ask"])
            self.streaming[simbolo] = pd.concat([self.streaming[simbolo], nueva_fila], ignore_index=True)
            if self.detener_streaming:
                break
            else:
                time.sleep(1)
            contador += 1
            
    def streaming_paralelo(self, simbolo: str, n: int) -> None:
        
        """
        Función que paraleliza la ejecución del método 'streaming_datos'
        """
        
        threading.Thread(target=self.streaming_datos, args=(simbolo, n)).start()
          
        
# Ejecutar
if __name__ == "__main__":
    # Instanciar
    fxcm = FXCM(token="API_TOKEN")
    # Obtener Información de la Cuenta
    print("\nInformación de la Cuenta:\n")
    print(fxcm.info_cuenta())
    # Obtener Instrumentos
    print("\nInstrumentos:\n")
    print(fxcm.instrumentos())
    # Obtener Datos Históricos
    print("\nDatos Históricos:\n")
    fxcm.obtener_datos_historicos(simbolos=["EUR/USD", "XAU/USD"], inicio="2023-01-01", fin="2024-01-01", periodo="D1")
    print(fxcm.precios["EUR/USD"])
    print(fxcm.precios["XAU/USD"])
    # Streaming de Datos
    print("\nStreaming de Datos:\n")
    fxcm.streaming_datos(simbolo="EUR/USD", n=10)
    print(fxcm.streaming["EUR/USD"])
    # Streaming de Datos Paralelizado
    print("\nStreaming de Datos Paralelizado:\n")
    fxcm.streaming_paralelo(simbolo="EUR/USD", n=1000000)
    time.sleep(10)
    fxcm.detener_streaming = True
