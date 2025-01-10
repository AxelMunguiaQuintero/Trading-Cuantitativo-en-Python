# -*- coding: utf-8 -*-
# Librerías Estándar
import pandas as pd
import numpy as np
import yfinance as yf
import time
import mplfinance as mpf
# Librerías Propias
...

# Clase Estrategia
class Estrategia1:
    
    """ 
    Estrategia 1: Cruce de Promedios Móviles
    
        Descripción:
            
            Estrategia que utiliza el cruce de promedios móviles para identificar señales de compra y venta.
    
    Estrategia Para:
        
        - Acciones
        - Índices
        - ETFs
        - Divisas
        - Materias Primas
        - Criptomonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - Diario
        - Semanal
        - Mensual
        
    Periodo de Retención:
        
        - Variable (Depende de la fuerza de la tendencia)
        
    Análisis Usado: 
        
        - Análisis Técnico
            * Promedios Móviles

    Descripción Detallada de la Estrategia:    
        
        Estrategia que busca aprovechar los cruces de promedios móviles como señales de entrada y salida en el mercado. 
        La compra se activa cuando el promedio móvil de corto plazo cruza por encima del promedio móvil de largo plazo,
        indicando un impulso alcista. La venta se realiza cuando el cruce es inverso, señalando un posible cambio de
        tendencia.
                        
        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                La toma de ganancia se activa cuando se produce una señal contraria a la de la posición actual.
                
            Stop Loss:
                
                La limitación de pérdidas ocurre cuando se produce una señal contraria a la de la posición actual.
                
    Supuestos Generales:
        
        - Esta estrategia no considera costos o comisiones (Comisiones de apertura, rollovers, entre otros).
        
    Notas:
        
        - Usar esta estrategia en ventanas de tiempo pequeñas (Segundos, Minutos o Horas) puede producir muchas
          señales falsas.
    """
    
    __version__ = 1.0
    
    # __init__
    def __init__(self, df: pd.DataFrame, ventana_cp: int = 9, ventana_lp: int = 21, columna: str = "Close") -> None:
        
        """
        Constructor.
        
        Parámetros
        ----------
        param : pd.DataFrame : df : Datos históricos del instrumento financiero.
        ----------
        param : int : ventana_cp : Ventana de corto plazo (por defecto, se establece en 9).
        ----------
        param : int : ventana_lp : Ventana de largo plazo (por defecto, se establece en 21).
        ----------
        param : str : columna : Columna que será usada para el cálculo (por defecto, se establece en "Close").
        
        Salida
        -------
        return: NoneType : None.
        """
        
        # Atributos
        self.df = df
        self.ventana_cp = ventana_cp
        self.ventana_lp = ventana_lp
        self.columna = columna
        self.calculo_estrategia = None
        # Atributos Privados
        
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self) -> pd.DataFrame:
        
        """
        Este método obtiene la rentabilidad de la estrategia durante todo el periodo
        
        Salida
        -------
        return: pd.DataFrame : Rentabilidad de la estrategia a lo largo del tiempo
        """
        
        # Calcular
        if self.calculo_estrategia is None:
            self.calcular()
        datos = self.calculo_estrategia.copy()
        datos["retorno"] = self.df[self.columna].pct_change()
        # Eliminar los datos nulos
        datos.dropna(inplace=True)
        # Calcular retorno
        retorno = (1 + datos["Cruce"].shift(periods=1) * datos["retorno"]).cumprod()
        
        return retorno
    
    
    # Calcular
    def calcular(self) -> dict:
        
        """
        Este método calcula el cruce de promedios móviles con los datos históricos de un instrumento financiero.

        Salida
        -------
        return: dict|bool : Devuelve un diccionario si se ha generado una señal en la última vela, o False si no se ha generado nada.
        """
        
        # Calcular   
        precio = self.df[self.columna]
        ma_rapida = precio.rolling(window=self.ventana_cp, min_periods=self.ventana_cp).mean()
        ma_rapida_s = ma_rapida.shift(periods=1)
        ma_lenta = precio.rolling(window=self.ventana_lp, min_periods=self.ventana_lp).mean()
        ma_lenta_s = ma_lenta.shift(periods=1)
        # Cruces de los promedios móviles
        cruces = np.where(((ma_rapida > ma_lenta) & (ma_lenta_s > ma_rapida_s)), 1, 
                          np.where(((ma_rapida < ma_lenta) & (ma_lenta_s < ma_rapida_s)), -1, np.nan))
        # Rellenar Tendencia
        cruces = pd.Series(cruces, index=self.df.index).ffill()
        # Unir columnas
        mac = pd.concat([ma_rapida, ma_lenta, cruces], axis=1)
        mac.columns = ["MA_Rápida", "MA_Lenta", "Cruce"]
        
        # Guardar como atributo el cálculo
        self.calculo_estrategia = mac
        
        # Revisar si se generó una señal
        if mac["Cruce"].iloc[-2] != mac["Cruce"].iloc[-1]: # Ocurrió un cambio de tendencia
            # Revisar tendencia
            if mac["Cruce"].iloc[-1] == 1:
                return {"tendencia": "alcista"}
            else:
                return {"tendencia": "bajista"}
        else:
            return False

    
    # Optimizar
    def optimizar(self, rango_cp: list, rango_lp: list) -> pd.DataFrame:
        
        """
        Este método optimiza los parámetros de la estrategia.
        
        Parámetros
        ----------
        param : list : rango_cp : Límite inferior y superior del periodo corto.
        ----------
        param : list : rango_lp : Límite inferior y superior del periodo largo.
        
        Salida
        -------
        return: pd.DataFrame : DataFrame con rendimientos para cada combinación de parámetros.
        """
        
        # Optimizar
        combinaciones = []
        for i in range(rango_cp[0], rango_cp[1] + 1):
            for l in range(rango_lp[0], rango_lp[1] + 1):
                combinaciones.append([i, l])
        # Guardar parámetros iniciales
        ventana_cp = self.ventana_cp
        ventana_lp = self.ventana_lp
        # Probar todas las combinaciones
        rendimientos = []
        for v_cp, v_lp in combinaciones:
            # Modificar valores de la estrategia
            self.ventana_cp = v_cp
            self.ventana_lp = v_lp
            # Calcular estrategia con valores actualizados
            self.calcular()
            # Backtest
            retornos = self.backtest()
            # Agregar los rendimientos y los parámetros
            rendimientos.append([v_cp, v_lp, retornos[-1]])
        # Convertir a DataFrame
        rendimientos = pd.DataFrame(rendimientos, columns=["Ventana CP", "Ventana LP", "Retorno Final"])
        # Ordenar de Mayor a Menor
        rendimientos = rendimientos.sort_values(by="Retorno Final", ascending=False)
        
        # Regresar valores originales
        self.ventana_cp = ventana_cp
        self.ventana_lp = ventana_lp
        self.calcular()
        
        return rendimientos
    
    
    # Plot
    def plot(self, ruta: str = "Estrategia1_PromediosMóviles.png"):
        
        """
        Este método realiza el gráfico de nuestros datos y estrategia.
        
        Parámetros
        ----------
        param : str : ruta : Ruta donde se guardará el gráfico (por defecto, se establece "Estrategia1_PromediosMóviles.png").
        
        Salida
        -------
        return: NoneType : None
        """
        
        # Calcular
        mpf.plot(self.df, type="candle", style="yahoo", title=dict(title="Gráfico Estrategia 1 - Cruce de Proedio Móviles", fontsize=20,
                                                                   y=0, x=0.55), mav=(self.ventana_cp, self.ventana_lp), 
                 ylabel="Precio", ylabel_lower="Volumen", volume=True, warn_too_much_data=self.df.shape[0], savefig=ruta,
                 figsize=(22, 12), tight_layout=True)

