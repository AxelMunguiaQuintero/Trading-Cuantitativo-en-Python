# -*- coding: utf-8 -*-
# Importar librerías
import nltk
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # pip install vaderSentiment

# Descargar recursos necesarios de NLTK
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# Texto de ejemplo
texto = "Cats love to play with small balls! They are playful and energetic."

# 1) Tokenización: Divide el texto en unidades más pequeñas (tokens), generalmente palabras
tokens = nltk.tokenize.word_tokenize(texto.lower())
print("Tokens:", tokens)

# 2) Lematización: Reduce las palabras a su forma base o lema. Por ejemplo, "cats" se convierte en "cat"
lematizer = nltk.stem.WordNetLemmatizer()
lemmatized_tokens = [lematizer.lemmatize(token) for token in tokens]
print("Lematización:", lemmatized_tokens)

# 3) Steamming: Reduce las palabras a su raíz. Por ejemplo, "playful" se convierte en "play"
stemmer = nltk.stem.PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
print("Stemming:", stemmed_tokens)

# 4) Eliminación de Stop Words: Elimina palabras comunes que no aportan mucho significado ("in", "is", "the")
stop_words = set(nltk.corpus.stopwords.words("english"))
filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]
print("Tokens sin Stop Words:", filtered_tokens)

# 5) Normalización (remover puntuaciones): Limpia el texto eliminando puntuación, emoticonos y otros caracteres especiales no deados.
normalized_tokens =[token for token in filtered_tokens if token not in string.punctuation]
print("Tokens normalizados:", normalized_tokens)

# Unir tokens en una sola sentencia nuevamente
texto_procesado = " ".join(normalized_tokens)
print(texto_procesado)

# Crear Instancia del Analizador de Sentimiento
sia = SentimentIntensityAnalyzer()

# Obtener Sentimiento
scores = sia.polarity_scores(texto_procesado)
print(scores)

# Validar el sentimiento
if scores["compound"] >= 0:
    print("¡La frase tiene un sentimiento Positivo!")
else:
    print("¡La frase tiene un sentimiento Negativo!")
    
# Analizar el Texto sin Procesamiento Propio
sent_no_procesada = sia.polarity_scores(texto)
print(sent_no_procesada)

# Validar el sentimiento
if sent_no_procesada["compound"] >= 0:
    print("¡La frase tiene un sentimiento Positivo!")
else:
    print("¡La frase tiene un sentimiento Negativo!")

# Recordatorio:
#   - El análisis de sentimiento requiere un procesamiento adecuado del texto para obtener resultados precisos.
#   - El análisis de sentimiento nos ayuda a comprender las opiniones expresadas en el texto proporcionando probabilidades
#     de cómo se siente la gente hacia un tema específico.
