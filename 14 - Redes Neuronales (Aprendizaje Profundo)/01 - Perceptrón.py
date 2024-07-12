# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import torch # conda install pytorch | pip install torch 
import torch.nn as nn
import torch.optim as optim 
import matplotlib.pyplot as plt
import networkx as nx # pip install networkx

# Datos de Entrenamiento
df = pd.DataFrame(data=[[5, 6, 2, 4, 1.5, 5.5, 6, 9, 12, 0, 14, 8, 3, 8.5, 2.5, 10, 0.5, 13],
                        [6, 7, 8, 4, 6, 7, 9, 8, 7, 5, 6, 7, 10, 6, 7, 8, 6, 5],
                        [1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1]]).T
df.columns = ["Horas Estudiadas", "Horas de Sueño", "Aprobar"]
print(df)

# Preparar datos
X = torch.tensor(df[["Horas Estudiadas", "Horas de Sueño"]].values, dtype=torch.float32)
y = torch.tensor(df["Aprobar"].values, dtype=torch.float32).view(-1, 1)

# Establecer la semilla
torch.manual_seed(1)
np.random.seed(1)

# Definir modelo (Perceptrón)
perceptron = nn.Sequential(
    nn.Linear(in_features=2, out_features=1),
    nn.Sigmoid()
    )

# Función para graficar la estructura del perceptrón
def plot_perceptron() -> None:
    
    """
    Función que grafica la estructura del Perceptrón
    """
    
    # Crear grafo dirigido
    G = nx.DiGraph()
    G.add_nodes_from([1, 2], layer=0)
    G.add_nodes_from([3], layer=1)
    G.add_edges_from([(1, 3), (2, 3)])
    pos = nx.multipartite_layout(G, subset_key="layer")
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.title("Estructura del Perceptrón")
    plt.show()
    
# Graficar la estructura del Perceptrón
plot_perceptron()
    
# Definir la función de pérdida y el optimizador
loss_func = nn.BCELoss()
optimizer = optim.SGD(perceptron.parameters(), lr=0.1) 

# Listas para guardar los valores de pérdida y precisión
loss_values = []
accuracy_values = []

# Entrenamiento del modelo
num_epochs = 1_000
for epoch in range(num_epochs):
    # Paso forward
    outputs = perceptron(X)
    loss = loss_func(outputs, y)
    
    # Paso backward y optimización
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # Calcular y almacenar la pérdida
    loss_values.append(loss.item())
    
    # Calcular la precisión
    predicted = (outputs > 0.5).float()
    accuracy = (predicted == y).float().mean().item()
    accuracy_values.append(accuracy)
    
    # Imprimir pérdida y precisión cada 100 iteraciones
    if (epoch + 1) % 100 == 0:
        print(f"Epoch [{epoch + 1} / {num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}")

# Graficar la pérdida y la precisión
epochs = range(1, len(loss_values) + 1)

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 6))

# Gráfico de Pérdida (Optimización del Modelo)
axes[0, 0].plot(epochs, loss_values, "b--", label="Pérdida")
axes[0, 0].set_xlabel("Iteraciones")
axes[0, 0].set_ylabel("Pérdida")
axes[0, 0].set_title("Pérdida durante el Entrenamiento", size=20)
axes[0, 0].legend()

# Gráfico de Presición (Optimización del Modelo)
axes[0, 1].plot(epochs, accuracy_values, "g--", label="Precisión")
axes[0, 1].set_xlabel("Iteraciones")
axes[0, 1].set_ylabel("Precisión")
axes[0, 1].set_title("Precisión durante el Entrenamiento", size=20)
axes[0, 1].legend()

# Datos Originales
axes[1, 0].scatter(df["Horas Estudiadas"][df["Aprobar"] == 1],
                   df["Horas de Sueño"][df["Aprobar"] == 1], color="green", label="Aprobados")
axes[1, 0].scatter(df["Horas Estudiadas"][df["Aprobar"] == 0],
                   df["Horas de Sueño"][df["Aprobar"] == 0], color="red", label="No Aprobados")
axes[1, 0].set_xlabel("Horas Estudiadas")
axes[1, 0].set_ylabel("Horas de Sueño")
axes[1, 0].set_title("Datos Originales", size=20)
axes[1, 0].legend()

# Datos Predicciones
pred = np.round(perceptron(X).detach().numpy()).flatten()
axes[1, 1].scatter(df["Horas Estudiadas"][pred == 1],
                   df["Horas de Sueño"][pred == 1], color="green", label="Predicción de Aprobados")
axes[1, 1].scatter(df["Horas Estudiadas"][pred == 0],
                   df["Horas de Sueño"][pred == 0], color="red", label="Predicción de No Aprobados")
axes[1, 1].set_xlabel("Horas Estudiadas")
axes[1, 1].set_ylabel("Horas de Sueño")
axes[1, 1].set_title("Predicciones del Modelo", size=20)
axes[1, 1].legend()
    
# Extraer los pesos del modelo
weights = perceptron[0].weight.detach().numpy()  
b = perceptron[0].bias.detach().numpy()
    
# Calcular los coeficientes de la línea de frontera de decisión
w1, w2 = weights[0]
b = b[0]
slope = -w1 / w2
intercept = -b / w2

# Trazar la frontera de decisión como una línea 
x_vals = np.array([df["Horas Estudiadas"].min(), df["Horas Estudiadas"].max()])
y_vals = slope *  x_vals + intercept
axes[1, 1].plot(x_vals, y_vals, "k--", lw=2, label="Frontera de Decisión")
axes[1, 1].legend()

plt.tight_layout()
plt.show()
    
# Recordatorio:
#   - Las Redes Neuronales son modelos computacionales inspirados en el cerebro humano, utilizados para resolver problemas complejos
#     de aprendizaje profundo.
#   - El Perceptrón es la unidad básica de una red neuronal, capaz de realizar operaciones simples de clasificación y aprendizaje supervisado.
