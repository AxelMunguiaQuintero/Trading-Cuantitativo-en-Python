# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import nltk
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Cargar opiniones de películas
df = pd.read_csv("../datos/Output.csv")
print(df.head())
print(df["sentiment"].value_counts())

# Tokenización
reseñas_tokens = [nltk.tokenize.word_tokenize(texto.lower()) for texto in df["review"]]
print("Primera reseña tokenizada:")
print(reseñas_tokens[0])

# Lematización
lemmatizer = nltk.stem.WordNetLemmatizer()
lemmatized_reseñas_tokens = [[lemmatizer.lemmatize(token) for token in reseña] for reseña in reseñas_tokens]
print("Lematización de la primera reseña:")
print(lemmatized_reseñas_tokens[0])

# Stemming 
stemmer = nltk.stem.PorterStemmer()
stemmed_reseñas_tokens = [[stemmer.stem(token) for token in reseña] for reseña in lemmatized_reseñas_tokens]
print("Stemming para primera reseña:")
print(stemmed_reseñas_tokens[0])

# Eliminación de Stop Words
stop_words = set(nltk.corpus.stopwords.words("english"))
filtered_reseñas_tokens = [[token for token in reseña if token not in stop_words] for reseña in stemmed_reseñas_tokens]
print("Token sin stop words para primera reseña:")
print(filtered_reseñas_tokens[0])

# Normalización 
normalized_token_reseñas = [[token for token in reseña if token not in string.punctuation] for reseña in filtered_reseñas_tokens]
print("Tokens normalizados para primera reseña:")
print(normalized_token_reseñas[0])

# Unir reseñas
texto_procesado = [" ".join(reseña) for reseña in normalized_token_reseñas]
print("Primer reseña procesada:")
print(texto_procesado[0])

# Crear una instancia del analizador
sia = SentimentIntensityAnalyzer()

# Obtener sentimiento
sentimiento_reseñas = [sia.polarity_scores(reseña) for reseña in texto_procesado]
print(sentimiento_reseñas[:5])

# Calificar como "Positiva" o "Negativa"
sentimiento_general = ["positive" if i["compound"] >=0 else "negative" for i in sentimiento_reseñas]
# Agregar al dataframe
df["Predicciones"] = sentimiento_general

print("Precisión con procesamiento de texto:", (df["sentiment"] == df["Predicciones"]).mean())

# Predecir con el procesamiento interno de VADER
df["Predicciones 2"] = df["review"].apply(lambda x: "positive" if sia.polarity_scores(x)["compound"] >= 0 else "negative")

print("Precisión con procesamiento de texto de VADER:", (df["sentiment"] == df["Predicciones 2"]).mean())

# Recordatorio:
#   - El análisis de sentimiento nos ayuda a entender mejor la opinión sobre diversos temas públicos.
