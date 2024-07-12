# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

# Optimizador de Portafolios
def Opt_Portafolios(rendimientos: pd.DataFrame) -> dict:
    
    """
    Obtiene los pesos optimizados para encontrar el portafolio de mayor coeficiente de Sharpe.
    """
    
    # Calcular matriz de covarianza anualizada
    diagonal_volatilidades = np.diag(rendimientos.std() * np.sqrt(252)) # Volatilidades anualizadas en diagonal
    Sigma = diagonal_volatilidades.dot(rendimientos.corr()).dot(diagonal_volatilidades) # Matriz de covarianza anualizada
    # Sigma = rendimientos.cov() * 252
    
    # Función objetivo para maximizar el coeficiente de Sharpe
    def sharpe_ratio(pesos, Sigma, rf, rendimientos_esperados):
        retorno_esperado_portafolio = rendimientos_esperados.dot(pesos)
        varianza_portafolio = pesos.dot(Sigma).dot(pesos)
        return -(retorno_esperado_portafolio - rf) / np.sqrt(varianza_portafolio)
    
    # Definir condiciones y límites para la optimización
    num_activos = len(rendimientos.columns)
    w0 = np.ones(num_activos) / num_activos
    bnds = ((0, 1), ) * num_activos
    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    
    # Tasa libre de riesgo y los rendimientos esperados individuales
    rf = 0.03
    rendimientos_esperados = rendimientos.mean() * 252
    
    # Optimización para encontrar el portafolio de máximo coeficiente de sharpe
    max_sr = minimize(sharpe_ratio, w0, args=(Sigma, rf, rendimientos_esperados), constraints=cons, bounds=bnds)
    
    # Mostrar resultados del portafolio de mayor coeficiente de Sharpe
    pesos_optimizados_sr = max_sr.x
    retorno_portafolio_optimizado_sr = (rendimientos * pesos_optimizados_sr).sum(axis=1).mean() * 252
    volatilidad_portafolio_optimizado_sr = np.sqrt(np.dot(pesos_optimizados_sr, np.dot(rendimientos.cov(), pesos_optimizados_sr))) * np.sqrt(252)
    sharpe_ratio_optimizado = (retorno_portafolio_optimizado_sr - rf) / volatilidad_portafolio_optimizado_sr
    
    return {
        "pesos": pesos_optimizados_sr,
        "retorno": retorno_portafolio_optimizado_sr,
        "volatilidad": volatilidad_portafolio_optimizado_sr,
        "sharpe ratio": sharpe_ratio_optimizado
        }
    

# Ejemplo (Recordatorio)  
if __name__ == "__main__":
    # Seleccionar activos
    archivo_fm = "FormulaMagica.csv"
    df_fm = pd.read_csv(archivo_fm, index_col="Ticker")
    # Mantener los primeros 25 para optimizar
    df_fm = df_fm.iloc[:25]
    # Obtener Datos Históricos
    tickers = list(df_fm.index)
    df_datos = yf.download(tickers=tickers, start="2023-01-01", end="2024-01-01", interval="1d")["Close"][list(df_fm.index)]
    # Rendimientos
    rendimientos = df_datos.pct_change().dropna()
    # Optimizar portafolio
    optimizacion = Opt_Portafolios(rendimientos)
    # Imprimir información por consola
    print(optimizacion)
