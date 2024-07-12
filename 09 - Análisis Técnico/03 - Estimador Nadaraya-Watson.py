# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

# Estimador/Envoltura Nadaraya Watson
def Estimador_Nadaraya_Watson_Envoltura(df: pd.DataFrame, longitud: int = 500, ancho_banda: float = 8.0, factor: float = 3.0, 
                                        columna: str = "Close") -> pd.DataFrame:
    
    """
    El Estimador Nadaraya-Watson puede describirse como una serie de promedio ponderados utilizando un kernel normalizado específico
    como función de ponderación. Para cada punto del estimador en el tiempo t, el pico del kernel se encuentra en el tiempo t, por lo
    que los pesos más altos se atribuyen a los valores vecinos al precio en el tiempo t.
    
    Un valor de ancho de banda más bajo contriburía hacia una ponderación más importante del precio en un punto preciso, y como tal, 
    daría resultados menos suavizados. Sin embargo, cuando el ancho de banda es suficientemente grande, los precios se ponderarían de
    manera similar, lo que resultaría en un resultado más cercano a la media de precios.
    
    Es interesante destacar que debido a la naturaleza del estimador y su procedimiento de ponderación, los resultados en tiempo real
    no se desviarían drásticamente para puntos en el estimador cerca del centro de la venta del cálculo.
    
    La Envoltura Nadaraya-Watson destaca los extremos realizados por los precios dentro del tamaño de ventana seleccionado. Esto se logra
    estimando la tendencia subyacente en el precio mediante suavizado del núcleo, calculando las desviaciones absolutas medias de ella y
    sumándola/restándola de la tendencia subyaente estimada.
    
    Cómo Operarlo:
        
        Se espera que el precio se revierta cuando cruce una de las extremidades de la envoltura o cuando se alcance un nuevo punto de 
        reverión en el Estimador NW.
        
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos históricos del activo.
    ----------
    param : int : longitud : Determina el número de observaciones de precios recientes que se utilizarán para ajustar el Estimador
                             Nadaraya-Watson (por defecto, se establece en 500).
    ----------
    param : float : ancho_banda : Controla el grado de suavidad de las envolturas, con valores más altos se devuelven resultados más
                                  suaves (por defecto, se establece en 8.0).
    ----------
    param : float : factor : Controla el ancho de la envoltura (por defecto, se establece en 3.0).
    ----------
    param : str : columna : Columna a utilizar en el cálculo de NW Est/Env (por defecto, se establece en "Close").
    
    Salida:
    ----------
    return : pd.DataFrame : Cálculo del Estimador/Envoltura de Nadaraya Watson.                                  
    """
    
    # Calcular
    assert df.shape[0] >= longitud, "La longitud del df debe de ser >= longitud"
    precio_columna = df[-longitud:][columna]
    filas = np.arange(0, longitud)
    matriz_pesos = np.array( np.exp( - np.power((np.matrix(filas).T - np.matrix(filas)), 2) / ((ancho_banda ** 2) * 2)))
    suma_x = (matriz_pesos * np.tile(precio_columna.values, (longitud, 1))).sum(axis=1)
    y2 = suma_x / matriz_pesos.sum(axis=1)
    nwee = pd.DataFrame(data=y2, index=precio_columna.index, columns=["Estimador"])
    # Dirección Estimador
    d = nwee - nwee.shift(periods=1)
    d_s = d.shift(periods=1)
    nwee["Direccion_Estimador"] = np.where((d > 0) & (d_s < 0), 1, np.where((d < 0) & (d_s > 0), -1, np.nan))
    nwee["Direccion_Estimador"] = nwee["Direccion_Estimador"].shift(periods=-1)
    # Dirección de las Bandas Superior e Inferior
    mae = (precio_columna - y2).abs().mean() * factor
    nwee["Banda_Superior"] = y2 + mae
    nwee["Banda_Inferior"] = y2 - mae
    precio_columna_s = precio_columna.shift(periods=1)
    direccion_bandas = np.where(((precio_columna < (y2 - mae))) & ((precio_columna > (y2 - mae))), 1,
                                np.where(((precio_columna_s > (y2 + mae))) & ((precio_columna < (y2 + mae))), -1, np.nan))
    nwee["Direccion_Bandas"] = direccion_bandas
    nwee["Direccion_Bandas"] = nwee["Direccion_Bandas"].shift(periods=-1)
    
    return nwee
    
# Obtener datos
df = pd.read_csv("../datos/AMZN.csv", index_col = "Date", parse_dates=True)
# Calcular indicador
nw = Estimador_Nadaraya_Watson_Envoltura(df)
# Dirección del Estimador
nw_estimador_positivo = nw["Estimador"].where(nw["Direccion_Estimador"].ffill() >= 0, np.nan)
nw_estimador_negativo = nw["Estimador"].where(nw["Direccion_Estimador"].ffill() < 0, np.nan)

nw_plots = [
    
    mpf.make_addplot(nw_estimador_positivo, label="Estimador Positivo", color="green"),
    mpf.make_addplot(nw_estimador_negativo, label="Estimador Negativo", color="red"),
    mpf.make_addplot(nw["Banda_Superior"], label="Banda Superior", color="green"),
    mpf.make_addplot(nw["Banda_Inferior"], label="Banda Inferior", color="red"),
    
    ]
mpf.plot(df[-500:], type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=nw_plots, figscale=3.0, title="Nadaraya-Watson Estimador/Envoltura")
plt.show()
    
# Recordatorio:
#   - La adaptabilidad de nuestro indicador Nadaraya/Watson EE nos permite capturar tendencias y extremos de precios, brindando
#     una visión dinámica del mercado.
#   - Es importante considerar la recalculación diaria del indicador, ya que puede generar inestabilidad en las señales generadas.
