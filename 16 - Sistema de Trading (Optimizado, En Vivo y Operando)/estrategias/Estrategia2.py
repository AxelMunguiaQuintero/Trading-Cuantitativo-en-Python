# Librerías Estándar
import pandas as pd
import numpy as np
import yfinance as yf
import time
import mplfinance as mpf
# Librerías Propias
...


# Clase Estrategia
class Estrategia2:
    
    """ 
    Estrategia 2: Estrategia de Supertendencia
        
        Descripción:
            
            Estrategia que utiliza el indicador de SuperTendencia para identificar señales de compra y venta 
            basadas en la dirección predominante de la tendencia del mercado.
        
    Estrategia Para:
        
        - Acciones
        - Índices
        - ETFs
        - Divisas
        - Materias Primas
        - Criptmonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - Intradía
        - Diario
        - Semanal
        - Mensual
        
    Periodo de Retención:
        
        - Variable (Depende de la fuerza de la tendencia)
        
    Análisis Usado: 
        
        - Análisis Técnico
            * SuperTendencia
    
    Descripción Detallada de la Estrategia:    
        
        Estrategia que utiliza el indicador de Supertendencia para determinar la dirección de la tendencia predominante. 
        Se considera una señal de compra cuando el precio cruza por encima de la línea de Supertendencia (indicando una 
        tendencia alcista), y una señal de venta cuando el precio cruza por debajo de la línea de Supertendencia (indicando
        una tendencia bajista).
                        
        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                La toma de ganancia se activa cuando se produce una señal contraria a la de la posición actual.
                
            Stop Loss:
                
                La limitación de pérdidas ocurre cuando se produce una señal contraria a la de la posición actual.
                
    Supuestos Generales:
        
        - Esta estrategia no considera costos o comisiones (Comisiones de apertura, rollovers, entre otros).
        - En situaciones de alta volatilidad, como eventos de noticias o resultados trimestrales que afecten 
          significativamente el precio (para acciones), el indicador de Supertendencia puede producir señales 
          falsas debido a movimientos bruscos y temporales del mercado.
        
    Notas:
        
        - Recordar que las líneas que se dibujan en el gráfico no solo indican la tendencia actual del mercado, sino que 
          también pueden funcionar como niveles de soporte o resistencia, proporcionando información adicional para la 
          toma de decisiones de trading.
    """
    
    __version__ = 1.0
    
    # __init__
    def __init__(self, df: pd.DataFrame, longitud: int = 14, factor: float = 3.0) -> None:
        
        """
        Constructor.
        
        Parámetros
        ----------
        param : pd.DataFrame : df : Datos históricos del activo financiero.
        ----------
        param : int : longitud : Ventana a utilizar en ATR para el cálculo de ST (por defecto, se establece en 14).
        ----------
        param : float : factor : Multiplicador de cálculo para el ATR (por defecto, se establece en 3.0).
        
        Salida
        -------
        return: NoneType : None
        """
        
        # Atributos
        self.df = df
        self.longitud = longitud
        self.factor = factor
        self.calculo_estrategia = None
        # Atributos Privados
        
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self) -> pd.DataFrame:
        
        """
        Este método obtiene el rendimiento generado con la estrategia de SuperTendencia.
        
        Salida
        -------
        return: pd.DataFrame : Rentabilidad de la estrategia a lo largo del tiempo.
        """
        
        # Calcular
        if self.calculo_estrategia is None:
            self.calcular()
        datos = self.calculo_estrategia.copy()
        tendencia = np.where(datos["FinalLowerB"].notna(), 1, -1)
        datos["tendencia"] = tendencia
        # Calcular rendimiento
        datos["rendimiento"] = self.df["Close"].pct_change()
        rendimiento = (1 + datos["tendencia"].shift(periods=1) * datos["rendimiento"]).cumprod()
        
        return rendimiento
    
    
    # Calcular
    def calcular(self) -> dict:
        
        """
        Este método calcula el indicador de SuperTendencia a partir de los datos históricos que fueron pasados como parámetro.
        
        Salida
        -------
        return: dict|bool : Un diccionario si se ha generado una señal en la última vela, o False si no se ha generado nada.
        """
        
        # Calcular True Range (TR)
        High, Low = self.df["High"], self.df["Low"]
        H_minus_L = High - Low
        prev_close = self.df["Close"].shift(periods=1)
        H_minus_PC = abs(High - prev_close)
        L_minus_PC = abs(Low - prev_close)
        TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=self.df.index, name="TR")
        
        # Calcular ATR (Average True Range)
        ATR = TR.ewm(alpha = 1 / self.longitud).mean()
        
        # Calcular valores básicos
        medio = ((High + Low) / 2)
        FinalUpperB = medio + self.factor * ATR
        FinalLowerB = medio - self.factor * ATR
        
        # Inicializar SuperTendencia
        Supertendencia = np.zeros(ATR.shape[0])
        close = self.df["Close"]
        
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
        FU = FinalUpperB[self.longitud - 1:]
        FL = FinalLowerB[self.longitud - 1:]
        ST_df = pd.concat([FU, FL], axis=1)
        ST_array = np.nansum([FU, FL], axis=0)
        ST_array[0] = np.nan
        ST_df["SuperTendencia"] = ST_array
        ST_df.columns = ["FinalUpperB", "FinalLowerB", "SuperTendencia"]
        
        # Guardar el cálculo como atributo
        self.calculo_estrategia = ST_df
        
        # Revisar si se generó una señal
        if pd.isna(ST_df["FinalUpperB"].iloc[-2]) & pd.notna(ST_df["FinalUpperB"].iloc[-1]): # Nueva Tendencia Bajista
            valor = {"tendencia": "bajista"}
        elif pd.isna(ST_df["FinalLowerB"].iloc[-2]) & pd.notna(ST_df["FinalLowerB"].iloc[-1]): # Nueva Tendencia Alcista
            valor = {"tendencia": "alcista"}
        else:
            valor = False

        return valor
    
    
    # Optimizar
    def optimizar(self, rango_periodos: list, rango_factores: list) -> pd.DataFrame:
        
        """
        Este método optimiza los parámetros de la estrategia para maximizar la utilidad.
        
        Parámetros
        ----------
        param : list : rango_periodo : Limite inferior y el limite superior de la longitud.
        ----------
        param : list : rango_factores : Limite inferior y el limite superior de los factores.
                
        
        Salida
        -------
        return: pd.DataFrame : Los rendimientos para cada estrategia que se ha probado.
        """
        
        # Optimizar
        combinaciones = []
        for l in range(rango_periodos[0], rango_periodos[1] + 1):
            for r in range(rango_factores[0], rango_factores[1] + 1):
                combinaciones.append([l, r])
        # Guardar los valores iniciales
        longitud = self.longitud
        factor = self.factor
        # Probar combinaciones
        rendimientos = []
        for long, fact in combinaciones:
            # Modificar valores para calcular la estrategia
            self.longitud = long
            self.factor = fact
            # Calcular estrategia con valores actualizados
            self.calcular()
            # Backtest
            rend = self.backtest()
            # Agregar rendimiento y parámetros
            rendimientos.append([long, fact, rend[-1]])
            
        # Convertir a un dataframe
        rendimientos = pd.DataFrame(data=rendimientos, columns=["Longitud", "Factor", "Rendimiento Total"])
        # Order en base a los rendimientos (mayor a menor)
        rendimientos = rendimientos.sort_values(by="Rendimiento Total", ascending=False)

        # Regresar valores originales
        self.longitud = longitud
        self.factor = factor
        self.calcular()
        
        return rendimientos
    
    
    # Plot
    def plot(self, ruta: str = "Estrategia2_SuperTendencia.png") -> None:
        
        """
        Este método realiza una representación gráfica de nuestros datos junto con nuestro indicador.
        
        Parámetros
        ----------
        param : str : ruta : Ruta donde se guardará el gráfico (por defecto, se establece "Estrategia2_SuperTendencia.png")
        
        Salida
        -------
        return: NoneType : None.
        """
        
        # Graficar
        sp_plots = [
            
            mpf.make_addplot(self.calculo_estrategia["SuperTendencia"], label="Cambio de Tendencia", color="black"),
            mpf.make_addplot(self.calculo_estrategia["FinalUpperB"], label="Tendencia Bajista", color="red"),
            mpf.make_addplot(self.calculo_estrategia["FinalLowerB"], label="Tendencia Alcista", color="green")
            
            ]
        
        mpf.plot(self.df.loc[self.calculo_estrategia.index], type="candle", style="yahoo", volume=True, figsize=(22, 12),
                 title=dict(title="Gráfico Estrategia 2 - SuperTendencia", fontsize=20, y=0, x=0.55), ylabel="Precio",
                 ylabel_lower="Volumen", savefig=ruta, addplot=sp_plots, figscale=3.0, tight_layout=True, 
                 warn_too_much_data=self.df.loc[self.calculo_estrategia.index].shape[0])
        
