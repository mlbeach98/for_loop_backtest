import numpy as np
import pandas as pd
import indicators as ind

df = pd.read_csv("AAPL.csv")

vals = ind.sma(df['Adj Close'], 10)

df['vals'] = vals

df.to_csv("value_check.csv")
