# -*- coding: utf-8 -*-
# Importar librerías
import threading
import time


# Definir funciones
def func1(segundos: float) -> None:
    
    """
    Función No. 1 que se ejecutará en paralelo
    """
    
    while True:
        print("Función 1 te saluda")
        time.sleep(segundos)
        
def func2(segundos: float) -> None:
    
    """
    Función No. 2 que se ejecutará en paralelo
    """
    
    while True:
        print("Función 2 te saluda")
        time.sleep(segundos)
        
# Inicializar Hilos
t0 = threading.Thread(target=func1, kwargs={"segundos": 3}, name="Hilo 1")
t1 = threading.Thread(target=func2, kwargs={"segundos": 3}, name="Hilo 2")
t0.start()
t1.start()

# Variables informativas
print("Nombre del Primer Hilo:", t0.name)
print("Nombre del Segundo Hilo:", t1.name)
print("¿Está activo el Primer Hilo?:", t0.is_alive())
print("¿Está activo el Segundo Hilo?:", t1.is_alive())

# Recordatorio:
#   - Dentro de un Proceso, se ejecutan los Hilos pudiendo un proceso albergar uno o varios hilos de ejecución.
#   - Cada Hilo dentro de un proceso comparte un espacio de memoria común, permitiéndoles acceder y modificar las
#     mismas variables y datos.
#   - A cada Hilo se le puede asignar un identificador único.
