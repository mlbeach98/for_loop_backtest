import numpy as np
import pandas as pd
import indicators as ind

df = pd.read_csv("AAPL.csv")

adjClose = df['Adj Close'].tolist()

rsi = ind.rsi(adjClose)
df['rsi'] = rsi

rsiCross30 = ind.list_cross_above_value(rsi, 30)
df['crossAbove30'] = rsiCross30

lookback = ind.lookback(rsiCross30, 10)
df['lookback10'] = lookback

df.to_csv("value_check.csv")
