# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
# Librerías Propias
from Brokers import Brokers
from AnalisisTecnico import Multiples_Estrategias
from AnalisisSentimiento import Sentimiento_Mercado

# Definir sistema de trading intradía
def Sistema_Intradia() -> None:
    
    """
    Ejecuta una estrategia de trading intradía (cada 1 minuto).
    """
    
    # Instancia de Brokers
    brokers = Brokers()
    # Conectar a Oanda
    archivo_conexion = "brokers/credenciales/config.cfg"
    brokers.Inicializar_Oanda(config_file=archivo_conexion)
    # Definir universo de instrumentos financieros
    instrumentos_tuplas = brokers.oanda.instrumentos()
    instrumentos_oanda = [i[1] for i in instrumentos_tuplas]
    instrumentos_acciones = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG"]
    # Ejecutar hasta que el programa se interrumpa manualmente
    while True:
        # Obtener Datos y Ejecutar Estrategia
        fecha_final = datetime.now()
        fecha_inicial = fecha_final - timedelta(days=1) # Día anterior
        # Dar formato correcto
        fecha_final = fecha_final.strftime("%Y-%m-%dT%H:%M:%S")
        fecha_inicial = fecha_inicial.strftime("%Y-%m-%dT%H:%M:%S")
        brokers.oanda.obtener_datos(tickers=instrumentos_oanda, inicio=fecha_inicial, final=fecha_final, granulidad="M1")
        df_yfinance = {instrumento: yf.download(instrumento, interval="1m", progress=False)  for instrumento in instrumentos_acciones}
        
        # Calcular estrategias para datos de Oanda
        señales_generadas = []
        for ticker, datos in brokers.oanda.precios.items():
            # Renombrar columnas
            datos.columns = ["Open", "High", "Low", "Close", "Volume", "Complete"]
            # Calcular Estrategia
            calculo_oanda = Multiples_Estrategias(datos=datos)
            
            # Revisar si hay señales
            
            # Estrategia 1
            if isinstance(calculo_oanda["est1"]["señal"], dict): # Se generó una señal en Estrategia 1
                tendencia_actual = 1 if calculo_oanda["est1"]["señal"]["tendencia"] == "alcista" else -1
                # Revisar si hay un consenso entre ambas estrategias
                if (tendencia_actual == 1) and (pd.notna(calculo_oanda["est2"]["calculos"]["FinalLowerB"].iloc[-1])):
                    # Se ha generado una señal alcista
                    señales_generadas.append([ticker, "buy"])
                elif (tendencia_actual == -1) and (pd.notna(calculo_oanda["est2"]["calculos"]["FinalUpperB"].iloc[-1])):
                    # Se ha generado una señal bajista
                    señales_generadas.append([ticker, "sell"])
                    
            # Estrategia 2
            elif isinstance(calculo_oanda["est2"]["señal"], dict): # Se generó una señal en Estrategia 2
                tendencia_actual = 1 if calculo_oanda["est2"]["señal"]["tendencia"] == "alcista" else -1
                # Revisar si hay un consenso entre ambas estrategias
                if (tendencia_actual == 1) and (calculo_oanda["est1"]["calculos"]["Cruce"].iloc[-1] == 1.0):
                    # Se ha generado una señal alcista
                    señales_generadas.append([ticker, "buy"])
                elif (tendencia_actual == -1) and (calculo_oanda["est1"]["calculos"]["Cruce"].iloc[-1] == -1.0):
                    # Se ha generado una señal bajista
                    señales_generadas.append([ticker, "sell"])
                    
            else:
                continue
            
        # Calcular Estrategia para los datos de yahoo finance
        for ticker, datos in df_yfinance.items():
            # Calcular Estrategia
            calculo_yfinance = Multiples_Estrategias(datos=datos)
            # Obtener Sentimiento de Mercado con respecto a este activo
            sentimiento = Sentimiento_Mercado(ticker=ticker)["sentimiento"].iloc[-1]
            
            # Revisar si hay señales
                    
            # Estrategia 1
            if isinstance(calculo_yfinance["est1"]["señal"], dict): # Se generó una señal en Estrategia 1
                tendencia_actual = 1 if calculo_yfinance["est1"]["señal"]["tendencia"] == "alcista" else -1
                # Revisar si hay un consenso entre ambas estrategias y el sentimieto de mercado
                if (tendencia_actual == 1) and (pd.notna(calculo_yfinance["est2"]["calculos"]["FinalLowerB"].iloc[-1])) and (sentimiento >= 0):
                    # Se ha generado una señal alcista
                    señales_generadas.append([ticker, "buy"])
                elif (tendencia_actual == -1) and (pd.notna(calculo_yfinance["est2"]["calculos"]["FinalUpperB"].iloc[-1])) and (sentimiento <= 0):
                    # Se ha generado una señal bajista
                    señales_generadas.append([ticker, "sell"])
                    
            # Estrategia 2
            elif isinstance(calculo_yfinance["est2"]["señal"], dict): # Se generó una señal en Estrategia 2
                tendencia_actual = 1 if calculo_yfinance["est2"]["señal"]["tendencia"] == "alcista" else -1
                # Revisar si hay un consenso entre ambas estrategias  y el sentimieto de mercado
                if (tendencia_actual == 1) and (calculo_yfinance["est1"]["calculos"]["Cruce"].iloc[-1] == 1.0) and (sentimiento >= 0):
                    # Se ha generado una señal alcista
                    señales_generadas.append([ticker, "buy"])
                elif (tendencia_actual == -1) and (calculo_yfinance["est1"]["calculos"]["Cruce"].iloc[-1] == -1.0) and (sentimiento <= 0):
                    # Se ha generado una señal bajista
                    señales_generadas.append([ticker, "sell"])
        
        
        # Imprimir por consola las señales generadas
        print("Sistema Intradía:", señales_generadas)
        # Dormir 1 minuto entre cada iteración
        time.sleep(60)
        
 
# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Ejecutar Sistema
    Sistema_Intradia()
