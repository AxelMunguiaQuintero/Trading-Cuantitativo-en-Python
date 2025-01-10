# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
# Librerías Propias
from estrategias.Estrategia1 import Estrategia1
from estrategias.Estrategia2 import Estrategia2

# Definir función
def Multiples_Estrategias(datos: pd.DataFrame, **kwargs) -> dict:
    
    """
    Calcula el estado actual para ambas estrategias
    """
    
    # Crear instancias
    est1 = Estrategia1(df=datos, ventana_cp=kwargs.get("ventana_cp", 9), ventana_lp=kwargs.get("ventana_lp", 14))
    est2 = Estrategia2(df=datos, longitud=kwargs.get("longitud", 14), factor=kwargs.get("factor", 3.0))
    # Calcular (Ver si se ha generado una señal)
    est1_situacion_actual = est1.calcular()
    est2_situacion_actual = est2.calcular()
    # Extraer calculos
    est1_calculos = est1.calculo_estrategia
    est2_calculos = est2.calculo_estrategia
    
    return {
        
        "est1": {"señal": est1_situacion_actual, "calculos": est1_calculos},
        "est2": {"señal": est2_situacion_actual, "calculos": est2_calculos}
        
        }

# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Obtener datos
    df = yf.download("AMZN", interval="1m")
    # Calcular estrategias
    calc_estrategias = Multiples_Estrategias(datos=df)
    print(calc_estrategias)
