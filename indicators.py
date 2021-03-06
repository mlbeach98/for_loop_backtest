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

def list1_above_list2(values1, values2, inclusive = False):
    """
    This function checks, at each index, if values1 is above values2. If so, append 1 to list
        otherwise append 0. If inclusive is true, equal values will return 1. List lengths must
        be equal.
    Inputs:
        values1(list of floats) - values to check if above
        values2(list of floats) - values to test against
        inclusive(bool) - if true, allow value equal to return 1
    Outputs:
        returnValues(binary list) - returns 1 if above, 0 otherwise
    Tested: Yes
    """

    returnValues = []

    if len(values1) != len(values2):
        print("ERROR: lists must be of same length")

    else:
        for i in range(len(values1)):
            if inclusive == False:
                if values1[i] > values2[i]:
                    returnValues.append(1)
                else:
                    returnValues.append(0)
            else:
                if values1[i] >= values2[i]:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    return returnValues

def list1_cross_list2(values1, values2, currentIncl = False, pastIncl = False, above = True):
    """
    This function compares each index of list1 to list2. Given default of above = True,
        if list1[i] > list2[i] and list1[i-1] < list2[i-1], append 1 to returnValues, else
        return 0.
    Inputs:
        values1(list of floats) - values to check if above
        values2(list of floats) - values to test against
        currentIncl(bool) - if true, allow current value equal to be included
        pastIncl(bool) - if true, allow past value equal to be included
        above(bool) - if true, look for list1 to cross above list2. If false, look for
            list2 to cross above list1
    Outputs:
        returnValues(binary list) - returns 1 if above, 0 otherwise
    Tested: Yes
    """

    returnValues = []

    if len(values1) != len(values2):
        print("ERROR: lists must be of same length")

    else:
        for i in range(len(values1)):
            if i == 0:
                returnValues.append(0)

            else:
                if currentIncl == False:
                    if pastIncl == False:
                        if above == True:
                            if values1[i] > values2[i] and values1[i-1] < values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                        else: #above == False
                            if values1[i] < values2[i] and values1[i-1] > values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                    else: #pastIncl == True
                        if above == True:
                            if values1[i] > values2[i] and values1[i-1] <= values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                        else: #above == False
                            if values1[i] < values2[i] and values1[i-1] >= values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                else: #currentIncl == True
                    if pastIncl == False:
                        if above == True:
                            if values1[i] >= values2[i] and values1[i-1] < values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                        else: #above == False
                            if values1[i] <= values2[i] and values1[i-1] > values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                    else: #pastIncl == True
                        if above == True:
                            if values1[i] >= values2[i] and values1[i-1] <= values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

                        else: #above == False
                            if values1[i] <= values2[i] and values1[i-1] >= values2[i-1]:
                                returnValues.append(1)
                            else:
                                returnValues.append(0)

    return returnValues

def list_above_value(values, static, inclusive = False, flipped = False):
    """
    This function tests each index of values against static, and if the currentAvg
        value of values is greater than static, append 1 to returnValues, else append
        0. If inclusive is True, value can be greater than or equal to.
    Inputs:
        values(list of float) - list of values to check against static
        static(float) - value to test list against
        inclusive(bool) - if true, allow value equal to return 1
        flipped(bool) - if true, test value below static
    Outputs:
        returnValues(binary list) - 1 if values above static, 0 otherwise
    Tested: Yes
    """

    returnValues = []

    for i in range(len(values)):
        if inclusive == False and flipped == False:
            if values[i] > static:
                returnValues.append(1)
            else:
                returnValues.append(0)

        elif inclusive == False and flipped == True:
            if values[i] < static:
                returnValues.append(1)
            else:
                returnValues.append(0)

        elif inclusive == True and flipped == False:
            if values[i] >= static:
                returnValues.append(1)
            else:
                returnValues.append(0)

        else:
            if values[i] <= static:
                returnValues.append(1)
            else:
                returnValues.append(0)

    return returnValues

def list_cross_above_value(values, static, inclCurrent = False, inclPast = False, flipped = False):
    """
    if a list index is above a given value, append 1 to returnValues else append 0
    """

    returnValues = []

    if inclCurrent == False and inclPast == False and flipped == False:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] > static and values[i-1] < static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == False and inclPast == False and flipped == True:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] < static and values[i-1] > static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == True and inclPast == False and flipped == False:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] >= static and values[i-1] < static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == True and inclPast == False and flipped == True:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] <= static and values[i-1] > static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == False and inclPast == True and flipped == False:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] > static and values[i-1] <= static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == False and inclPast == True and flipped == True:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] < static and values[i-1] >= static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == True and inclPast == True and flipped == False:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] >= static and values[i-1] <= static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    if inclCurrent == True and inclPast == True and flipped == True:
        for i in range(len(values)):
            if i == 0:
                returnValues.append(0)
            else:
                if values[i] <= static and values[i-1] >= static:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    return returnValues

