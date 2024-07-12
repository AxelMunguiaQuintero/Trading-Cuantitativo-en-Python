# -*- coding: utf-8 -*-
# Importar librerí­as
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Obtener precios de cierre
activos = ["AAPL", "MSFT", "GOOGL", "DIS"]
precios = yf.download(tickers=activos, start="2023-01-01", end="2024-01-01", interval="1d")
# Acomodar en Orden
precios = precios["Close"][activos]

# Obtener rendimientos
rendimientos = precios.pct_change()

# Observar correlación entre activos
correlacion = rendimientos.corr()
plt.figure(figsize=(22, 12), dpi=100)
sns.heatmap(correlacion, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Matriz de Correlación de Rendimientos")
plt.show()

# Calcular la matriz de covarianza
covarianza = rendimientos.cov()

# Pesos del portafolio para cada activo
pesos = np.array([0.33, 0.33, 0.33, 0.01])

# Rendimientos del portafolio anualizado
rendimiento_portafolio = (rendimientos * pesos).sum(axis=1).mean() * 252
print("Rendimiento anual del portafolio de inversión esperado:", rendimiento_portafolio)

# Volatilidad del portafolio anualizada
volatilidad_portafolio = np.sqrt(np.dot(pesos, np.dot(covarianza, pesos))) * np.sqrt(252)
print("Volatilidad anual del portafolio:", volatilidad_portafolio)

# Crear Portafolios (15,000 distintos portafolios)
numero_portafolios = 15_000
# Almacenar resultados en un array (rendimiento, volatilidad, sharpe-ratio)
resultados = np.zeros((3, numero_portafolios))
pesos_lista = []
# Iterar para crear los 15,000 portafolios distintos
for i in range(numero_portafolios):
    # Selecionar pesos random
    pesos = np.random.random(4)
    # Rebalancear los pesos para que sumen 1
    pesos = pesos / np.sum(pesos)
    
    # Calcular retorno y la volatilidad del portafolio
    retorno_portafolio = (rendimientos * pesos).sum(axis=1).mean() * 252
    volatilidad_portafolio = np.sqrt(np.dot(pesos, np.dot(covarianza, pesos))) * np.sqrt(252)
    
    # Almacenar los resultados
    resultados[0, i] = retorno_portafolio
    resultados[1, i] = volatilidad_portafolio
    resultados[2, i] = (retorno_portafolio - 0.03) / volatilidad_portafolio
    pesos_lista.append(pesos)
    
# Convertir datos en un dataframe
resultados = pd.DataFrame(resultados.T, columns=["Retorno Anual", "Volatilidad Anual", "Sharpe-Ratio"])
# Graficar portafolios
plt.figure(figsize=(22, 12))
plt.scatter(resultados["Volatilidad Anual"], resultados["Retorno Anual"], c=resultados["Sharpe-Ratio"], cmap="RdYlBu",
            edgecolors="black", linewidths=0.45, s=50)
plt.title("Rendimiento Esperado vs Volatilidad", size=25)
plt.xlabel("Volatilidad Anual $\sigma$", size=25)
plt.ylabel("Rendimiento Anual $E[r]$", size=25)
plt.colorbar()
plt.tight_layout()
plt.show()

# Encontrar el portafolio de mínima varianza
min_volatilidad_portafolio = resultados.iloc[resultados["Volatilidad Anual"].idxmin()]
print("Portafolio de Mínima Varianza:\n")
print(min_volatilidad_portafolio, end="\n"*2)
print("Los pesos para este portafolio son:", list(zip(activos, pesos_lista[resultados["Volatilidad Anual"].idxmin()])))

# Encontrar el portafolio con el mayor coeficiente de Sharpe
max_sharpe_portafolio = resultados.iloc[resultados["Sharpe-Ratio"].idxmax()]
print("Portafolio con mayor Sharpe-Ration\n:")
print(max_sharpe_portafolio)
print("Los pesos para este portafolio son:", list(zip(activos, pesos_lista[resultados["Sharpe-Ratio"].idxmax()])))

# Graficar nuevamente los portafolios
plt.figure(figsize=(22, 12))
plt.scatter(resultados["Volatilidad Anual"], resultados["Retorno Anual"], c=resultados["Sharpe-Ratio"], cmap="RdYlBu",
            edgecolors="black", linewidths=0.45, s=50)
plt.colorbar()
plt.scatter(min_volatilidad_portafolio["Volatilidad Anual"], min_volatilidad_portafolio["Retorno Anual"],
            marker="X", color="r", s=500, edgecolors="black", lw=3, label="Portafolio con Menor Varianza")
plt.scatter(max_sharpe_portafolio["Volatilidad Anual"], max_sharpe_portafolio["Retorno Anual"],
            marker="X", color="yellow", s=500, edgecolors="black", lw=3, label="Portafolio con Mayor Sharpe-Ratio")
plt.title("Rendimiento Esperado vs Volatilidad", size=25)
plt.xlabel("Volatilidad Anual $\sigma$", size=25)
plt.ylabel("Rendimiento Anual $E[r]$", size=25)
plt.legend()
plt.tight_layout()
plt.show()

######## Optimización de Portafolios Eficiente ########

# Calcular la matriz de covarianza anualizada
diagonal_volatilidades = np.diag(rendimientos.std() * np.sqrt(252)) # Volatilidades anualizadas en diagonal
Sigma = diagonal_volatilidades.dot(correlacion).dot(diagonal_volatilidades) # Matriz de Covarianza Anualizada
# Sigma = rendimientos.cov() * 252

# Función objetivo para minimizar la varianza del portafolio
def varianza(pesos, sigma):
    return pesos.dot(sigma).dot(pesos)

# Definir condiciones y límites para la optimización de mínima varianza
num_activos = len(activos)
w0 = np.ones(num_activos) / num_activos
bnds = ((0, 1), ) * num_activos # Límites de pesos (entre 0 y 1)
cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

# Optimizar para encontrar el portafolio de mínima varianza
minvar = minimize(varianza, w0, args=(Sigma,), bounds=bnds, constraints=cons)

# Imprimir los resultados del portafolio de mínima varianza
pesos_optimizados = minvar.x
retorno_portafolio_optimizado = (rendimientos * pesos_optimizados).sum(axis=1).mean() * 252
volatilidad_portafolio_optimizado = np.sqrt(np.dot(pesos_optimizados, np.dot(covarianza, pesos_optimizados))) * np.sqrt(252)

print("Antiguo mejor Portafolio de Mínima Varianza:\n")
print("Rendimiento:", min_volatilidad_portafolio["Retorno Anual"])
print("Volatilidad:", min_volatilidad_portafolio["Volatilidad Anual"])
print("-----" * 20)
print("Actual mejor Portafolio de Mínima Varianza:\n")
print("Rendimiento:", retorno_portafolio_optimizado)
print("Volatilidad:", volatilidad_portafolio_optimizado)

# Función objetivo para maximizar el Sharpe-Ratio
def sharpe_ratio(pesos, sigma, rf, rendimientos_esperados):
    retorno_esperado_portafolio = rendimientos_esperados.dot(pesos)
    varianza_portafolio = pesos.dot(sigma).dot(pesos)
    
    return -(retorno_esperado_portafolio - rf) / np.sqrt(varianza_portafolio)

# Definir condiciones y límites para la optimización de mínima varianza
num_activos = len(activos)
w0 = np.ones(num_activos) / num_activos
bnds = ((0, 1), ) * num_activos # Límites de pesos (entre 0 y 1)
cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

# Tasa libre de riesgo (risk-free rate) y rendimientos esperados individuales
rf = 0.03
rendimientos_esperados = rendimientos.mean() * 252

# Optimización para encontrar el portafolio de máximo sharpe-ratio
max_sr = minimize(sharpe_ratio, w0, args=(Sigma, rf, rendimientos_esperados), bounds=bnds, constraints=cons)

# Imprimir los resultados del portafolio de mayor sharpe-ratio
pesos_optimizados_sr = max_sr.x
retorno_portafolio_optimizado_sr = (rendimientos * pesos_optimizados_sr).sum(axis=1).mean() * 252
volatilidad_portafolio_optimizado_sr = np.sqrt(np.dot(pesos_optimizados_sr, np.dot(covarianza, pesos_optimizados_sr))) * np.sqrt(252)

print("Antiguo mejor Portafolio de Mayor Sharpe-Ratio:\n")
print("Rendimiento:", max_sharpe_portafolio["Retorno Anual"])
print("Volatilidad:", max_sharpe_portafolio["Volatilidad Anual"])
print("-----" * 20)
print("Actual mejor Portafolio de Mayor Sharpe-Ratio:\n")
print("Rendimiento:", retorno_portafolio_optimizado_sr)
print("Volatilidad:", volatilidad_portafolio_optimizado_sr)

# Recordatorio:
#   - El Portafolio de Mínima Varianza es aquel que ofrece la menor volatilidad posible para un nivel dado de
#     rendimiento esperado, ideal para inversores que buscan minimizar el riesgo.
#   - Por otro lado, el Portafolio con Mayor Sharpe-Ratio representa la combinación óptima de riesgo y rendimiento,
#     siendo preferido por inversores que buscan maximizar sus retornos ajustados al riesgo.
