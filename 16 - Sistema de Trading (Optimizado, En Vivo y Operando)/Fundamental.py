# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import time

# Definir función
def Formula_Magica(tickers: list) -> pd.DataFrame:
    
    """
    Calcula la metodología de la Fórmula Mágica para un conjunto de activos.
    """
    
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
            
        # Dormir para evitar bloqueos del servidor
        time.sleep(1)
            
    # Crear un DataFrame con los resultados
    resultados = pd.DataFrame(data=resultados, columns=["Ticker", "ROC", "Earnings Yield", "P/E Ratio"]).set_index("Ticker")
    # Realizar Ranking
    resultados["Ranking"] = resultados["ROC"].rank(ascending=False, na_option="bottom") + \
        resultados["Earnings Yield"].rank(ascending=False, na_option="bottom")
    # Ordenar en Base al Ranking y al P/E Ratio
    resultados = resultados.sort_values(by=["Ranking", "P/E Ratio"], ascending=[True, False])
    
    return resultados
    
    
# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Cargar Datos
    df_archivo = "S&P 500.csv"
    df = pd.read_csv(df_archivo, index_col="Symbol")
    # Ordenar en base a capitalización (Mantener 100 más grandes)
    df = df.sort_values(by="marketCap", ascending=False).iloc[:100]
    # Encontrar mejores en base a la metodología de Fórmula Mágica
    fm = Formula_Magica(tickers=list(df.index))
    print(fm)
    # Guardar datos
    fm.dropna().to_csv("FormulaMagica.csv")
