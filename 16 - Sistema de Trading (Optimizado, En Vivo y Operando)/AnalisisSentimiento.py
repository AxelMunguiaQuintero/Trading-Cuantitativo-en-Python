# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Extraer Sentimiento
def Sentimiento_Mercado(ticker: str) -> pd.DataFrame:
    
    """
    Extrae el sentimiento de un activo a través de los titulares.
    """
    
    # Definir url de FINVIZ
    url = "https://finviz.com/quote.ashx?t={}&p=d"
    
    # Extraer HTML
    extracciones = []
    # Crear usuarios falsos para realizar las peticiones (evitar bloqueos)
    ua = UserAgent()
    header = {"User-Agent": str(ua.chrome)}
    # Petición
    r = requests.get(url=url.format(ticker), headers=header)
    soup = BeautifulSoup(r.content, "html5lib")
    # Localizar tabla con noticias
    tabla_noticias = soup.find(id="news-table")
    # Localizar cada noticia individual
    noticias = tabla_noticias.findAll(name="tr")
    # Guardar noticias y los titulares
    for noticia in noticias:
        datos_noticia = noticia.find(name="a", attrs={"class":"tab-link-news"})
        titular = datos_noticia.text
        fecha_publicacion = noticia.find(name="td").text.replace("\n", "").strip().split()
        # Dar formato correcto a la fecha
        if len(fecha_publicacion) == 2:
            fecha = fecha_publicacion[0]
            hora = fecha_publicacion[1]
            if fecha.lower() == "today":
                fecha = datetime.now().strftime("%b-%d-%y")
        else:
            hora = fecha_publicacion[0]
            
        extracciones.append([ticker, fecha, hora, titular])
            
    # Convertir a DataFrame
    noticias = pd.DataFrame(data=extracciones, columns=["Ticker", "Fecha", "Hora", "Titular"])   
    noticias["Fecha"] = pd.to_datetime(noticias["Fecha"], format="%b-%d-%y")
            
    # Obtener sentimiento
    sia = SentimentIntensityAnalyzer()
    noticias["sentimiento"] = noticias["Titular"].apply(lambda x: sia.polarity_scores(x)["compound"])    
    
    # Agrupar datos por ticker y por día
    noticias_agrupadas = noticias[["Ticker", "Fecha", "sentimiento"]].groupby(["Ticker", "Fecha"]).mean()
    noticias_agrupadas.reset_index(inplace=True)
    
    return noticias_agrupadas

# Ejemplo (Recordatorio)
if __name__ == "__main__":
    # Definir activo
    ticker = "AMZN"
    # Obtener sentimiento
    sentimiento = Sentimiento_Mercado(ticker)
    print(sentimiento)
