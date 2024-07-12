# Importar librerías
import yfinance as yf # pip install yfinance


# Definir parámetros
ticker = "AAPL"
inicio = "2021-01-01"
final = "2024-01-01"

# Datos diarios
df = yf.download(tickers=ticker, start=inicio, end=final, interval="1d")
print(df)

# Datos en un minuto
df = yf.download(tickers=ticker, interval="1m")
print(df)

# Datos en una hora
df = yf.download(tickers=ticker, start="2021-01-01",  interval="1h")
print(df)

# Datos semanales
df = yf.download(tickers=ticker, start=inicio, end=final, interval="1wk")
print(df)

# Datos mensuales
df = yf.download(tickers=ticker, start=inicio, end=final, interval="1mo")
print(df)

# Criptomonedas
df = yf.download(tickers="BTC-USD", start=inicio, end=final, interval="1d")
print(df)

# Crear un objeto Ticker de Yahoo Finance
stock = yf.Ticker(ticker="MSFT")
stock_info = stock.info

# Imprimir información relevante
print("Símbolo:", stock_info["symbol"])
print("Nombre:", stock_info["longName"])
print("Precio Actual:", stock_info["currentPrice"])
print("Divisa:", stock_info["currency"])
print("Sitio web:", stock_info["website"])

# Obtener el resumen de la empresa
print("\nResumen de la empresa:")
for key, value in stock_info.items():
    print(f"{key}: {value}")

# Obtener el balance financiero
balance_sheet = stock.balance_sheet
print("\nBalance General:")
print(balance_sheet)

# Obtener los ingresos
income_statement = stock.financials
print("\nIngresos")
print(income_statement)

# Dividendos
dividends = stock.dividends
print("\nDividendos:")
print(dividends)

# Obtener el flujo de efectivo
cashflow = stock.cashflow
print("\nFlujo de Efectivo:")
print(cashflow)

# Recordatorio:
#   - yfinance es una librería muy amplia que permite extraer información en diferentes marcos de tiempo,
#     y además ofrece una diversidad de información muy útil para un análisis más exhaustivo sobre diferentes activos.
