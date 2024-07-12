# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
from copy import deepcopy
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf


# Bandas de Bollinger
def Bollinger_Bands(df: pd.DataFrame, longitud: int = 20, desviacion_std: float = 2.0, columna: str = "Close") -> pd.DataFrame:
    
    """
    Las Bandas de Bollinger son una herramienta de análisis técnico para generar señales de sobrecompra o sobreventa. Están
    compuestas por tres líneas: una media móvil simple (conocida como banda media) y una banda superior e inferior. Las bandas
    superior e inferior suelen estar a +/- 2 desviaciones estándar de una media móvil simple de 20 días.
    
    Cómo Operarlo:
        
        Cuando el precio del activo rompe por debajo de la banda inferior de las Bandas de Bollinger, los precios han caído quizás
        demasiada y es probable que rebote. Por otro lado, cuando los precios rompen por encima de la banda superior, el mercado
        está quizás sobrecomprado y es probable que haya una corrección.
        
        Utilizar las bandas como indicadores de sobrecompra/sobreventa se basa en el concepto de reversión a la media del precio.
        La reversión a la media asume que, si los precios se desvían sustancialmente de la media o promedio, eventualmente volverán
        al precio medio.
        
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos históricos del activo.
    ----------
    param : int : longitud : Ventana a utilizar en el cálculo de las Bandas de Bollinger (por defecto, se establece en 20).
    ----------
    param : float : desviacion_std : Número de Desviaciones Estándar a utilizar en el cálculo de las Bandas de Bollinger (por defecto, se establece en 2.0).
    ----------
    param : str : columna : Columna a utilizar en el cálculo de las Bandas de Bollinger (por defecto, se establece en "Close").
    
    Salida:
    ----------
    return : pd.DataFrame : Cálculo de las Bandas de Bollinger.
    """
    
    # Calcular
    datos = deepcopy(df)
    rolling = datos[columna].rolling(window=longitud)
    datos["MA"] = rolling.mean()
    std_bandas = desviacion_std * rolling.std(ddof=0)
    datos["BB_Up"] = datos["MA"] + std_bandas
    datos["BB_Lw"] = datos["MA"] - std_bandas
    
    return datos[["BB_Up", "MA", "BB_Lw"]]
    
# Obtener datos
df = yf.download(tickers="PYPL", start="2023-01-01", end="2024-01-01", interval="1d")
# Calcular Bandas de Bollinger
bb = Bollinger_Bands(df, longitud=20, desviacion_std=2.0)
# Plot
bb_plot = mpf.make_addplot(bb)
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=bb_plot, figscale=2.0, title="Bandas de Bollinger")
plt.show()
    
# Recordatorio:
#   - Las Bandas de Bollinger pueden indicar niveles de sobrecompra y sobreventa cuando los precios tocan o cruzan
#     la banda superior e inferior, respectivamente.
#   - La reversión a la media indica que los precios tienden a regresar a un nivel promedio después de tocar las Bandas
#     de Bollinger, lo que puede ayudar a identificar oportunidades de trading.
