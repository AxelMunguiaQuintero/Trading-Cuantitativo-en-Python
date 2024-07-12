# Importar librerías
import multiprocessing
import numpy as np


# Definir función
def operaciones_rango(limite_inferior: int, limite_superior: int, diccionario, clave, sincronizador) -> None:
    
    """
    Realiza una diversidad de operaciones a un grupo de números para obtener un único valor
    """
    
    # Calcular
    valor = 0
    for i in range(limite_inferior, limite_superior + 1):
        valor += np.sqrt((i * 3) + ((i + 15) / 10))
        
    sincronizador.acquire()
    diccionario[clave] = valor
    sincronizador.release()
        
    print(f"El valor obtenido en el rango [{limite_inferior}, {limite_superior}] = {valor}")
    
    
if __name__ == "__main__":
    
    # Declarar rangos de valores
    limites_inferiores = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    limites_superiores = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
    
    # Diccionario de memoria compartida
    manager = multiprocessing.Manager()
    dict_resultados = manager.dict()
    
    # Sincronizador
    mutex = multiprocessing.Lock()
    
    # Crear e Inicializar los Procesos
    procesos_lista = []
    for i in range(len(limites_inferiores)):
        p = multiprocessing.Process(target=operaciones_rango, kwargs={"limite_inferior": limites_inferiores[i],
                                                                      "limite_superior": limites_superiores[i],
                                                                      "diccionario": dict_resultados,
                                                                      "clave": f"Proceso_{i}",
                                                                      "sincronizador": mutex})
        procesos_lista.append(p)
        p.start()
        
    # Esperar a que terminen los procesos su ejecución
    for p in procesos_lista:
        p.join()
        
    # Mostrar por consola el diccionario
    print("\n\nObjeto de Memoria Compartida\n\n")
    print(dict_resultados.items())
        
# Recordatorio:
#   - Los sincronizadores nos ayudan a evitar la corrupción de nuestros datos y son perfectas herramientas para un orden
#     en la ejecución de tareas paralelas.
#   - Los objetos de memoria compartida son útiles para compartir, agregar o modificar información.
#   - El uso de JOIN nos permite esperar a que los Hilos o Procesos cesen su ejecución.
