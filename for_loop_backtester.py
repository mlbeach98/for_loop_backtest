import numpy as np
import pandas as pd

df = pd.read_csv("AAPL.csv")

# SMA
def SMA(df, columnName, length, newColName):
    """
    Function creates a simple moving average of the columnName column in
    df for a given length, and adds it back to the df under the name newColName

    Inputs:
        df - pandas dataframe
        columnName - name of column in df you would like SMA of
        length - length of moving average
        newColName - name of new column in df
    Outputs:
        none
    """

    colWanted = df[columnName]
    newCol = []

    for i in len(colWanted):
        if i < length - 1:
            newCol.append(0)
        else:
            currentAvg = sum(colWanted[i-length-1:i])/length
            newCol.append(currentAvg)

    df[newColName] = newCol
