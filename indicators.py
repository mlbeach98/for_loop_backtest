def SMA(df, columnName, length, newColName):
    """
    Function creates a simple moving average of the columnName column in
    df for a given length, and adds it back to the df under the name newColName

    Inputs:
        df(dataframe) - pandas dataframe
        columnName(string) - name of column in df you would like SMA of
        length(int) - length of moving average
        newColName(string) - name of new column in df
    Outputs:
        none
    """

    colWanted = df[columnName]
    newCol = []

    for i in range(len(colWanted)):
        if i < length - 1:
            newCol.append(0)
        else:
            currentAvg = sum(colWanted[i-length+1:i+1])/length
            newCol.append(currentAvg)

    df[newColName] = newCol
