# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np


# Obtener datos
df = pd.read_csv("../datos/AMZN.csv", index_col="Date")
print("Fecha Inicial:", df.index[0])
print("Fecha Final:", df.index[-1])

# Coeficiente de Sharpe (Sharpe-Ratio)
def coef_sharpe(datos: pd.DataFrame, tasa_lr: float = 0.03, columna: str = "Close") -> float:
    
    """
    Calcula el Coeficiente de Sharpe que es la rentabilidad que ofrece una inversión por cada unidad de riesgo que se asume.
    
    Parámetros
    ----------
    param : pd.DataFrame : datos : Datos históricos de un activo financiero.
    ----------
    param : float : tasa_lr : Tasa libre de riesgo (por defecto, 0.03 está establecido).
    ----------
    param : str : columna : Columna que usaremos para realizar el calculo (por defecto, "Close" está establecido)
    
    Salida:
    return : float : Coeficiente de Sharpe
    """
    
    # Calcular
    retorno_activo = (datos[columna][-1] / datos[columna][0]) ** (1 / np.ceil(datos.shape[0] / 252)) - 1
    desviacion_estandar_anualizada = datos[columna].pct_change().std() * np.sqrt(252)
    
    return (retorno_activo - tasa_lr) / desviacion_estandar_anualizada


cs = coef_sharpe(df, tasa_lr=0.03, columna="Close")
print("Coeficiente de Sharpe:", cs, end="\n"*2)

if cs > 0:
    print("""
          - Nuestra inversión genera un rendimiento superior a la tasa libre de riesgo, considerando el riesgo asumido.
          Es un indicador de un buen rendimiento ajustado al riesgo.
          """)
else:
    print("- La inversión está generando pérdidas en comparación con una inversión en un activo libre de riesgo.")
    print("- En este caso conviene más invertir en activos libres de riesgo como bonos del gobierno o depósitos bancarios seguros")

# Recordatorio:
#   - El Coeficiente de Sharpe es la rentabilidad que ofrece una inversión por cada unidad de riesgo que se asume.
#   - Si es Positivo tenemos un rendimiento superior a la tasa libre de riesgo considerando el riesgo asumido.
#   - Si es Negativo, conviene más invertir en activos libres de riesgo.
