# Importar librerías
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Lista de tickers de las acciones que evaluaremos
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JNJ", "SQ", "PYPL", "META", "NFLX"]

resultados = []
for ticker in tickers:
    # Obtener los datos financieros de la acción
    accion = yf.Ticker(ticker)
    try:
        # Obtener el último precio de cierre
        last_price = accion.info["currentPrice"]
        
        # Obtener el net income y el EBIT
        financials = accion.financials
        net_income = financials.loc["Net Income"][0] # Ingreso Neto
        ebit = financials.loc["EBIT"][0] # Earnings Before Interest and Taxes
        
        # Calcular ROC
        total_assets = accion.balance_sheet.loc["Total Assets"].iloc[0]
        current_liabilities = accion.balance_sheet.loc["Current Liabilities"].iloc[0]
        working_capital = total_assets - current_liabilities
        roc = (ebit / working_capital) * 100
        
        # Calcular el Rendimiento sobre las Ganancias (Earnings Yield)
        earnings_yield = (ebit / last_price) * 100
        
        # Calcular el P/E ratio
        pe_ratio = last_price / (net_income / accion.info["sharesOutstanding"])
        
        # Agregar los resultados a la lista
        resultados.append({
            "Ticker": ticker,
            "ROC": roc,
            "Earnings Yield": earnings_yield,
            "P/E Ratio": pe_ratio
            })
    except Exception as error:
        print("Error obteniendo los datos para:", ticker, error)
        
# Crear un DataFrame con los resultados
resultados = pd.DataFrame(data=resultados, columns=["Ticker", "ROC", "Earnings Yield", "P/E Ratio"]).set_index("Ticker")
# Realizar Ranking
resultados["Ranking"] = resultados["ROC"].rank(ascending=False, na_option="bottom") + \
    resultados["Earnings Yield"].rank(ascending=False, na_option="bottom")
# Ordenar en Base al Ranking y al P/E Ratio
resultados = resultados.sort_values(by=["Ranking", "P/E Ratio"], ascending=[True, False])

# Mostrar las mejores opciones según la estrategia de Greenblatt
print("Mejores Acciones Según Fórmula Mágica:")
print(resultados)        
        
# Simular Estrategia de Inversión

# Activos Óptimos (Según la Fórmula Mágica)
activos_principales = yf.download(tickers=list(resultados.index[:5]), start="2024-01-01", end="2024-07-01")["Close"]
activos_principales_retorno = activos_principales.pct_change().mean(axis=1)
activos_principales_retorno_comportamiento = (1 + activos_principales_retorno).cumprod()

# Activos No tan Óptimos (Según la Fórmula Mágica)
activos_secundarios = yf.download(tickers=list(resultados.index[5:]), start="2024-01-01", end="2024-07-01")["Close"]     
activos_secundarios_retorno = activos_secundarios.pct_change().mean(axis=1)        
activos_secundarios_retorno_comportamiento = (1 + activos_secundarios_retorno).cumprod()

# Graficar retornos
plt.figure(figsize=(22, 12))
activos_principales_retorno_comportamiento.plot(label="Activos Óptimos (Fórmula Mágica)", lw=3, color="green")
activos_secundarios_retorno_comportamiento.plot(label="Activos Secundarios (Fórmula Mágica)", lw=3, color="red")
plt.legend()
plt.grid()
plt.show()        
        
# Recordatorio:
#   - La Fórmula Mágica selecciona acciones utilizando 2 métricas clave: retorno sobre el capital (ROC) y 
#     el rendimiento de ganancias (EY). Las acciones se clasifican según estos criterios. Las empresas con los 
#     puntajes más bajos son consideradas las mejores inversiones.
