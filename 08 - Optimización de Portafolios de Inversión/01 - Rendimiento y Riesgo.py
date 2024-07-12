# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Obtener datos históricos
tickers_lista = ["AMZN", "TSLA", "MSFT", "NFLX", "META", "PYPL"]
datos = {}
for ticker in tickers_lista:
    datos[ticker] = yf.download(ticker, start="2023-01-01", end="2024-01-01", interval="1d")
    
# Graficar Precios
plt.figure(figsize=(22, 12))
for ticker in tickers_lista:
    datos[ticker]["Close"].plot(label=ticker)
plt.legend()
plt.grid()
plt.show()

# Calcular rendimientos diarios
rendimientos = pd.DataFrame(columns=tickers_lista)
for ticker in tickers_lista:
    rendimientos[ticker] = datos[ticker]["Close"].pct_change()
print(rendimientos)

# Graficar rendimientos
rendimientos.plot(figsize=(22, 12), title="Rendimientos de los Activos")
plt.show()

# Obtener rendimiento anualizado
rendimientos_promedios_diarios = rendimientos.mean(axis=0)
rendimiento_anual = rendimientos_promedios_diarios * 252
print("Rendimiento anual de cada instrumento:\n")
print(rendimiento_anual)

# Obtener la volatilidad
volatilidad_promedio_diaria = rendimientos.std(axis=0)
volatilidad_anual = volatilidad_promedio_diaria * np.sqrt(252)
print("Volatilidad anual de cada instrumento:\n")
print(volatilidad_anual)

# Graficar rendimientos vs volatilidad
x_valores = volatilidad_anual.values
y_valores = rendimiento_anual.values
plt.figure(figsize=(22, 12))
plt.plot(x_valores, y_valores, "ro", ms=20)
# Agregar etiquetas
for ticker in tickers_lista:
    x = volatilidad_anual[ticker]
    y = rendimiento_anual[ticker]
    plt.text(x, y, ticker, ha="left", va="bottom", fontsize=10, fontweight="bold", rotation = 45)
plt.xlabel("Volatilidad $\sigma$", size=25)
plt.ylabel("Rendimiento Anual $E[r]$", size=25)
plt.grid()
plt.show()

# Recordatorio:
#   - Un rendimiento esperado más alto generalmente conlleva asumir un nivel de riesgo mayor.
#   - La diversificación de activos en un portafolio puede reducir significativamente el riesgo,
#     permitiendo alcanzar rendimientos similares con menor volatilidad.
