# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import pandas_ta as pd_ta # pip install pandas-ta
import ta # pip install ta

# Obtener datos
df = pd.read_csv("../datos/AMZN.csv", index_col="Date", parse_dates=True)

# Indicadores de pandas_ta
ma = pd_ta.overlap.ma("sma", df["Close"], length=8) # Simple Moving Average
ema = pd_ta.overlap.ema(close=df["Close"], length=14) # Exponential Moving Average
cci = pd_ta.momentum.cci(high=df["High"], low=df["Low"], close=df["Close"], length=14) # Commodity Channel Index
atr = pd_ta.atr(high=df["High"], low=df["Low"], close=df["Close"], length=21) # Average True Range

# Indicadores de ta
rsi = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
macd = ta.trend.MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9).macd()
cmf = ta.volume.ChaikinMoneyFlowIndicator(high=df["High"], low=df["Low"], close=df["Close"], volume=df["Volume"]).chaikin_money_flow()
