# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt


# Indicador: SuperTendencia
def SuperTendencia(df: pd.DataFrame, longitud: int = 14, factor: float = 3.0) -> pd.DataFrame:
    
    """
    SuperTendencia es el indicador de seguimiento de tendencia. Dibuja un línea en el gráfico de velas, dependiendo del color,
    indica si está en una tendencia negativa (una línea roja sobre las velas) o una tendencia positiva (línea verde debajo de las velas).
    Ambas líneas pueden utilizarse como niveles de soporte (línea verde) o resistencia (línea roja).
    
    Cómo Operarlo:
        
        La forma más fácil de operar con SuperTendencia es tomar posiciones según las tendencias. Se compra cuando la línea es verde (alcista)
        y se vende en corto cuando la línea es roja (bajista). SuperTendencia suele ser una herramienta complementaria a otros indicadores.
        Una de las estrategias más utilizadas es combinar SuperTendencia y RSI. Si hay un cambio en la tendencia (alcista a bajista en SuperTendencia)
        y el RSI cruza un nivel por debajo de 50, entonces se puede colocar una posición en corto en el activo. Ahora, si hay un cambio en la
        tendencia (bajista a alcista en SuperTendencia) y un cruce del RSI por encima de 50, se puede colocar una posición larga para el activo.
        
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del activo.
    -----------
    param : int : longitud : Ventana a utilizar en ATR para el cálculo de ST (por defecto, se establece en 14).
    -----------
    param : float : factor : Multiplicador de cálculo de ATR (por defecto, se establece en 3.0).
    
    Salida:
    -----------
    return : pd.DataFrame : Cálculo de SuperTendencia.
    """
    
    # Calcular True Range (TR)
    High, Low = df["High"], df["Low"]
    H_minus_L = High - Low
    prev_close = df["Close"].shift(periods=1)
    H_minus_PC = abs(High - prev_close)
    L_minus_PC = abs(Low - prev_close)
    TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
    
    # Calcular ATR (Average True Range)
    ATR = TR.ewm(alpha = 1 / longitud).mean()
    
    # Calcular valores básicos
    medio = ((High + Low) / 2)
    FinalUpperB = medio + factor * ATR
    FinalLowerB = medio - factor * ATR
    
    # Inicializar SuperTendencia
    Supertendencia = np.zeros(ATR.shape[0])
    close = df["Close"]
    
    for i in range(1, ATR.shape[0]):
        # Calcular SuperTendencia para cada punto
        if close[i] > FinalUpperB[i - 1]:
            Supertendencia[i] = True
        elif close[i] < FinalLowerB[i - 1]:
            Supertendencia[i] = False
        # La tendencia continua
        else:
            Supertendencia[i] = Supertendencia[i - 1]
            # Ajustar las bandas finales
            if Supertendencia[i] == True and FinalLowerB[i] < FinalLowerB[i - 1]:
                FinalLowerB[i] = FinalLowerB[i - 1]
            elif Supertendencia[i] == False and FinalUpperB[i] > FinalUpperB[i - 1]:
                FinalUpperB[i] = FinalUpperB[i - 1]
                
        # Eliminar bandas según la dirección de la tendencia
        if Supertendencia[i] == True:
            FinalUpperB[i] = np.nan
        else:
            FinalLowerB[i] = np.nan
            
    # Ajustar valor inicial en la posición 0
    if Supertendencia[1] == 0:
        FinalLowerB[0] = np.nan
    else:
        FinalUpperB[0] = np.nan
        
    # Eliminar valores no deseados
    FU = FinalUpperB[longitud - 1:]
    FL = FinalLowerB[longitud - 1:]
    ST_df = pd.concat([FU, FL], axis=1)
    ST_array = np.nansum([FU, FL], axis=0)
    ST_array[0] = np.nan
    ST_df["SuperTendencia"] = ST_array
    ST_df.columns = ["FinalUpperB", "FinalLowerB", "SuperTendencia"]
    
    return ST_df
            
# Datos
df = pd.read_csv("../datos/AMZN.csv", index_col="Date", parse_dates=True)
# Calcular Indicador
sp = SuperTendencia(df)       
# Plot
sp_plots = [
    
    mpf.make_addplot(sp["SuperTendencia"], label="Cambio de Tendencia", color="black"),
    mpf.make_addplot(sp["FinalUpperB"], label="Tendencia Bajista", color="red"),
    mpf.make_addplot(sp["FinalLowerB"], label="Tendencia Alcista", color="green")
    
    ] 
mpf.plot(df[-sp.shape[0]:], type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=sp_plots, figscale=3.0, title="Super Tendencia")
plt.show()
    
# Recordatorio:
#   - SuperTendencia es útil como generador de señales en los cambios de tendencia en el mercado.
#   - Su análisis debe de ser completado con más información para mejorar la toma de decisiones.
