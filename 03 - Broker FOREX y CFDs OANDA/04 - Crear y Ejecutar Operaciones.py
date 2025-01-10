# -*- coding: utf-8 -*-
# Importar librerías
import tpqoa

# Conexión a la API
oanda = tpqoa.tpqoa(conf_file="config.cfg")

# Crear Posición de Compra EUR_USD
ticker = "EUR_USD"
precios = oanda.get_prices(instrument=ticker)
precio_actual = (precios[1] + precios[2]) / 2
orden_compra = oanda.create_order(instrument=ticker, units=1000, sl_distance=0.01, tp_price=round(precio_actual + 0.01, 4), ret=True)

# Ver posiciones activas
print(oanda.get_positions())

# Cerrar Posición EUR_USD con una de venta
ticker = "EUR_USD"
orden_venta = oanda.create_order(instrument=ticker, units=-1000)

# Ver posiciones activas
print(oanda.get_positions())

# Imprimir Transacciones de la Cuenta
oanda.print_transactions()

# Obtener información de la cuenta
cuenta_info = oanda.get_account_summary()
print("Rendimiento de la cuenta:", cuenta_info["pl"])

# Obtener información histórica de transacciones
historial_transacciones = oanda.get_transactions()

# Obtener información específica de una transacción
print(oanda.get_transaction(tid=orden_compra["id"]))

# Recordatorio:
#   - La creación de órdenes debe realizarse con cautela, pues errores en la configuración o ejecución de una orden pueden
#     resultar en pérdidas financieras.
