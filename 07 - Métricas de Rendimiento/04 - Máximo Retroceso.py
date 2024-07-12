# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd

# Datos
df = pd.read_csv("../datos/NVDA.csv", index_col="Date")
print("Fecha Inicial:", df.index[0])
print("Fecha Final:", df.index[-1])

# Máxima Reducción (Maximum Drawdown)
def max_dd(datos: pd.DataFrame, columna: str = "Close") -> float:
    
    """
    Mide la peor pérdida sufrida por una inversión, permitiendo a los inversionistas evaluar el riesgo.
    
    Parámetros
    ----------
    param : pd.DataFrame : datos : Datos históricos de un instrumento financiero.
    ----------
    param : str : columna : Columna ha utilizar para realizar el calculo del indicador (por defecto, "Close" está establecida).
    ----------
    Salida:
    ----------
    return : float : Máxima reducción.
    """
    
    # Calcular
    rendimientos_diarios = datos[columna].pct_change()
    rendimientos_acumulados = (1 + rendimientos_diarios).cumprod()
    mayor_rendimiento_acumulado = rendimientos_acumulados.cummax()
    diferencia = mayor_rendimiento_acumulado - rendimientos_acumulados
    diferencia_porcentaje = diferencia / mayor_rendimiento_acumulado
    retroceso_maximo = diferencia_porcentaje.max()
    
    return retroceso_maximo

max_retroceso = max_dd(df)
print("La mayor pérdida que pudimos haber experimentado hubiese sido de:", round(max_retroceso * 100, 3), "%")

# Recordatorio:
#   - El máximo retroceso nos ofrece una visión directa de la pérdida máxima que podríamos haber experimentado por una inversión.
#   - El máximo retroceso nos ayuda a gestionar de manera más efectiva el riesgo en nuestras carteras.
