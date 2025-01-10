# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf

# Definir ticker y obtener datos
ticker = "AAPL"
accion = yf.Ticker(ticker)
flujo_de_caja = accion.cashflow

# Definir parámetros para el modelo de valoración
tasa_crecimiento = 0.03 # Tasa de crecimiento anual estimada para el flujo de caja libre
tasa_descuento = 0.1 # Tasa de descuento para descontar los flujos de caja al valor presente
tasa_crecimiento_terminal = 0.02 # Tasa de crecimiento perpetuo después del periodo de proyección
años_proyeccion = 5 # Número de años para proyectar el flujo de caja

# Obtener flujo de caja libre (FCF) del año más reciente
fcf = flujo_de_caja.loc["Free Cash Flow"][0]

# Proyectar FCF para los próximos años
proyecciones_fcf = [fcf * (1 + tasa_crecimiento) ** i for i in range(1, años_proyeccion + 1)]

# Calcular valor terminal
valor_terminal = proyecciones_fcf[-1] * (1 + tasa_crecimiento_terminal) / (tasa_descuento - tasa_crecimiento_terminal)

# Descontar los flujos de caja y el valor terminal al presente
valor_dcf = sum([fcf / (1 + tasa_descuento) ** (i + 1) for i, fcf in enumerate(proyecciones_fcf)])
valor_dcf += valor_terminal / (1 + tasa_descuento) ** años_proyeccion

# Obtener el número de acciones en circulación
acciones_en_circulacion = accion.info["sharesOutstanding"]

# Calcular el valor intrínseco por acción
valor_intrinseco_por_accion = valor_dcf / acciones_en_circulacion
print(f"Valor Intrínseco de {ticker}: ${valor_intrinseco_por_accion:.2f} por acción")
print(f"Valor Actual de {ticker}: ${accion.info['currentPrice']}")

# Recordatorio:
#   - La Tasa de Crecimiento representa una estimación del crecimiento anual del flujo de caja libre. Un 3% es una
#     suposición conservadora y razonable para muchas empresas maduras.
#   - La Tasa de Descuento se utiliza para descontar los flujos de caja futuros al valor presente. Un 10% es una tasa
#     comúnmente utilizada que refleja el costo de capital de una empresa.
#   - La Tasa de Crecimiento Terminal representa el crecimiento perpetuo del flujo de caja del perído de proyección.
#     Un 2% es una suposición conservadora que refleja el crecimiento a largo plazo de la economía.
#   - Un periodo de 5 años para proyectar los flujos de caja, es estándar y permite una proyección razonable
#     sin ser demasiado incierto.
#   - El valor intrínseco es la valoración real de una empresa basada en fundamentos financieros, independiente de su precio
#     de mercado.
