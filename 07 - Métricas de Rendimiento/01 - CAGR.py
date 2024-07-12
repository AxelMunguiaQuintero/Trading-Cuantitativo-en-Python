# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf


# Recuperar datos
df = pd.read_csv("../datos/NVDA.csv", index_col="Date")
print("Fecha Inicial:", df.index[0])
print("Fecha Final:", df.index[-1])

# Tasa de Crecimiento Anual Compuesta
def CAGR(datos: pd.DataFrame, calculo_optimizado: bool = True, columna: str = "Close") -> float:
    
    """
    Mide la tasa de crecimiento anualizada de una inversión durante un periodo de tiempo específico.
    
    Parámetros
    ----------
    param : pd.DataFrame : datos : Datos históricos de un activo financiero.
    ----------
    param : bool : calculo_optimizado : Si es True, utilizará el primer método para calcular la métrica (por defecto, True está establecido).
    ----------
    param : str : columna : Columna ha utilizar para realizar el calculo (por defecto, "Close" está establecido).
    
    Salida:
    return : float : Tasa de Crecimiento.
    """
    
    # Calcular
    n = np.ceil(datos.shape[0] / 252)
    if calculo_optimizado:
        valor_inicial = datos[columna][0]
        valor_final = datos[columna][-1]
        
        return (valor_final / valor_inicial) ** (1 / n) - 1
    else:
        # Usando rendimientos
        retornos_diarios = datos[columna].pct_change()
        retornos_acumulados = (1 + retornos_diarios).cumprod()
        
        return retornos_acumulados[-1] ** (1 / n) - 1
    
print("Tasa de Crecimiento Anual Compuesto (Método Optimizado) ->", CAGR(df))
print("Tasa de Crecimiento Anual Compuesto (Método No Optimizado) -> Usando retornos: ", CAGR(df, calculo_optimizado=False))
        
# Repetir proceso pero con un instrumento distinto (TSLA)
df = yf.download(tickers="TSLA", start=df.index[0], end=df.index[-1], interval="1d")
print("Tasa de Crecimiento Anual Compuesto (Método Optimizado) ->", CAGR(df))
print("Tasa de Crecimiento Anual Compuesto (Método No Optimizado) -> Usando retornos: ", CAGR(df, calculo_optimizado=False))

# Recordatorio:
#   - CAGR es una métrica comúnmente utilizada para medir la tasa de crecimiento anualizada de una inversión durante
#     un periodo de tiempo específico.
