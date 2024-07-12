# Importar librerías
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
# Librerías Propias
from Fundamental import Formula_Magica
from OptPortafolios import Opt_Portafolios

# Definir Sistema de Trading/Inversión a Largo Plazo
def Sistema_LargoPlazo() -> None:
    
    """
    Ejecuta una estrategia de trading a largo plazo (cada día).
    """
    
    # Obtener activos
    tickers = pd.read_csv("S&P 500.csv").sort_values(by="marketCap", ascending=False)["Symbol"].tolist()[:30]
    # Fórmula Mágica
    fm = Formula_Magica(tickers)
    # Tickers y Fechas
    tickers_fm = list(fm.index)
    fecha_final = datetime.now()
    fecha_inicial = fecha_final - timedelta(days=365) # Último año
    # Dar formato correcto
    fecha_inicial = fecha_inicial.strftime("%Y-%m-%d")
    fecha_final = fecha_final.strftime("%Y-%m-%d")
    df_tickers = yf.download(tickers_fm, start=fecha_inicial, end=fecha_final, interval="1d", progress=False)["Close"]
    # Ordenar descargar en el orden inicial/original
    df_tickers = df_tickers[tickers_fm]
    # Rendimientos
    rendimientos = df_tickers.pct_change().dropna()
    # Optimizar Portafolio
    optimizacion = Opt_Portafolios(rendimientos)
    # Imprimir información
    ponderaciones = list(zip(rendimientos.columns, optimizacion["pesos"]))
    ponderaciones_ordenadas = sorted(ponderaciones, key=lambda x: x[1])[::-1]
    print("Ponderaciones del Portafolio:")
    print(ponderaciones_ordenadas)
    print("Rendimiento Portafolio:", optimizacion["retorno"])
    print("Volatilidad del Portafolio:", optimizacion["volatilidad"])
    print("Coeficiente de Sharpe:", optimizacion["sharpe ratio"])
    
    
# Ejemplo (Recordatorio)    
if __name__ == "__main__":
    # Ejecutar Sistema
    Sistema_LargoPlazo()
