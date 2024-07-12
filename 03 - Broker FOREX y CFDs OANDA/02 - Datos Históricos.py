# Importar librerías
import tpqoa

# Generar conexión
oanda = tpqoa.tpqoa(conf_file="config.cfg")

# Parámetros
ticker = "XAU_USD"
inicio = "2023-01-01"
final = "2024-01-01"

# Datos Históricos
help(oanda.get_history)

# Datos diarios
df = oanda.get_history(instrument=ticker, start=inicio, end=final, granularity="D", price="M")
print("Número de Filas:", df.shape[0])
print(df)

# Datos intradía
df = oanda.get_history(instrument=ticker, start=inicio, end="2023-01-08", granularity="S5", price="M")
print("Número de Filas:", df.shape[0])
print(df)

df = oanda.get_history(instrument=ticker, start=inicio, end="2023-01-08", granularity="H1", price="M")
print("Número de Filas:", df.shape[0])
print(df)

# Obtener Precios Actuales
print(oanda.get_prices(instrument=ticker))

# Recordatorio:
#   - La librería tpqoa elimina las limitaciones de OANDA al manejar automáticamente la obtención de grandes
#     volúmenes de datos sin intervención manual.
