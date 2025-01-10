# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
from hmmlearn import hmm # pip install hmmlearn==0.3.2
import matplotlib.pyplot as plt

# Generar los datos de la función de Seno
t = np.linspace(start=0, stop=8*np.pi, num=1500) # Tiempo
señal = np.sin(t)

# Visualizar la señal generado
plt.figure(figsize=(22, 12))
plt.plot(t, señal, label="Función de Seno")
plt.title("Señal observada: Función de Seno")
plt.xlabel("Tiempo")
plt.ylabel("Valor")
plt.legend()
plt.grid()
plt.show()

# Preparar los datos para entrenar el modelo
obs = señal.reshape(-1, 1)

# Definir el modelo HMM con 2 estados ocultos
modelo = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)

# Ajustar el modelos a los datos observados
modelo.fit(obs)

# Predicción de los datos ocultos
hidden_states = modelo.predict(obs)

# Visualizar los estados ocultos junto con la señal observada
plt.figure(figsize=(22, 12))
plt.scatter(t[hidden_states==0], señal[hidden_states==0], label="Función Seno con Estado 0", color="blue")
plt.scatter(t[hidden_states==1], señal[hidden_states==1], label="Función Seno con Estado 1", color="red")
plt.title("Estados Ocultos en la Señal Observada")
plt.xlabel("Tiempo")
plt.ylabel("Valor")
plt.legend()
plt.grid()
plt.show()

# Interpretación de los estados ocultos
for i in range(modelo.n_components):
    longitud_estados = sum(hidden_states == i)
    print(f"Estado {i}: Duración: {longitud_estados}")
    print(f"Estado {i} representa un porcentaje de {longitud_estados/hidden_states.shape[0]}\n")

# Recordatorio:
#   - Los estados de Markov representan condiciones discretas que un sistema puede ocupar en un momento dado.
#   - En un modelo de Markov, solo importa el estado actual para predecir el siguiente paso.