if __name__ == "__main__":
    
    # Obtener datos
    df = yf.download("AMZN", start="2022-01-01", end="2024-01-01", interval="1d")
    # Inicializar estrategia
    est2 = Estrategia2(df=df, longitud=14, factor=3.0)
    # Calcular
    calculo = est2.calcular()
    print(calculo)
    
    # Ejemplo de una señal
    print(Estrategia2(df=df.loc[:"2023-10-30"], longitud=14, factor=3.0).calcular())
    
    # Backtest
    backtest = est2.backtest()
    print("Rendimiento Final con Parámetros Actuales:", backtest.iloc[-1])
    # Optimizar
    rango_long = [5, 100]
    rango_factores = [1, 5]
    inicio = time.time()
    rendimientos = est2.optimizar(rango_periodos=rango_long, rango_factores=rango_factores)
    print(rendimientos)
    print("Tomó {} segundos".format(time.time() - inicio))
    
    # Ajustar los mejores parámetros
    est2 = Estrategia2(df=df, longitud = int(rendimientos.iloc[0, 0]), factor= int(rendimientos.iloc[0, 1]))
    est2.calcular()
    # Backtest
    backtest = est2.backtest()
    print("Rendimiento Final con Parámetros Actuales:", backtest.iloc[-1])
    # Guardar el gráfico
    est2.plot()