if __name__ == "__main__":
    
    # Obtener datos
    df = yf.download("MSFT", start="2021-01-01", end="2024-01-01", interval="1d")
    # Instanciar clase
    est1 = Estrategia1(df=df, ventana_cp=9, ventana_lp=21, columna="Close")
    # Calcular estrategia
    calculo = est1.calcular()
    print(calculo)
    
    # Ejemplo que si genere una señal
    print(Estrategia1(df=df[:-1], ventana_cp=9, ventana_lp=21, columna="Close").calcular())
    
    # Backtest
    backtest = est1.backtest()
    print("Rendimiento final con Parámetros Actuales:", backtest.iloc[-1])    
    # Optimizar
    rango_cp = [5, 25]
    rango_lp = [26, 200]
    inicio = time.time()
    rendimientos = est1.optimizar(rango_cp=rango_cp, rango_lp=rango_lp)
    print(rendimientos)
    print("Tómo {} segundos".format(time.time() - inicio))
    
    # Ajustar mejores parámetros
    est1 = Estrategia1(df=df, ventana_cp=int(rendimientos.iloc[0, 0]), ventana_lp=int(rendimientos.iloc[0, 1]))
    est1.calcular()
    # Backtest
    backtest = est1.backtest()
    print("Rendimiento final con Parámetros Optimizados:", backtest.iloc[-1]) 
    # Guardar gráfico
    est1.plot()
