# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import json


# URLs de Wikipedia para diferentes índices bursátiles
urls = {
        
    "S&P 500": {"link": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", "indice": 0, "country": "United States"},
    "Dow Jones Industrial Average": {"link": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", "indice": 1, "country": "United States"},
    "NASDAQ-100": {"link": "https://en.wikipedia.org/wiki/NASDAQ-100", "indice": 4, "country": "United States"},
    "FTSE 100": {"link": "https://en.wikipedia.org/wiki/FTSE_100_Index", "indice": 4, "country": "United Kingdom"},
    "DAX": {"link": "https://en.wikipedia.org/wiki/DAX", "indice": 4, "country": "Germany"},
    "CAC 40": {"link": "https://en.wikipedia.org/wiki/CAC_40", "indice": 4, "country": "France"},
    "Hang Seng Index": {"link": "https://en.wikipedia.org/wiki/Hang_Seng_Index", "indice": 6, "country": "Hong Kong"},
    "ASX 200": {"link": "https://en.wikipedia.org/wiki/S%26P/ASX_200", "indice": 2, "country": "Australia"},
    "S&P/TSX Composite Index": {"link": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index", "indice": 3, "country": "Canada"}
    
}

# Guardar información en un json
archivo = "links_indices.json"
with open(archivo, "w") as file:
    # Convertir a tipo json
    json_dict = json.dumps(urls)
    # Guardar archvio
    json.dump(json_dict, file)
    
# Descargar la lista de componentes del S&P 500 desde Wikipedia
def obtener_activos(indice: str = "S&P 500", archivo: str = "links_indices.json") -> pd.DataFrame:
    
    """
    Descarga los instrumentos que conforman a un índice.
    """
    
    # Cargar el documento
    urls_documento = json.load(open(archivo, "r"))
    urls_dict = json.loads(urls_documento)
    # Asegurarnos de que el índice se encuentre entre los disponibles
    assert indice in list(urls_dict.keys()), f"El valor debe de ser uno de los siguientes {list(urls_dict.keys())}"
    activos_tablas = pd.read_html(urls_dict[indice]["link"])
    componentes = activos_tablas[urls_dict[indice]["indice"]]
    
    return componentes


# Ejemplo (Recordatorio)
if __name__ == "__main__":
    
    # Definir índice
    ticker = "S&P 500"
    archivo = "links_indices.json"
    
    # Obtener activos
    componentes = obtener_activos(ticker, archivo)
    print(componentes)
