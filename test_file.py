import numpy as np
import pandas as pd
import indicators as ind

df = pd.read_csv("AAPL.csv")

vals = ind.list_above_value(df['Open'], 199.619995, inclusive=True)

df['vals'] = vals

df.to_csv("value_check.csv")
