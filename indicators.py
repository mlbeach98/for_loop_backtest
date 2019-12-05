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
