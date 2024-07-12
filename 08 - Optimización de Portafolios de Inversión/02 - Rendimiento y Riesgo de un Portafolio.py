# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Obtener datos
activos = ["AAPL", "MSFT", "GOOGL", "DIS"]
precios = yf.download(tickers=activos, start="2023-01-01", end="2024-01-01", interval="1d")

precios = precios["Close"]
# Ordenarlos en base a las columnas
precios = precios[activos]

# Graficar precios
colores = ["red", "green", "blue", "orange"]
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(22, 12))
for n, ax in enumerate(axes.flatten()):
    precios[activos[n]].plot(color=colores[n], lw=2, ax=ax, label=activos[n], title="Precios de Cierre:" + activos[n])
    ax.grid()
    ax.legend()
plt.tight_layout()
plt.show()

# Obtener rendimientos
rendimientos = precios.pct_change()
# Rendimientos y volatilidad diaria
rendimientos_diarios_promedio = rendimientos.mean()
volatilidad_diaria_promedio = rendimientos.std()

# Unir en un dataframe
rend_vol_diaria = pd.DataFrame(columns=["Rendimiento Diario Promedio", "Volatilidad Diaria Promedio"], index=activos)
rend_vol_diaria["Rendimiento Diario Promedio"] = rendimientos_diarios_promedio
rend_vol_diaria["Volatilidad Diaria Promedio"] = volatilidad_diaria_promedio

# Datos anualizados
rend_vol_anual = pd.DataFrame(columns=["Rendimiento Anual Promedio", "Volatilidad Anual Promedio"], index=activos)
rend_vol_anual["Rendimiento Anual Promedio"] = rendimientos_diarios_promedio * 252
rend_vol_anual["Volatilidad Anual Promedio"] = volatilidad_diaria_promedio * np.sqrt(252)

# Crear Portafolios de Inversión

# Portafolio 1: 25% AAPL, 25% MSFT, 25% GOOGL, 25% DIS
apple_porcentaje = 0.25
microsoft_porcentaje = 0.25
google_porcentaje = 0.25
disney_porcentaje = 0.25
portafolio1 = rendimientos["AAPL"] * apple_porcentaje + rendimientos["MSFT"] * microsoft_porcentaje + \
    rendimientos["GOOGL"] * google_porcentaje + rendimientos["DIS"] * disney_porcentaje

# Portafolio 2: 30% AAPL, 30% MSFT, 30% GOOGL, 10% DIS
apple_porcentaje = 0.30
microsoft_porcentaje = 0.30
google_porcentaje = 0.30
disney_porcentaje = 0.10
portafolio2 = rendimientos["AAPL"] * apple_porcentaje + rendimientos["MSFT"] * microsoft_porcentaje + \
    rendimientos["GOOGL"] * google_porcentaje + rendimientos["DIS"] * disney_porcentaje

# Portafolio 3: 15% AAPL, 25% MSFT, 40% GOOGL, 20% DIS
apple_porcentaje = 0.15
microsoft_porcentaje = 0.25
google_porcentaje = 0.40
disney_porcentaje = 0.20
portafolio3 = rendimientos["AAPL"] * apple_porcentaje + rendimientos["MSFT"] * microsoft_porcentaje + \
    rendimientos["GOOGL"] * google_porcentaje + rendimientos["DIS"] * disney_porcentaje
    
# Portafolio 4: 33% AAPL, 33% MSFT, 33% GOOGL, 1% DIS
apple_porcentaje = 0.33
microsoft_porcentaje = 0.33
google_porcentaje = 0.33
disney_porcentaje = 0.01
portafolio4 = rendimientos["AAPL"] * apple_porcentaje + rendimientos["MSFT"] * microsoft_porcentaje + \
    rendimientos["GOOGL"] * google_porcentaje + rendimientos["DIS"] * disney_porcentaje

# Unir el rendimiento y volatilidad anualizada de cada portafolio a los datos existentes
rend_vol_anual.loc["Portafolio 1"] = [portafolio1.mean() * 252, portafolio1.std() * np.sqrt(252)]
rend_vol_anual.loc["Portafolio 2"] = [portafolio2.mean() * 252, portafolio2.std() * np.sqrt(252)]
rend_vol_anual.loc["Portafolio 3"] = [portafolio2.mean() * 252, portafolio3.std() * np.sqrt(252)]
rend_vol_anual.loc["Portafolio 4"] = [portafolio2.mean() * 252, portafolio4.std() * np.sqrt(252)]

# Graficar cada activo (rendimiento esperado vs volatilidad)
plt.figure(figsize=(22, 12))
plt.plot(rend_vol_anual["Volatilidad Anual Promedio"], rend_vol_anual["Rendimiento Anual Promedio"], "ro", ms=20)
# Agregar Etiquetas
for etiqueta in rend_vol_anual.index:
    plt.text(rend_vol_anual.loc[etiqueta, "Volatilidad Anual Promedio"], rend_vol_anual.loc[etiqueta, "Rendimiento Anual Promedio"],
             etiqueta, ha="left", va="bottom", fontsize=10, fontweight="bold", rotation=45)
plt.xlabel("Volatilidad $\sigma$", size=25)
plt.ylabel("Rendimiento Anual $E[r]$", size=25)
plt.grid()
plt.show()

# Recordatorio:
#   - La diversificación puede reducir la exposición al riesgo y mejorar el rendimiento.
#   - La diversificación nos puede proteger contra eventos específicos del mercado que afecten a un grupo de activos.
