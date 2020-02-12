databaseName = "yahoo_data_updated.db"
tableName = "hist"

import numpy as np
import pandas as pd
from os import listdir, remove
import random
import indicators as ind
from datetime import datetime
import sqlite3

conn = None
conn = sqlite3.connect(databaseName)
cur = conn.cursor()

cur.execute("SELECT DISTINCT ticker FROM {};".format(tableName))
tempList = cur.fetchall()
allTickerList = []
for i in tempList:
    allTickerList.append(i[0])

cutoffDate = "20160101"
tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])

tradeResultsCount = 0
tickerCount = 0
for ticker in allTickerList:
    tickerCount += 1
    print("{}/{}: {}".format(tickerCount, len(allTickerList), ticker))
    #read in stock_data

    sqlDf = pd.read_sql_query("SELECT * FROM {} WHERE ticker = '{}';".format(tableName, ticker), conn)
    sqlDf = sqlDf.drop(['tickerDatetime', 'ticker', 'runSplit', 'runDiv'], axis = 1)
    sqlDf = sqlDf.sort_values(by = ['datetime'])

    #if datetime.strptime(data.iloc[0][0], dateFormat) < datetime.strptime(cutoffDate, "%m/%d/%Y"):
    if sqlDf.datetime[0] < cutoffDate:

        adjClose = sqlDf['adjClose'].tolist()
        volume = sqlDf['adjVolume'].tolist()

        sma10 = ind.sma(adjClose, 10)
        sma20 = ind.sma(adjClose, 20)

        buySignal = ind.list1_cross_list2(sma10, sma20)
        sellSignal = ind.list1_cross_list2(sma20, sma10)

        #determine trades
        bought = False

        for i in range(len(sqlDf)):

            if sqlDf.datetime[i] > cutoffDate:
                sqlDf.drop(sqlDf.index[i:], inplace=True)
                break

            if bought == False:
                if buySignal[i] == 1:
                    iVal = i
                    buyDate = sqlDf.datetime[i]
                    buyPrice = sqlDf.adjClose[i]
                    bought = True
            else: #bought == True
                #if data.iloc[i][sellLoc] == 1:
                if sellSignal[i] == 1:
                    sellDate = sqlDf.datetime[i]
                    sellPrice = sqlDf.adjClose[i]
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


tradeResults.to_csv("tradeResultsPartial{}.csv".format(tradeResultsCount))
del tradeResults
tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])
tradeResultsCount += 1

tradeResultsFinal = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])
for i in range(tradeResultsCount):
    for file in listdir():
        if file == "tradeResultsPartial{}.csv".format(i):
            tempDf = pd.read_csv(file)
            remove(file)

            tradeResultsFinal = tradeResultsFinal.append(tempDf, ignore_index = True, sort = False)

tradeResultsFinal = tradeResultsFinal.reset_index()

tradeResultsFinal.to_csv("tradeResults.csv")

averageReturn = tradeResultsFinal['tradeReturn'].mean()
averageDaysHeld = tradeResultsFinal['daysHeld'].mean()

totalCount = 0
winCount = 0

for trade in tradeResultsFinal['tradeReturn']:
    totalCount += 1
    if trade > 0:
        winCount += 1

print("Average Return: {}%".format(round(averageReturn * 100.0, 4)))
print("Average Days Held: {}".format(round(averageDaysHeld,4)))
print("Win rate: {}%".format(round(winCount/totalCount * 100.0, 4)))
