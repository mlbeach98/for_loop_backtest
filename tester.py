import numpy as np
import pandas as pd
from os import listdir, chdir
from os.path import isfile, join
import random
import indicators as ind
from datetime import datetime

onlyFiles = []
fileLoc = r"C:\Users\mlbea\Documents\GitHub\stock_data"
for file in listdir(fileLoc):
    if isfile(join(fileLoc, file)):
        onlyFiles.append(file.split(".")[0])

tickerList = random.sample(onlyFiles, 10)

chdir(fileLoc)

symbolData = {}
cutoffDate = "06/01/2015"
tradeResults = pd.DataFrame(columns = ['symbol', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'daysHeld', 'gainLoss', 'tradeReturn'])

for ticker in tickerList:
    #read in stock_data
    data = pd.read_csv(ticker + ".csv")
    if datetime.strptime(data.iloc[0][0], "%Y-%m-%d") < datetime.strptime(cutoffDate, "%m/%d/%Y"):
        print("dates good")

        #apply indicators
        adjClose = data['Adj Close'].tolist()
        dailyReturns = ind.percent_change(adjClose)
        data['dailyReturns'] = dailyReturns

        ema9 = ind.ema(adjClose, 9)
        data['ema9'] = ema9

        #create signals off indicators
        buySignal = ind.list1_cross_list2(adjClose, ema9)
        data['buySignal'] = buySignal

        sellSignal = ind.list1_cross_list2(adjClose, ema9, above=False)
        data['sellSignal'] = sellSignal

        #determine trades
        bought = False

        buyLoc = data.columns.get_loc('buySignal')
        sellLoc = data.columns.get_loc('sellSignal')

        for i in range(len(data)):
            if bought == False:
                if data.iloc[i][buyLoc] == 1:
                    print("trade_b")
                    iVal = i
                    buyDate = data.iloc[i][0]
                    buyPrice = data.iloc[i][5]
                    bought = True
            else: #bought == True
                if data.iloc[i][sellLoc] == 1:
                    print("trade")
                    sellDate = data.iloc[i][0]
                    sellPrice = data.iloc[i][5]
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

        #analyze results
        symbolData[ticker] = data

chdir(r"C:\Users\mlbea\Documents\GitHub\for_loop_backtest")
tradeResults.to_csv("tradeResults.csv")