def percent_change(values):
    """
    This function calculates the day over day change in a list
    Inputs:
        values(list of float) - list of values to find daily change in
    Outputs:
        returnValues(list of float) - percent change from previous observation
    Tested: No
    """

    returnValues = []

    for i in range(len(values)):
        if i == 0:
            returnValues.append(0)
        else:
            returnValues.append((values[i]-values[i-1])/values[i-1])

    return returnValues

def increase(values, inverted = False, inclusive = False):
    """
    This function tells whether a value has increased from the past observation
    Inputs:
        values(list of float) - list of values to check
        inverted(bool) - if true, test decrease
        inclusive(bool) - if true, allows same value to return 1
    Outputs:
        returnValues(binary list) - returns 1 if obs is greater than last, 0 otherwise
    Tested: No
    """

    returnValues = []

    for i in range(len(values)):
        if i == 0:
            returnValues.append(0)
        else:
            if inclusive == False:
                if inverted == False:
                    if values[i] > values[i-1]:
                        returnValues.append(1)
                    else:
                        returnValues.append(0)
                else: #inverted = True
                    if values[i] < values[i-1]:
                        returnValues.append(1)
                    else:
                        returnValues.append(0)
            else: #inclusive = True
                if inverted == False:
                    if values[i] >= values[i-1]:
                        returnValues.append(1)
                    else:
                        returnValues.append(0)
                else: #inverted = True
                    if values[i] <= values[i-1]:
                        returnValues.append(1)
                    else:
                        returnValues.append(0)

    return returnValues

def product(listOfValues):
    """
    This function multiplies the observation at each list for a given index
    Inputs:
        listOfValues(list of list of floats) - lists to be multiplied together
    Outputs:
        returnValues(list of float) - multiplied values
    Tested: No
    """

    if len(listOfValues) < 2:
        print("Please enter at least two lists")

    else:
        lengthList = []
        for i in listOfValues:
            lengthList.append(len(i))

        if min(lengthList) != max(lengthList):
            print("All lists must be of same length")

        else:
            #start actual work here
            returnValues = []
            for i in range(len(listOfValues[0])):

                currentVal = 1
                for list1 in listOfValues:
                    currentVal *= list1[i]

                returnValues.append(currentVal)

            return returnValues

def macd_histogram(values, fastLength = 12, slowLength = 26, signalLength = 9):
    """
    This function computes a macd of "values" which is made up of the fast ema - slow ema, and then taking the difference between that line and the signalLength ema of the line
    """

    fastLine = ema(values, fastLength)
    slowLine = ema(values, slowLength)
    macdLine = []

    for i in range(len(fastLine)):
        if slowLine[i] == 0:
            macdLine.append(0)
        else:
            macdLine.append(fastLine[i] - slowLine[i])

    signalLine = ema(macdLine, signalLength)
    returnValues = []

    for i in range(len(macdLine)):
        if signalLine == 0:
            returnValues.append(0)
        else:
            returnValues.append(macdLine[i] - signalLine[i])

    return returnValues

def rsi(values, rsiLength = 14):
    """
    This function returns the rsi of a given length for "values"
    """

    dailyChange = percent_change(values)

    initGainList = []
    initLossList = []

    for i in range(rsiLength):
        if dailyChange[i] > 0:
            initGainList.append(abs(dailyChange[i]))
        elif dailyChange[i] < 0:
            initLossList.append(abs(dailyChange[i]))

    avgGain = sum(initGainList)/rsiLength
    avgLoss = sum(initLossList)/rsiLength

    if avgLoss == 0:
        RS = 1000000000 #just need some non zero large number here
    else:
        RS = avgGain / avgLoss

    RSI = 100 - (100 / (1 + RS))

    returnValues = []

    for i in range(len(values)):
        if i < rsiLength - 1:
            returnValues.append(0)
        elif i == rsiLength:
            returnValues.append(RSI)
        else:
            if dailyChange[i] > 0:
                avgGain = ((avgGain * (rsiLength - 1)) + abs(dailyChange[i])) / rsiLength
            elif dailyChange[i] < 0:
                avgLoss = ((avgLoss * (rsiLength - 1)) + abs(dailyChange[i])) / rsiLength

            if avgLoss == 0:
                RS = 1000000000 #just need some non zero large number here
            else:
                RS = avgGain / avgLoss

            returnValues.append(100 - (100 / (1 + RS)))

    return returnValues

def lookback(values, lookbackLength, all = False):
    """
    This function checks if an observation in the past lookbackLength observations was a 1 in values. If all is set to true, this will only return 1 if all the values are 1.
    """

    returnValues = []

    if all == False:
        for i in range(len(values)):
            if i < lookbackLength - 1:
                if sum(values[:i+1]) > 0:
                    returnValues.append(1)
                else:
                    returnValues.append(0)
            else: #enough observations
                if sum(values[i-lookbackLength+1:i+1]) > 0:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    elif all == True:
        for i in range(len(values)):
            if i < lookbackLength - 1:
                if sum(values[:i]) == i + 1:
                    returnValues.append(1)
                else:
                    returnValues.append(0)
            else: #enough observations
                if sum(values[i-lookbackLength:i]) == lookbackLength:
                    returnValues.append(1)
                else:
                    returnValues.append(0)

    return returnValues
