# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from warnings import filterwarnings
filterwarnings("ignore")
# Librerías Propias
from InstrumentosFinancieros import obtener_activos
from InfoHist import market_cap
from AnalisisCuantitativo import Estados_Ocultos
from estrategias.Estrategia2 import Estrategia2

# Definir Sistema de Trading Corto/Mediano Plazo
def Sistema_MedianoPlazo(descargar_datos: bool = False) -> None:
    
    """
    Ejecuta una estrategia de trading a mediano plazo (cada 1 hora).
    """
    
    # Recuperar Activos
    if descargar_datos:
        activos_sp500 = obtener_activos(indice="S&P 500", archivo="links_indices.json")
        activos_sp500["marketCap"] = 0
        # Extraer Capitalización
        for n, ticker in enumerate(activos_sp500["Symbol"]):
            marketCap = market_cap(ticker)
            activos_sp500.loc[n, "marketCap"] = marketCap
    else:
        activos_sp500 = pd.read_csv("S&P 500.csv")
    # Mantener los 30 más grandes
    activos_sp500 = activos_sp500.sort_values(by="marketCap", ascending=False)
    activos_sp500 = activos_sp500["Symbol"].iloc[:30].tolist()
    # Ejecutar el sistema hasta que se detenga manualmente
    señales_generadas = []
    while True:
        for ticker in activos_sp500:
            # Obtener Datos y Ejecutar Estrategia
            fecha_final = datetime.now()
            fecha_inicial = fecha_final - timedelta(days=30) # Últimos 30 días
            # Dar formato correcto
            fecha_final = fecha_final.strftime("%Y-%m-%d")
            df = yf.download(ticker, start=fecha_inicial, interval="1h", progress=False)
            # Calcular estrategia
            eo_m = Estados_Ocultos(df=df, n_continuidad=10)
            est2 = Estrategia2(df)
            actual_señal = est2.calcular()
            # Revisar si hay señales
            if isinstance(actual_señal, dict):
                if (actual_señal["tendencia"] == "alcista") and pd.notna(eo_m["estados"]["alcista"].iloc[-1]):
                    # Se ha generado una señal alcista
                    señales_generadas.append([ticker, "buy"])
                elif (actual_señal["tendencia"] == "bajista") and pd.notna(eo_m["estados"]["bajista"].iloc[-1]):
                    # Se ha generado una señal bajista
                    señales_generadas.append([ticker, "sell"])
                else:
                    continue
        # Imprimir por consola las señales generadas
        print("Sistema de Corto/Mediano Plazo:", señales_generadas)
        # Dormir entre cada iteración (1 hora)
        time.sleep(60 * 60)
    
    
# Ejemplo (Recordatorio)    
if __name__ == "__main__":
    # Ejecutar Sistemaa
    Sistema_MedianoPlazo(descargar_datos=False)
