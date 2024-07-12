# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from copy import deepcopy
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Parabolic SAR
def Parabolic_SAR(df: pd.DataFrame, incremento: float = 0.02, max_paso: float = 0.20) -> pd.DataFrame:
    
    """
    El indicador de Parabolic SAR se utiliza para determinar la dirección de la tendencia y posible 
    reversas en el precio. Utiliza un método de parada y reversa llamado "SAR" para identificar punto
    de salida y entrada adecuados.
    
    El indicador utiliza un sistema de puntos superpuestos en un gráfico de precios. Una reversa ocurre
    cuando estos puntos cambian de dirección, pero una señal de reversa en el SAR no necesariamente indica
    una reversa en el precio. Una reversa en el SAR solo indica que el precio y el indicador se han cruzado.
    
    Cómo Operarlo:
        
        El PSAR genera señales de compra o venta cuando la posición de los puntos se mueve de un lado del precio
        del activo al otro. Por ejemplo, una señal de compra ocurre cuando los puntos se mueven de arriba del 
        precio a abajo del precio, mientras que una señal de venta ocurre cuando los puntos se mueven de abajo
        del precio a arriba del precio.
        
        Los puntos del PSAR se utilizan para establecer órdenes de stop loss móviles. Por ejemplo, si el precio
        está subiendo y el PSAR también está subiendo, el PSAR puede utilizarse como una posible salida si se
        está en una posición larga. Si el precio cae por debajo del PSAR, se debe de salir de la operación larga.
        
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del activo.
    -----------
    param : float : incremento : Incremento máximo que se utilizará en el cálculo del SAR Parabólico (por defecto, se establece 0.02).
    -----------
    param : float : max_paso : Paso máximo que se utilizará en el cálculo del SAR Parabólico (por defecto, se establece 0.20).
    
    Salida:
    -----------
    return : pd.DataFrame : Cálculo de Parabolic SAR.
    """
    
    # Calcular
    data = deepcopy(df)
    High, Low, Close = data["High"].values, data["Low"].values, data["Close"].values
    psar_up, psar_down = np.repeat(np.nan, Close.shape[0]), np.repeat(np.nan, Close.shape[0])
    up_trend = True
    up_trend_high = High[0]
    down_trend_low = Low[0]
    acc_factor = incremento
    for i in range(2, Close.shape[0]):
        reversal = False
        max_high = High[i]
        min_low = Low[i]
        # Tendencia alcista
        if up_trend:
            # Calcular el nuevo PSAR para una tendencia alcista
            Close[i] = Close[i - 1] + (acc_factor * (up_trend_high - Close[i - 1]))
            # Verificar si se produce una reversión de tendencia
            if min_low < Close[i]:
                reversal = True
                Close[i] = up_trend_high
                down_trend_low = min_low
                # Reiniciar el factor de aceleración
                acc_factor = incremento
            else:
                if max_high > up_trend_high:
                    up_trend_high = max_high 
                    acc_factor = min(acc_factor + incremento, max_paso)
                low1 = Low[i - 1]
                low2 = Low[i - 2]
                # Ajustar el PSAR en caso de que los valores bajen
                if low2 < Close[i]:
                    Close[i] = low2
                elif low1 < Close[i]:
                    Close[i] = low1
        # Tendencia Bajista
        else:
            # Calcular el nuevo PSAR para una tendencia bajista
            Close[i] = Close[i - 1] - (acc_factor * (Close[i - 1] - down_trend_low))
            # Verificar si se produce una reversión en la tendencia
            if max_high > Close[i]:
                # Indicar que se produce una reversión
                reversal = True 
                Close[i] = down_trend_low
                up_trend_high = max_high
                # Reiniciar el factor de aceleración
                acc_factor = incremento
            else:
                if min_low < down_trend_low:
                    down_trend_low = min_low 
                    acc_factor = min(acc_factor + incremento, max_paso)
                high1 = High[i - 1]
                high2 = High[i - 2]
                # Ajusatr el PSAR en caso de que los valores suban
                if high2 > Close[i]:
                    Close[i] = high2
                elif high1 > Close[i]:
                    Close[i] = high1
                    
        # Actualizar la dirección de la tendencia
        up_trend = up_trend != reversal
        
        # Actualizar los puntos del PSAR
        if up_trend:
            psar_up[i] = Close[i]
        else:
            psar_down[i] = Close[i]
            
    data["PSAR"] = Close
    data["UpTrend"] = psar_up
    data["DownTrend"] = psar_down
    
    return data[["PSAR", "UpTrend", "DownTrend"]]
        
    
# Obtener los datos
df = pd.read_csv("../datos/AMZN.csv", index_col="Date", parse_dates=True)
# Calcular indicador
p_sar = Parabolic_SAR(df)
# Plots    
psar_plots = [
    
    mpf.make_addplot(p_sar["UpTrend"], label="Tendencia Alcista", color="green", type="scatter"),
    mpf.make_addplot(p_sar["DownTrend"], label="Tendencia Bajista", color="red", type="scatter")
    
    ]
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=psar_plots, figscale=3.0, title="Parabolic SAR")
plt.show()  
    
# Recordatorio:
#   - El Parabolic SAR identifica tendencias y posibles cambios de dirección mediante puntos sobre o bajo el precio.
#   - Los puntos del SAR pueden servir como señales de entrada o salida según su posición respecto al precio.
