# Importar librerías
import yfinance as yf
import pandas as pd
import time

# Obtener capitalización de mercado
def market_cap(instrumento: str) -> float:
    
    """
    Obtiene la capitalización de mercado para un activo (acción).
    """
    
    # Obtener datos
    accion = yf.Ticker(ticker=instrumento)
    marketCap = accion.info.get("marketCap", 0)
    
    return marketCap

# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Librerías Propias
    from InstrumentosFinancieros import obtener_activos
    
    # Definir índice
    ticker_indice = "S&P 500"
    archivo = "links_indices.json"
    componentes = obtener_activos(ticker_indice, archivo)
    # Crear una nueva columna para el marketCap
    componentes["marketCap"] = 0
    # Extraer su nivel de capitalización
    for n, ticker in enumerate(componentes["Symbol"]):
        print("Información para:", ticker, "con índice ->", n)
        marketCap = market_cap(ticker)
        componentes.loc[n, "marketCap"] = marketCap
        time.sleep(0.50)
    print(componentes)
    # Guardar
    componentes.set_index("Symbol").to_csv(ticker_indice + ".csv")
    # Cargar
    componentes = pd.read_csv(ticker_indice + ".csv", index_col="Symbol")
