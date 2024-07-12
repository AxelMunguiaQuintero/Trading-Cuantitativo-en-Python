# Importar librerías
import multiprocessing
import datetime
import pytz # pip install pytz
import time
# Librerías Propias
from Sistema_Intradia import Sistema_Intradia
from Sistema_MedianoPlazo import Sistema_MedianoPlazo
from Sistema_LargoPlazo import Sistema_LargoPlazo

# Ejecutar
if __name__ == "__main__":
    # Ejecutar de manera paralela cada sistema
    s_intradia_proceso = multiprocessing.Process(target=Sistema_Intradia)
    s_medianoPlazo_proceso = multiprocessing.Process(target=Sistema_MedianoPlazo)
    s_largoPlazo_proceso = multiprocessing.Process(target=Sistema_LargoPlazo)
    # Inicializar
    s_intradia_proceso.start()
    s_medianoPlazo_proceso.start()
    s_largoPlazo_proceso.start()
    
    # Definir la zona horario de Nueva York
    ny_tz = pytz.timezone("America/New_York")
    # Obtener la hora actual en Nueva York
    tiempo_actual = datetime.datetime.now(ny_tz)
    # Definir la hora de cierre de mercado (4:00 P.M. ET)
    cierre_mercado = tiempo_actual.replace(hour=16, minute=0, second=0, microsecond=0)
    
    # Dormir código hasta cesar su ejecución
    time.sleep((cierre_mercado - tiempo_actual).seconds)
    # Detener Procesos en ejecución
    s_intradia_proceso.kill()
    s_medianoPlazo_proceso.kill()
    s_largoPlazo_proceso.kill()
    print("¡Jornada ha terminado!")

# Recordatorio:
#   - Cada Sistema de Trading se está ejecutando en un proceso distinto de forma paralela.
#   - Es recomendable ejecutar este script desde terminal para ver que es lo que se está imprimiendo por consola.
