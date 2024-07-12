# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
from hmmlearn import hmm
import matplotlib.pyplot as plt


# Obtener datos históricos
df = yf.download("SPY", start="2019-01-01", end="2024-01-01", interval="1d")

# Crear columnas para el modelo (retornos logarítmicos y rango)
df["log_r"] = np.log(df["Close"]/df["Close"].shift(periods=1))
df["rango"] = df["High"] / df["Low"] - 1
df = df.dropna()

# Separar datos de entrenamiento y prueba
x_train = df[["log_r", "rango"]].loc[:"2021-12-31"] # Primeros 3 años de datos
x_test = df[["log_r", "rango"]].loc["2022-01-01":] # Siguientes 2 años para validar el modelo

print(f"Longitud de datos de entrenamiento: {x_train.shape[0]} - de {x_train.index[0]} a {x_train.index[-1]}")
print(f"Longitud de datos de prueba: {x_test.shape[0]} - de {x_test.index[0]} a {x_test.index[-1]}")

# Definir y ajustar el modelo con 2 estados (alcista y bajista)
modelo = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)
modelo.fit(x_train)

# Predecir datos de entrenamiento y de prueba
hidden_states_entrenamiento = modelo.predict(x_train)
hidden_states_prueba = modelo.predict(x_test)

# Comparar rendimientos de cada método de inversión con datos de prueba:
#   1. Estrategia 1: Comprar y mantener
#   2. Estrategia 2: Cruce de Promedios Móviles
#   3. Estrategia 3: Invertir en base a la predicción del Modelo de Márkov

# Datos de prueba
df_prueba = df.loc[x_test.index]


# Estrategia 1: Comprar y Mantener
df_prueba["rendimiento_estrategia1"] = (df_prueba["Close"].pct_change() + 1).cumprod()

# Estrategia 2: Cruce de Promedios Móviles
ma_9d = df_prueba["Close"].rolling(window=9).mean()
ma_21d = df_prueba["Close"].rolling(window=21).mean()
# Detectar cruces
cruce = np.where(ma_9d > ma_21d, 1, -1)
# Rellenar los nans hacia adelante de los cruces
cruce = pd.Series(cruce, index=df_prueba.index).ffill()
# Calcular retorno
rendimientos_diarios = df_prueba["Close"].pct_change()
df_prueba["rendimiento_estrategia2"] = (1 + cruce.shift(periods=1) * rendimientos_diarios).cumprod()

# Estrategia 3: Invertir en Base a la Predicción del Modelo de Márkov
estado0 = df_prueba["Close"].where(hidden_states_prueba==0, np.nan)
estado1 = df_prueba["Close"].where(hidden_states_prueba==1, np.nan)

n_continuidad = 25
estados = {"alcista": "", "bajista": ""}

# Iterar sobre las filas de cualquier estado (estado0 o estado1)
for i in range(estado0.shape[0] - n_continuidad):
    sub_estado0 = estado0.iloc[i: i + n_continuidad].dropna()
    # Revisar si hay 25 datos continuos
    if sub_estado0.shape[0] == n_continuidad:
        # Ajustar Regresión para conocer la pendiente
        params = np.polyfit(x=sub_estado0, y=range(0, n_continuidad), deg=1)
        pendiente = params[0]
        if pendiente > 0:
            estados["alcista"] = estado0
            estados["bajista"] = estado1
        else:
            estados["alcista"] = estado1
            estados["bajista"] = estado0
        # Cesar ejecución
        break
    
# Visualizar
plt.figure(figsize=(22, 12))
plt.plot(estados["bajista"], color="red", label="Tendencia Bajista")
plt.plot(estados["alcista"], color="green", label="Tendencia Alcista")
plt.title("Estados Ocultos en el ETF (SPY) - Alcista/Bajista")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.legend()
plt.grid()
plt.show()

# Obtener dirección y rendimiento
direccion = np.where(estados["alcista"].notnull(), 1, -1)
direccion = pd.Series(direccion, index=df_prueba.index, name="Direccion")
df_prueba["rendimiento_estrategia3"] = (1 + direccion.shift(periods=1) * rendimientos_diarios).cumprod()


# Graficar rendimientos para las estrategias
df_prueba[["rendimiento_estrategia1", "rendimiento_estrategia2", "rendimiento_estrategia3"]].plot(figsize=(22, 12))
plt.title("Comparativa de Rendimientos para Estrategias")
plt.xlabel("Tiempo")
plt.ylabel("Comportamiento del Capital")
plt.legend()
plt.show()

# Recordatorios:
#   - Los estados intenrnos del modelos de Márkov nos ayudan a detectar las tendencias actuales de activos financieros.
#   - El hecho de que el modelo se adapte bien a un instrumento financiero esto no significa que funcione para otro.
#   - Podemos ajustar el modelo de Márkov a un índice (como lo hicimos en esta lección) para tomar decisiones más informadas,
#     pues la mayoría de las acciones están altamente correlacionadas con los índices. Por ejemplo, si el modelo de Márkov
#     no se ajusta con una acción que tiene mucha correlación con el S&P 500, como podría ser Microsoft (MSFT), pero a través
#     de otro modelo (quizá indicadores técnicos) detectamos una tendencia alcista, entonces podríamos sumar ambos análisis para
#     mejorar precisión de nuestras inversiones.
