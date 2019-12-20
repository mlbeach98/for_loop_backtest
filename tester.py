import numpy as np
import pandas as pd
from os import listdir, chdir, remove
from os.path import isfile, join
import random
import indicators as ind
from datetime import datetime
import sqlite3

# set to 5 for csv, 4 for sql
indexNum = 4

onlyFiles = []
fileLoc = r"C:\Users\mlbea\Documents\GitHub\stock_data"
resultsLoc = r"C:\Users\mlbea\Documents\GitHub\for_loop_backtest"
resultsLocWith = r"C:\\Users\\mlbea\\Documents\\GitHub\\for_loop_backtest\\"
for file in listdir(fileLoc):
    if isfile(join(fileLoc, file)):
        onlyFiles.append(file.split(".")[0])

tickerList = ['AAPL']
onlyFiles.remove('AAPL')

tickerList = random.sample(onlyFiles, len(onlyFiles))
#tickerList = random.sample(onlyFiles, 10)

chdir(fileLoc)

cutoffDate = "06/01/2015"
tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])

tradeResultsCount = 0
tickerCount = 0
for ticker in tickerList:
    tickerCount += 1
    print("{}/{}: {}".format(tickerCount, len(tickerList), ticker))
    #read in stock_data
    if indexNum == 5:
        data = pd.read_csv(ticker + ".csv")
    elif indexNum == 4:
        conn = None
    	conn = sqlite3.connect('stockData.db')
    	cur = conn.cursor()

        SQL_Query = pd.read_sql_query("SELECT * FROM historical WHERE ticker = '" + ticker + "'", conn)

        SQL_Query.rename(columns = {"adjOpen": "open", "adjHigh": "high", "adjLow": "low", "adjClose": "close", "adjVolume": "volume"})

        data = pd.DataFrame(SQL_Query, columns = ['tickerDatetime', 'ticker', 'datetime', 'adjOpen', 'adjHigh', 'adjLow', 'adjClose', 'adjVolume'])
            data = data.drop(['tickerDatetime', 'ticker'], axis = 1)
    		data = data.sort_values(by=['datetime'])

    if data.iloc[0][0][-5] == "-":
        dateFormat = "%m-%d-%Y"
    elif data.iloc[0][0][-5] == "/":
        dateFormat = "%m/%d/%Y"
    elif data.iloc[0][0][-3] == "-":
        dateFormat = "%Y-%m-%d"

    if datetime.strptime(data.iloc[0][0], dateFormat) < datetime.strptime(cutoffDate, "%m/%d/%Y"):

        #apply indicators

        if indexNum == 4:
            adjClose = data['adjClose'].tolist()
            volume = data['volume'].tolist()
        elif indexNum == 5:
            adjClose = data['Adj Close'].tolist()
            volume = data['Volume'].tolist()
        else:
            print("please set valid indexNum")

        dailyReturns = ind.percent_change(adjClose)
        data['dailyReturns'] = dailyReturns


        sma20 = ind.sma(adjClose, 20)
        data['sma20'] = sma20

        # ema9 = ind.ema(adjClose, 9)
        # data['ema9'] = ema9
        # ema20 = ind.ema(adjClose, 20)
        # data['ema20'] = ema20

        #create signals off indicators
        buySignal = ind.list1_cross_list2(adjClose, sma20)
        data['buySignal'] = buySignal
        sellSignal = ind.list1_above_list2(sma20, adjClose)
        data['sellSignal'] = sellSignal

        # emaCross = ind.list1_cross_list2(ema9, ema20)
        # data['emaCross'] = emaCross
        # increaseVol = ind.increase(volume)
        # data['increaseVol'] = increaseVol
        # buySignal = ind.product([emaCross, increaseVol])
        # data['buySignal'] = buySignal
        #
        # sellSignal = ind.list1_cross_list2(ema20, ema9)
        # data['sellSignal'] = sellSignal

        #determine trades
        bought = False

        buyLoc = data.columns.get_loc('buySignal')
        sellLoc = data.columns.get_loc('sellSignal')

        for i in range(len(data)):

            if datetime.strptime(data.iloc[i][0], dateFormat) > datetime.strptime(cutoffDate, "%m/%d/%Y"):
                data.drop(data.index[i:], inplace=True)
                break

            if bought == False:
                if data.iloc[i][buyLoc] == 1:
                    iVal = i
                    buyDate = data.iloc[i][0]
                    buyPrice = data.iloc[i][indexNum]
                    bought = True
            else: #bought == True
                if data.iloc[i][sellLoc] == 1:
                    sellDate = data.iloc[i][0]
                    sellPrice = data.iloc[i][indexNum]
                    bought = False

                    daysHeld = i - iVal
                    gainLoss = sellPrice - buyPrice
                    tradeReturn = (sellPrice - buyPrice)/buyPrice

                    dict1 = {}
                    dict1['symbol'] = ticker
                    dict1['buyDate'] = buyDate
                    dict1['buyPrice'] = buyPrice
                    dict1['sellDate'] = sellDate
                    dict1['sellPrice'] = sellPrice
                    dict1['daysHeld'] = daysHeld
                    dict1['gainLoss'] = gainLoss
                    dict1['tradeReturn'] = tradeReturn

                    tradeResults = tradeResults.append(dict1, ignore_index=True)

                    if len(tradeResults) >= 25000:
                        chdir(resultsLoc)
                        tradeResults.to_csv("tradeResultsPartial{}.csv".format(tradeResultsCount))
                        del tradeResults
                        tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])
                        chdir(fileLoc)
                        tradeResultsCount += 1

chdir(resultsLoc)
tradeResults.to_csv("tradeResultsPartial{}.csv".format(tradeResultsCount))
del tradeResults
tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])
tradeResultsCount += 1

tradeResultsFinal = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])
for i in range(tradeResultsCount):
    for file in listdir(resultsLoc):
        if file == "tradeResultsPartial{}.csv".format(i):
            tempDf = pd.read_csv(file)
            remove(file)

            tradeResultsFinal = tradeResultsFinal.append(tempDf, ignore_index = True, sort = False)

tradeResultsFinal = tradeResultsFinal.reset_index()

tradeResultsFinal.to_csv("tradeResults.csv")

averageReturn = tradeResultsFinal['tradeReturn'].mean()
averageDaysHeld = tradeResultsFinal['daysHeld'].mean()
individualStockReturns = {}
returnsList = []
for ticker in tickerList:
    tempTradeResults = tradeResultsFinal.drop(tradeResultsFinal[tradeResultsFinal['symbol'] != ticker].index)
    if len(tempTradeResults) > 0:
        individualStockReturns[ticker] = sum(tempTradeResults['tradeReturn'])/len(tempTradeResults)
        returnsList.append(sum(tempTradeResults['tradeReturn'])/len(tempTradeResults))

#drop best and worst stock, average rest
returnsList.remove(max(returnsList))
returnsList.remove(min(returnsList))
individualReturns = sum(returnsList)/len(returnsList)

totalCount = 0
winCount = 0

for trade in returnsList:
    totalCount += 1
    if trade > 0:
        winCount += 1

print("Average Return: {}%".format(round(averageReturn * 100.0, 4)))
print("Average Days Held: {}".format(round(averageDaysHeld,4)))
print("Without outliers: {}%".format(round(individualReturns * 100.0, 4)))
print("Win rate: {}%".format(round(winCount/totalCount * 100.0, 4)))
