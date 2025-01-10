# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import yfinance as yf
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Obtener datos
start="2021-01-01"
end="2024-01-01"
ticker="SPY"
df = yf.download(ticker, start, end, interval="1d")

# Agregar los retornos logarítmicos y el rango diario de cada vela
df["log_r"] = np.log(df["Close"] / df["Close"].shift(periods=1))
df["rango"] = df["High"].div(df["Low"]) - 1

# Definir el modelo con 2 estados ocultos
modelo = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)

# Ajustar el modelo
datos = df[["log_r", "rango"]].dropna()
modelo.fit(datos)

# Predecir
hidden_states = modelo.predict(datos)

# Separar Estados Ocultos
Close = df.dropna()["Close"]
estado0 = Close.where(hidden_states==0, np.nan)
estado1 = Close.where(hidden_states==1, np.nan)

# Visualizar
plt.figure(figsize=(22, 12))
plt.plot(estado0, color="green", label="Tendencia Alcista")
plt.plot(estado1, color="red", label="Tendencia Bajista")
plt.title("Estados Ocultos en el ETF (SPY) - Alcista/Bajista")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.legend()
plt.grid()
plt.show()

# Recordatorio:
#   - Para detectar las tendencias del mercado con el modelo HMM, debemos adaptar los datos para proporcionar la información
#     necesaria que el modelo requiere.
