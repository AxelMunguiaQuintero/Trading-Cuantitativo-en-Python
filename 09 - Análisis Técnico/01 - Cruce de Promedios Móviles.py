# Importar librerias
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Cruce de Promedios Móviles
def MA_Crossover(df: pd.DataFrame, len_rapida: int = 9, len_lenta: int = 26, columna: str = "Close") -> pd.DataFrame:
    
    """
    El Cruce de Medias Móviles es un indicador técnico que utiliza dos medias móviles (MAs) como estrategia de trading.
    Es un buen ejemplo de lo que se conoce como estrategias tradicionales. Las estrategias tradicionales siempre están 
    en posición larga o corta, lo que significa que nunca están fuera del mercado.
    
    Cómo Operarlo:
        
        El operar con el Cruce de Medias Móviles es bastante simple. Si la media móvil rápida cruza de abajo hacia arriba
        la media móvil lenta, esto señala una oportunidad de compra. Si la media móvil rápida cruza de arriba hacia abajo
        la media móvil lenta, esto señala una oportunidad de venta. El Cruce de Medias Móviles se usa frecuentemente junto
        con otros indicadores para evitar señales falsas en mercados de baja volatilidad.
        
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos históricos.
    ----------
    param : int : len_rapida : Venta rápida a usar en el cálculo del Cruce de MA (por defecto, se establece en 9).
    ----------
    param : int : len_lenta : Venta lenta a usar en el cálculo del Cruce de MA (por defecto, se establece en 26).
    ----------
    param : str : columna : Columna a usar en el cálculo del Cruce de MA (por defecto, se establece en "Close").
    ----------
    Salida:
    ----------
    return : pd.DataFrame : Cálculo del Cruce de Medias Móviles.
    """
    
    # Calcular
    close = df[columna]
    MA_rapida = close.rolling(window=len_rapida).mean()
    MA_rapida_s = MA_rapida.shift(periods=1)
    MA_lenta = close.rolling(window=len_lenta).mean()
    MA_lenta_s = MA_lenta.shift(periods=1)
    # Detectar los cruces
    Cruce = np.where(((MA_rapida > MA_lenta) & (MA_lenta_s > MA_rapida_s)), 1,
                     np.where(((MA_rapida < MA_lenta) & (MA_lenta_s < MA_rapida_s)), -1, np.nan))
    # Rellenar los Nans hacia adelante de los cruces
    Cruce = pd.Series(Cruce, index=df.index).ffill()
    
    MAC = pd.concat([MA_rapida, MA_lenta, Cruce], axis=1)
    MAC.columns = ["MA_Rápida", "MA_Lenta", "Cruce"]
    
    return MAC

# Mostar un ejemplo
datos = yf.download("AMZN", start="2019-01-01", end="2024-01-01", interval="1d")
# Calcular estrategia para diferentes periodos de tiempo (Corto, Mediano y Largo plazo)
cruce_ma_cp = MA_Crossover(datos, len_rapida=9, len_lenta=26) # Corto Plazo
cruce_ma_mp = MA_Crossover(datos, len_rapida=21, len_lenta=50) # Mediano Plazo
cruce_ma_lp = MA_Crossover(datos, len_rapida=50, len_lenta=200) # Largo Plazo    
    
# Plot
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(28, 18))
datos["Close"].plot(ax=axes[0], label="Precios de Cierre")
cruce_ma_cp.plot(secondary_y=["Cruce"], ax=axes[0], title="Corto Plazo con Ventanas [9, 26]")  
datos["Close"].plot(ax=axes[1], label="Precios de Cierre")
cruce_ma_mp.plot(secondary_y=["Cruce"], ax=axes[1], title="Mediano Plazo con Ventanas [21, 50]")  
datos["Close"].plot(ax=axes[2], label="Precios de Cierre")
cruce_ma_lp.plot(secondary_y=["Cruce"], ax=axes[2], title="Largo Plazo con Ventanas [50, 200]")   
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()
    
# Recordatorio:
#   - El cruce de MA es una estratega básica pero efectiva que utiliza medias móviles para identificar puntos
#     de entrada y salida en el mercado.
#   - Es importante considerar el contexto actual de mercado y usar múltiples marcos temporales para aplicar el cruce de MA.
#   - La confirmación con otros indicadores técnicos puede mejorar la precisión de las señales del indicador.
