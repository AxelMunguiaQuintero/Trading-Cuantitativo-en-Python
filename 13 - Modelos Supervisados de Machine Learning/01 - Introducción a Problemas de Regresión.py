# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
from xgboost import XGBRegressor # pip install xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


# Leer datos
df = pd.read_csv("../datos/housing.csv", sep=",")
columnas = df.columns

# Conocer la distribución de las variables
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(22, 12))

for n, i in enumerate(axes.flatten()):
    
    if n < 14:
        df[columnas[n]].plot(kind="hist", ax=i)
        i.set_title(columnas[n])
    else:
        i.axis("off")
        i.text(0.5, 0.5, "Gráficos de Distribución de Cada Columna", fontsize=14,
               ha="center", va="center", weight="bold")

plt.tight_layout()
plt.show()

# Separar los Datos de Entrenamiento y de Prueba
X = df.drop("MEDV", axis=1) # Variables predictoras (todas menos MEDV)
y = df["MEDV"] # Variable objetivo (valor medio de las viviendas)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

# Crear el modelo y entrenar
modelo = XGBRegressor(max_depth=2, objective="reg:squarederror", random_state=1)
modelo.fit(X_train, y_train)

# Predecir los valores de entrenamiento y de prueba
y_train_pred = modelo.predict(X_train)
plt.figure(figsize=(22, 12))
plt.scatter(y_train, y_train_pred)
plt.ylabel("Valores Reales (y_train)")
plt.xlabel("Predicciones (y_train_pred)")
plt.title("Predicciones vs Valores Reales en conjunto de Entrenamiento")
plt.show()

y_test_pred = modelo.predict(X_test)
plt.figure(figsize=(22, 12))
plt.scatter(y_test, y_test_pred)
plt.ylabel("Valores Reales (y_test)")
plt.xlabel("Predicciones (y_test_pred)")
plt.title("Predicciones vs Valores Reales en conjunto de Prueba")
plt.show()


# Calcular y mostrar el error cuadrático medio (MSE) en el conjunto de entrenamiento
mse_entrenamiento = mean_squared_error(y_true=y_train, y_pred=y_train_pred)
print("Error cuadrático medio (MSE) en conjunto de entrenamiento:", mse_entrenamiento)

# Calcular y mostrar el error cuadrático medio (MSE) en el conjunto de prueba
mse_prueba = mean_squared_error(y_true=y_test, y_pred=y_test_pred)
print("Error cuadrático medio (MSE) en conjunto de prueba:", mse_prueba)

# Recordatorio:
#   - XGBoost es un potente algoritmo de aprendizaje autmático que utiliza árboles de decisión y técnicas
#     de refuerzo para mejorar continuamente la precisión del modelo.
