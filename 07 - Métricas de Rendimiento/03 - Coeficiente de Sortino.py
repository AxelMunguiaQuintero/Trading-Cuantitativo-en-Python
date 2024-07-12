# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np

# Datos Históricos
df = pd.read_csv("../datos/MSFT.csv", index_col="Date")
print("Fecha Inicial:", df.index[0])
print("Fecha Final:", df.index[-1])

# Coeficiente de Sortino (Sortino-Ratio)
def coef_Sortino(datos: pd.DataFrame, tasa_lr: float = 0.03, columna: str = "Close") -> float:
    
    """
    Mide el rendimiento ajustado al riesgo al considerar solo la volatilidad negativa, lo que lo hace
    más sensible a las pérdidas que el Coeficiente de Sharpe.
    
    Parámetros
    ----------
    param : pd.DataFrame : datos : Datos Históricos de un activo financiero.
    ----------
    param : float : tasa_lr : Tasa libre de riesgo (por defecto, 0.03 está establecido).
    ----------
    param : str : columna : Columna que se utilizará para realizar el calculo (por defecto, "Close" está establecido).
    
    Salida:
    return : float : Coeficiente de Sortino
    """
    
    # Calcular
    rendimiento_activo = (datos[columna][-1] / datos[columna][0]) ** (1 / np.ceil(datos.shape[0] / 252)) - 1
    rendimientos_diarios = datos[columna].pct_change()
    rendimientos_diarios_negativos = rendimientos_diarios[rendimientos_diarios < 0]
    desviacion_estandar_negativos = rendimientos_diarios_negativos.std() * np.sqrt(252)
    
    return (rendimiento_activo - tasa_lr) / desviacion_estandar_negativos

csortino = coef_Sortino(df)
print("Coeficiente de Sortino:", csortino)
if csortino > 0:
    print("""
          El rendimiento de la inversión es superior a la tasa de retorno objetivo, considerando solo la volatilidad
          negativa o las pérdidas no deseadas
          """)
else:
    print("""
          El rendimiento de la inversión es inferior a la tasa de retorno objetivo, considerando solo la volatilidad
          negativa o las pérdidas no deseadas
          """)
          
# Recordatorio:
#   - El coeficiente de Sharpe evalúa la rentabilidad ajustada al riesgo total, mientras que el Coeficiente de Sortino
#     se enfoca en la volatilidad negativa, mejorando la precisión al penalizar únicamente las pérdidas no deseadas.
