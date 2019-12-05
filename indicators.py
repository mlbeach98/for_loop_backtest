def sma(values, length, roundLen = 8):
    """
    Function creates a simple moving average the values list with length length

    Inputs:

        values(list of float) - values to take moving average of
        length(int) - length of moving average
        roundLen(int) - rounds moving average values to this many decimal points (helps
            with floating point calculation)
    Outputs:
        returnValues(list of float) - return list of moving averages
    Tested: Yes
    """

    returnValues = []

    for i in range(len(values)):
        if i < length - 1:
            returnValues.append(0)
        else:
            currentAvg = round(sum(values[i-length+1:i+1])/length, roundLen)
            returnValues.append(currentAvg)

    return returnValues


def ema(values, length, roundLen = 8, emaMult = 0):
    """
    Function creates an exponential moving average the values list with length length

    Inputs:

        values(list of float) - values to take moving average of
        length(int) - length of moving average
        roundLen(int) - rounds moving average values to this many decimal points (helps
            with floating point calculation)
        emaMult(float) - default 0, if left at default uses 2/(length + 1)
    Outputs:
        returnValues(list of float) - return list of moving averages
    Tested: Yes
    """

    if emaMult == 0:
        emaMult = 2/(length + 1)

    returnValues = []

    for i in range(len(values)):
        if i < length - 1:
            returnValues.append(0)
        elif i == length - 1:
            currentAvg = round(sum(values[i-length+1:i+1])/length, roundLen)
            returnValues.append(currentAvg)
        else:
            currentAvg = round(emaMult*values[i] + (1-emaMult)*returnValues[-1], roundLen)
            returnValues.append(currentAvg)

    return returnValues
