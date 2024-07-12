# -*- coding: utf-8 -*-
# Importar librerías
import pandas_datareader as pdr # pip install pandas-datareader
import pandas_datareader.data as web
from datetime import datetime 
import matplotlib.pyplot as plt


# Obtener datos históricos
fecha_inicio = "2020-01-01"
fecha_final = "2024-01-01"
ticker = "AMZN"

# Fuente: Stooq
try:
    df = pdr.get_data_stooq(symbols=ticker, start=fecha_inicio, end=fecha_final)
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    

# Fuente: Stooq
try:
    df = pdr.stooq.StooqDailyReader(symbols=ticker, start=fecha_inicio, end=fecha_final).read()
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    
    
# Fuente: Yahoo
try:
    df = pdr.get_data_yahoo(symbols=ticker, start=fecha_inicio, end=fecha_final)
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    

# Descargar múltiples tickers
tickers = ["AMZN", "AAPL", "MSFT"]
fecha_inicio = datetime(2020, 1, 1)
fecha_final = datetime(2024, 1, 1)
df = web.DataReader(name=tickers, data_source="stooq", start=fecha_inicio, end=fecha_final)
    
    
close = df["Close"]
    
    
# Graficar
close.plot(figsize=(22, 12))
plt.title("Precios de Cierre", size=25)
plt.xlabel("Fecha", size=20)
plt.ylabel("Precios", size=20)
plt.legend()
plt.show()
    
    
# Recordatorio:
#   - Debemos de mantener actualizadas las librerías para evitar cualquier posible error (pip install --upgrade pandas-datareader)
